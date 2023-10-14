from functools import reduce
from datetime import date

from django.db.models import Q
from django.conf import settings
from django.contrib import admin
from django.contrib import messages
from django.utils import timezone
from django.utils.html import format_html
from django.db.models import Subquery, OuterRef, Count, Sum
from django.conf import settings

from rest_framework.authtoken.models import Token

from annotation import models
from annotation.forms import ClientDomainRelationshipAdminForm
from annotation.utils import ExportCsvMixin

year, week, _ = timezone.now().isocalendar()

from annotation import admin_filters

class CommonUrlActionsMixin(ExportCsvMixin):

    actions = ["greenlist_selected_urls", "redlist_selected_urls", "amberlist_selected_urls",
               "low_priority", "medium_priority", "high_priority", "reset_urls", "export_items_to_csv"]

    def delete_without_confirmation(self, request, queryset):
        """
        default implementation fails because too may rows are affected.
        We override to skip the confirmation screen
        """
        queryset.delete()
        self.message_user(request, f"{queryset.count()} urls deleted successfully!", messages.SUCCESS)

    def redlist_selected_urls(self, request, queryset):
        queryset.update(status="red")
        self.message_user(request, f"{queryset.count()} urls redlisted successfully!", messages.SUCCESS)

    def amberlist_selected_urls(self, request, queryset):
        queryset.update(status="amber")
        self.message_user(request, f"{queryset.count()} urls amberlisted successfully!", messages.SUCCESS)

    def low_priority(self, request, queryset):
        queryset.update(priority=3)
        self.message_user(request, f"{queryset.count()} url priorities set to low!", messages.INFO)
    low_priority.short_description = "Change Priority to Low"

    def medium_priority(self, request, queryset):
        queryset.update(priority=2)
        self.message_user(request, f"{queryset.count()} url priorities set to medium!", messages.INFO)
    medium_priority.short_description = "Change Priority to Medium"

    def high_priority(self, request, queryset):
        queryset.update(priority=1)
        self.message_user(request, f"{queryset.count()} url priorities set to high!", messages.INFO)
    high_priority.short_description = "Change Priority to High"

    def reset_urls(self, request, queryset):
        count = queryset.count()
        for url in queryset:
            url.known = False
            url.save()
            tasks = url.tasks.all()
            tasks.delete()
            url.intent_data.all().delete()
        self.message_user(request, f"{count} url reset!", messages.INFO)
 


class StepInline(admin.StackedInline):
    model = models.Step


class TaskAdmin(admin.ModelAdmin, ExportCsvMixin):
    inlines = [StepInline, ]
    list_display = ('get_url','user', 'state','start_date','mode', 'current_step', 'date_completed', 'action')
    list_filter = ('user', 'state','mode', 'date_completed')
    actions = ("mark_as_bad_url", "reset_and_clear_archive", "redlist_task_url", "export_items_to_csv")
    raw_id_fields = ("url",)
    search_fields = ('url__url',) #Search url field of url model

    def get_queryset(self, request):
        """
        Restrict views for annotators to their tasks only
        """
        queryset = super().get_queryset(request)
        if not request.user.is_superuser and request.user.user_type == "annotator":
            queryset = queryset.filter(user=request.user)

        return queryset

    def get_url(self, obj):
        return obj.url.short_url
    
    def current_step(self, obj):
        try:
            return obj.steps.last().step
        except:
            return None

    def action(self, obj):
        return format_html(
            f"""<a href="{obj.url.archived_url}"
            class="btn btn-success float-right"
            target="_blank" title="{obj.url.archived_url}">View archive</a>"""
            )
    def mark_as_bad_url(self, request, queryset):
        for task in queryset:
            task.state = "bad_url"
            task.completed=True
            task.save()
        self.message_user(
            request, f"{task.url.url} has been marked as a bad url! {task.user} will get a new task on next request.", messages.INFO)

    def reset_and_clear_archive(self, request, queryset):
        """
        Useful for tasks marked as bad due to faulty archive
        """
        for task in queryset:
            task.url.archived_url = ""
            task.url.save()
            task.delete()
        self.message_user(
            request, f"Archives for selected urls has been cleared. These urls will be re-archived and reassigned", messages.INFO)

    def redlist_task_url(self, request, queryset):
        for task in queryset:
            task.url.status = "red"
            task.url.save()
        self.message_user(
            request, f"Urls of the selected tasks has been redlisted!", messages.INFO)

    get_url.short_description = 'Url'


class CountryInline(admin.StackedInline):
    model = models.Country.urls.through
    extra = 0


class ClientInline(admin.StackedInline):
    model = models.Client.urls.through
    extra = 0

@admin.register(models.Url)
class UrlAdmin(admin.ModelAdmin, CommonUrlActionsMixin):
    list_display = ('short_url', 'page_views', 'last_counted', 'events', 'priority', 'status', 'known', "action")
    actions = CommonUrlActionsMixin.actions
    search_fields = ('url',)
    list_filter = ('status','known',)
    raw_id_fields = ("domain",)
    readonly_fields = ("annotators_assigned",)
    inlines = [CountryInline, ClientInline]

    def action(self, obj):
        return format_html(
            f"""<a href="{obj.url}" class="btn btn-success float-right" target="_blank" title="{obj.url}">Visit</a>"""
            )
            
    def get_search_results(self, request, queryset, search_term):
            '''
            This enables search with regular expressions.
            If a query starts with `^`, it's automaticaally treated as a reqular expression search
            '''
            if search_term.startswith('^'):
                # we're performing the search using the specified search fields dynamically
                return queryset.filter(reduce(lambda x, y: x | y,
                                            [Q(**{'{}__iregex'.format(field): search_term})
                                            for field in self.search_fields])), True
            return super().get_search_results(request, queryset, search_term)

class RawUrlAdmin(admin.ModelAdmin, CommonUrlActionsMixin):
    list_display = ('full_url', 'page_views','status','priority',)
    list_editable = ('status', 'priority')
    list_display_links = None
    actions = CommonUrlActionsMixin.actions
    radio_fields = {"status": admin.HORIZONTAL, "priority": admin.HORIZONTAL}
    search_fields = ('url',)

    def get_queryset(self, request):
        """
        This tab is specifically for the annotators to greenlist urls.
        We only want to show them urls that are yet to be greenlisted
        """
        qs = super().get_queryset(request)
        return qs.filter(status="amber").exclude(domain__status="red")

    def full_url(self, obj):
        return format_html(f"<a href='{obj.url}' target='_blank'>{obj.url}</a>")

    def has_add_permission(self, request, obj=None):
        #This is not an actual model, so we want to disable adding objects.
        return False

    def has_delete_permission(self, request, obj=None):
        #Deleting an object here will be deleting the actual user. We don't want that
        return False

@admin.register(models.DomainPriority)
class DomainPriorityAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('domain', 'approximate_urls', 'views', )
    search_fields = ('domain',)
    actions = ["export_items_to_csv"] 


class FacetPropertyInline(admin.StackedInline):
    model = models.FacetProperty

class SelectedProductsInline(admin.StackedInline):
    model = models.SelectedProduct

class IntentDataAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('short_url', 'department', 'category', 'subcategory', 'subset', 'intent', 'date_processed', )
    list_filter = (
        'department', 
        admin_filters.CategoryListFilter, 
        admin_filters.SubCategoryListFilter,
        admin_filters.SubSetListFilter,
        'facet_properties__facet',
        'date_processed',
    )
    raw_id_fields = ("url",)
    actions = ("delete_without_confirmation", "export_items_to_csv")
    inlines = [FacetPropertyInline, SelectedProductsInline]

    def short_url(self, obj):
        return obj.url.short_url

    def delete_without_confirmation(self, request, queryset):
        """
        default implementation fails because too may rows are affected.
        We override to skip the confirmation screen
        """
        queryset.delete()



class IntentDataInline(admin.StackedInline):
    model = models.IntentData


class KnownUrlsAdmin(admin.ModelAdmin):
    inlines = [IntentDataInline]
    search_fields = ("url", )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(known=True)



class AnnotationStatsFilter(admin.SimpleListFilter):
    title = ""

    parameter_name = 'has_annotated'

    def lookups(self, request, model_admin):
        return (
            ('1', ('Annotators')),
            ('2', ('All Users')),
            ('3', ('Completed an annotation this month')),
            ('4', ('Completed an annotation last month')),
        )

    def queryset(self, request, queryset):
        # set default state of the filter to 1
        if self.value() is None:
            self.used_parameters[self.parameter_name] = '1'
        else:
            self.used_parameters[self.parameter_name] = int(self.value())

        if self.value() == '1':
            queryset = queryset.filter(user_type="annotator")
            return queryset

        if self.value() == '2':
            return queryset
    
        if self.value() == '3':
            queryset = queryset.annotate(_count=Subquery(models.Task.objects.filter(user = OuterRef("pk"), state="completed", mode="annotator", date_completed__month=timezone.now().month).values("user").annotate(count = Count('pk')).values("count")))
            return queryset.exclude(_count__lt=1)

        if self.value() == '4':
            queryset = queryset.annotate(_count=Subquery(models.Task.objects.filter(user = OuterRef("pk"), state="completed", mode="annotator", date_completed__month=timezone.now().month-1).values("user").annotate(count = Count('pk')).values("count")))
            return queryset.exclude(_count__lt=1)



class AnnotationStatsAdmin(admin.ModelAdmin):
    list_display = ('email', 'today', 'this_week', 'this_month','last_month','all_time')
    list_display_links = None
    list_filter = (AnnotationStatsFilter,)

    def get_queryset(self, request):
        """
            Restrict annotation scoreboard to show current user only
            unless current user is a superuser
        """
        queryset = super().get_queryset(request)
        #make columns sortable
        
        queryset = queryset.annotate(_today = Subquery(models.Task.objects.filter(user = OuterRef("pk"), state="completed", mode="annotator", date_completed__date=date.today()).values("user").annotate(count = Count('pk')).values("count")),
                                     _this_week = Subquery(models.Task.objects.filter(user = OuterRef("pk"), state="completed", mode="annotator", date_completed__week=week, date_completed__year=year).values("user").annotate(count = Count('pk')).values("count")),
                                    _this_month = Subquery(models.Task.objects.filter(user = OuterRef("pk"), state="completed", mode="annotator", date_completed__month=timezone.now().month, date_completed__year=year).values("user").annotate(count = Count('pk')).values("count")),
                                    _last_month = Subquery(models.Task.objects.filter(user = OuterRef("pk"), state="completed", mode="annotator", date_completed__month=timezone.now().month-1, date_completed__year=year).values("user").annotate(count = Count('pk')).values("count")),
                                    _all_time = Subquery(models.Task.objects.filter(user = OuterRef("pk"), state="completed", mode="annotator").values("user").annotate(count = Count('pk')).values("count")),
                                    )
        if not request.user.is_superuser:
            return queryset.filter(email = request.user.email)    
        else:
            return queryset
            
    def today(self, obj):
        return obj._today

    def this_week(self, obj):
        return obj._this_week

    def this_month(self, obj):
        return obj._this_month
    
    def last_month(self, obj):
        return obj._last_month

    def all_time(self, obj):
        return obj._all_time

    def has_add_permission(self, request):
        #This is not an actual model, so we want to disable adding objects.
        return False

    def has_delete_permission(self, request):
        #Deleting an object here will be deleting the actual user. We don't want that
        return False

    today.admin_order_field = '_today'
    this_week.admin_order_field = '_this_week'
    this_month.admin_order_field = '_this_month'
    last_month.admin_order_field = '_last_month'
    all_time.admin_order_field = '_all_time'

    
class TBAQAdmin(admin.ModelAdmin, CommonUrlActionsMixin):
    list_display = ('url', 'archive_url', 'page_views','status','priority','annotators_assigned',"action")
    list_editable = ('status', 'priority')
    actions = CommonUrlActionsMixin.actions
    search_fields = ('url',)

    def get_queryset(self, request):
        """
        This tab is to visualise the urls currently in queue
        """
        queryset = super().get_queryset(request)
        return queryset.filter(url__in=[url.url for url in models.Url.objects.tbaq()])

    def action(self, obj):
        return format_html(
            f"""<a href="{obj.archived_url}" class="btn btn-success float-right" target="_blank" title="{obj.url}">View</a>"""
            )

    def has_delete_permission(self, request, *args, **kwargs):
        #Deleting an object here will be deleting the actual url. We don't want that
        return False

    def has_add_permission(self, request, *args, **kwargs):
        return False

    def archive_url(self, obj):
        return obj.archived_url[0:10]


@admin.register(models.NewTBAQ)
class NewTBAQAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('queue', 'url', 'events', 'total_page_view',)
    raw_id_fields = ['url']
    actions = ["export_items_to_csv"]

    def url(self, obj):
        return obj.url.short_url

    def queue(self, obj):
        return str(obj)

    def total_page_view(self, obj):
        return str(sum([pageview.number_of_views for pageview in obj.page_views.all()]))

    def get_queryset(self, request):
        """
        Show only urls that are greenlisted (status=green)
        """
        queryset = super().get_queryset(request)
        return queryset.filter(url__status="green").annotate(sum_pageview=Sum('page_views__number_of_views')).order_by('sum_pageview')  

class SkippedUrlsAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('url', 'reason_for_skipping_url', 'step', 'user', 'action')
    actions = ("return_to_queue","redlist_urls", "clear_archive", "export_items_to_csv")
    search_fields = ('url',)
    list_filter = ("reason_for_skipping_url", )

    def get_list_display(self, request):
        if request.user.user_type == "annotator":
            return['url', 'step', 'reason', 'action']
        return super().get_list_display(request)

    def get_queryset(self, request):
        """
        Filter skipped tasks only
        """
        queryset = super().get_queryset(request)
        return queryset.filter(state="bad_url")

    def step(self, obj):
        return  obj.steps.last().step

    def action(self, obj):
        return format_html(
            f"""<a href="{obj.url.archived_url}" class="btn btn-success float-right" target="_blank" title="{obj.url.url}">View url</a>"""
            )
    def reason(self, obj):
        #Returns the reason the url was marked as bad
        bad_step = models.Step.objects.filter(task=obj, step="bad_url", task__mode="annotator").first()
        try:
            return bad_step.step_data["reason"]
        except Exception as e:
            return "-"

    def has_add_permission(self, request):
        #This is not an actual model, so we want to disable adding objects.
        return False

    def has_delete_permission(self, request):
        #This is not an actual model, so we want to disable deleting objects.
        return False

    def return_to_queue(self, request, queryset):
        queryset.update(state="in_progress", completed=False, reason_for_skipping_url="")

    def redlist_urls(self, request, queryset):
        for task in queryset:
            task.url.update(status="red")
            task.url.save()
    
    def clear_archive(self, request, queryset):
        """
        Useful for urls marked as bad due to faulty archive
        """
        for task in queryset:
            task.url.archived_url = ""
            task.url.save()
        self.message_user(
            request, f"Archives for selected urls has been cleared. These urls will return when re-archived", messages.INFO)

    
class ArchiveQueueAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('url', 'page_views','archive_attempt_count','status','priority')
    actions = ("remove_from_queue", "export_items_to_csv")
    search_fields = ('url',)

    def get_queryset(self, request):
        """
        This tab is to visualise the urls currently in queue
        """
        queryset = super().get_queryset(request)
        return queryset.filter(status="green", archived_url="")

    def has_add_permission(self, request):
        #This is not an actual model, so we want to disable adding objects.
        return False

    def has_delete_permission(self, request, *args):
        #Deleting an object here will be deleting the actual url. We don't want that
        return False

    def remove_from_queue(self, request, queryset):
        queryset.update(status="amber", priority=2)



class AnnotatorQueueAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False


class CountryAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('name', 'short_name')
    raw_id_fileds = ['urls']
    

class ClientAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('name', 'beeswax_green_list', 'beeswax_red_list' )

    def beeswax_green_list(self, obj):
        return obj.beeswax_list, obj.beeswax_list.greenlist_id if obj.beeswax_list else ''

    def beeswax_red_list(self, obj):
        return obj.beeswax_list, obj.beeswax_list.redlist_id if obj.beeswax_list else ''



class QueueRelationshipAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('queue', 'url', 'events',)
    raw_id_fields = ['url']
    actions = ["export_items_to_csv"]


    def url(self, obj):
        return obj.url.short_url

    def queue(self, obj):
        return str(obj)


class BeeswaxListAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('name', 'greenlist_id', 'redlist_id')
    # exclude = ['greenlist_id', 'redlist_id']
    actions = ["export_items_to_csv"]


@admin.register(models.ClientDomainRelationship)
class ClientDomainRelationshipAdmin(admin.ModelAdmin, ExportCsvMixin):
    form = ClientDomainRelationshipAdminForm
    
    search_fields = ['client__name', 'domain__domain']
    list_display = ('client', 'domain', 'status', )
    list_editable = ['status']
    list_filter = ['status', 'client']
    raw_id_fields = ("domain",)
    actions = ["export_items_to_csv"]


@admin.register(models.FacetProperty)
class FacetPropertyAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('entity_id','entity', 'facet', 'facet_type', 'entity_intent', 'facet_intent')
    raw_id_fields = ('entity', )
    actions = ["export_items_to_csv"]
    list_filter = (
                admin_filters.CustomDepartmentFilter, 
                admin_filters.CategoryListFilter, 
                admin_filters.SubCategoryListFilter, 
                admin_filters.SubSetListFilter,
                # "entity__department",
                # "entity__category",
                # "entity__subcategory",
                # "entity__subset",
                "facet", 
                "facet_type",
            )
    

@admin.register(models.UrlEditor)
class UrlEditorAdmin(admin.ModelAdmin):
    
    def changelist_view(self, request, extra_context=None):
        #Passing authentication token as context data to template to be picked up by javascript
        extra_context = extra_context or {}
        token, _ = Token.objects.get_or_create(user=request.user)
        request_scheme = "http" if settings.ENVIRONMENT == "dev" else "https"
        extra_context['base_url'] = f'{request_scheme}://{request.get_host()}/'
        extra_context['token'] = token
        request_scheme = "http" if settings.ENVIRONMENT == "dev" else "https"
        extra_context['base_url'] = f'{request_scheme}://{request.get_host()}/'
        return super(UrlEditorAdmin, self).changelist_view(request, extra_context=extra_context)


@admin.register(models.UrlScraped)
class ScrappedUrlAdmin(admin.ModelAdmin):
    search_fields = ("text",)


@admin.register(models.ExtensionVersion)
class ExtensionVersionAdmin(admin.ModelAdmin):
    list_display = ['version', 'created_at']
    search_fields = ['version']

@admin.register(models.TaskBreakdown)
class TaskBreakdownAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('user', "url", "products_selected", "grouped_entities", "product_list")
    list_filter = ("user", "date_completed")
    search_fields = ("url__url",)
    actions = ["export_items_to_csv"]

    def get_queryset(self, request):
        """
        This tab is to visualise task breakdowns
        """
        queryset = models.Task.objects.filter(state="completed", mode="annotator", completed=True, url__known=True)
        
        return queryset

    def products_selected(self, obj):
        return models.SelectedProduct.objects.filter(entity__url=obj.url).count()

    def grouped_entities(self, obj):
        return models.IntentData.objects.filter(url=obj.url).count()

    def product_list(self, obj):
        selected_products = models.SelectedProduct.objects.filter(entity__url=obj.url)
        return format_html(', '.join([f"<small>{p.product}({p.intent})</small>" for p in selected_products]))

    def has_add_permission(self, request):
        #This is not an actual model, so we want to disable adding objects.
        return False

@admin.register(models.DomainLog)
class DomainLogAdmin(admin.ModelAdmin):
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['base_url'] = f'{request.scheme}://{request.get_host()}/'
        return super(DomainLogAdmin, self).changelist_view(request, extra_context=extra_context)
        

@admin.register(models.DomainOverview)
class DomainOverviewAdmin(admin.ModelAdmin, ExportCsvMixin):
    search_fields = ['client__name', 'domain__domain']
    list_display = ('client', 'domain', 'page_views', 'approx_urls', 'beeswax_list')
    list_filter = ['status', 'client']
    raw_id_fields = ("domain",)
    actions = ["export_items_to_csv"]   

    def page_views(self, obj):
        return obj.domain.views

    def approx_urls(self, obj):
        return obj.domain.approximate_urls    
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('domain', 'client')

    def beeswax_list(self, obj):
        beeswax_list = obj.client.beeswax_list
        color = ''
        if beeswax_list:
            if beeswax_list.greenlist_id:
                color = 'green'
            elif beeswax_list.redlist_id:
                color = 'red'
        text = format_html(f'<span>{beeswax_list} <i style="color: {color};" class="fas fa-circle fa-xs"></i> </span>')
        return text if beeswax_list else beeswax_list

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_id','name','xpath','intent']


@admin.register(models.EntityFacetRelationship)
class EntityFacetRelationshipAdmin(admin.ModelAdmin):
    list_display = ['facet','entity','has_facet']


@admin.register(models.Entity)
class EntityAdmin(admin.ModelAdmin):
    list_display = ['avg_intent', 'all_products', 'all_facets', 'all_nodes']

    def all_products(self, obj):
        return "\n" + ", ".join([p.__str__() for p in obj.products.all()])

    def all_facets(self, obj):
        return "\n" + ", ".join([f.__str__() for f in obj.facets.all()])

    def all_nodes(self, obj):
        return "\n" + ", ".join([n.__str__() for n in obj.classification.all()])
    



admin.site.register(models.RawUrl, RawUrlAdmin)
admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.IntentData, IntentDataAdmin)
admin.site.register(models.AnnotationStats, AnnotationStatsAdmin)
admin.site.register(models.TBAQ, TBAQAdmin)
admin.site.register(models.SkippedUrl, SkippedUrlsAdmin)
admin.site.register(models.ArchiveQueue, ArchiveQueueAdmin)
admin.site.register(models.KnownUrls, KnownUrlsAdmin)
admin.site.register(models.AnnotatorQueue, AnnotatorQueueAdmin)
admin.site.register(models.Country, CountryAdmin)
admin.site.register(models.Client, ClientAdmin)
admin.site.register(models.QueueUrlRelationship, QueueRelationshipAdmin)
admin.site.register(models.BeeswaxList, BeeswaxListAdmin)
