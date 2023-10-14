from django.contrib import admin
from django.utils import timezone
from django.conf import settings
from rest_framework.authtoken.models import Token

from simple_history.admin import SimpleHistoryAdmin

from classification import models
from classification.utils import is_allowed
from annotation.utils import ExportCsvMixin


@admin.register(models.TaxonomyEditor)
class TaxonomyEditorAdmin(admin.ModelAdmin):
    
    def changelist_view(self, request, extra_context=None):
        #Passing authentication token as context data to template to be picked up by javascript
        extra_context = extra_context or {}
        added_context = get_added_context(request)
        extra_context.update(added_context)
        token, _ = Token.objects.get_or_create(user=request.user)
        extra_context['token'] = token
        extra_context['has_write_access'] = is_allowed(request.user, group_names=['taxonomy', 'annotator-taxonomist'])
        extra_context['email_verified'] = request.user.is_verified_for_ses
        request_scheme = "http" if settings.ENVIRONMENT == "local" else "https"
        extra_context['base_url'] = f'{request_scheme}://{request.get_host()}/'
        return super(TaxonomyEditorAdmin, self).changelist_view(request, extra_context=extra_context)

@admin.register(models.TaxonomyFeed)
class TaxonomyFeedAdmin(admin.ModelAdmin):
    
    def changelist_view(self, request, extra_context=None):
        #Passing authentication token as context data to template to be picked up by javascript
        extra_context = extra_context or {}
        token, _ = Token.objects.get_or_create(user=request.user)
        extra_context['token'] = token
        request_scheme = "http" if settings.ENVIRONMENT == "dev" else "https"
        extra_context['base_url'] = f'{request_scheme}://{request.get_host()}/'
        return super(TaxonomyFeedAdmin, self).changelist_view(request, extra_context=extra_context)

@admin.register(models.FacetCategory)
class FacetCategoryAdmin(SimpleHistoryAdmin):
    pass

@admin.register(models.FacetValue)
class FacetValueAdmin(SimpleHistoryAdmin, ExportCsvMixin):
    list_display = ("category", "label", "description")
    actions = ("delete_without_confirmation", "export_items_to_csv")
    search_fields = ("label",)
    list_filter = ("category",)

    def delete_without_confirmation(self, request, queryset):
        """
        default implementation fails because too may rows are affected.
        We override to skip the confirmation screen
        """
        queryset.delete()

@admin.register(models.NodeFacetRelationship)
class NodeFacetRelationshipAdmin(SimpleHistoryAdmin, ExportCsvMixin):
    list_display = ("node", "facet", "has_facet")
    actions = ("delete_without_confirmation", "export_items_to_csv")
    search_fields = ("node__title", "facet__label")

    def delete_without_confirmation(self, request, queryset):
        """
        default implementation fails because too may rows are affected.
        We override to skip the confirmation screen
        """
        queryset.delete()

@admin.register(models.Node)
class NodeAdmin(SimpleHistoryAdmin):
    list_display = ("title", "parent", "status", "description")
    search_fields = ("title",)
    actions = ["export_items_to_csv"]

    def delete_selected(self, request, queryset):
       queryset.update(status='deleted')

    actions = ["delete_selected"]


@admin.register(models.DeletedNode)
class DeletedNodeAdmin(admin.ModelAdmin):
    list_display = ("title", "parent", "date_deleted", "days_remaining")
    actions = ("restore",)

    def get_queryset(self, request):
        return models.Node.objects.deleted()

    def days_remaining(self, obj):
        delta = timezone.now() - obj.updated_at
        return 30 - delta.days

    def restore(self, request, queryset):
        queryset.update(status="active")

    def date_deleted(self, obj):
        return obj.updated_at

    def has_add_permission(self, request, obj=None):
        #Disable add button
        return False

@admin.register(models.SKUMapper)
class SKUMapperAdmin(admin.ModelAdmin):
    list_display = ('client', 'product_name', 'manufacturer', 'description', 'hierarchy_mapping')


@admin.register(models.SKUMapperEditor)
class SKUMapperEditorAdmin(admin.ModelAdmin):
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        # we need some added context for the react app to use
        # base_url, auth and others
        added_context = get_added_context(request)
        # concatenate it with the extra_context if any
        extra_context.update(added_context)
        return super(SKUMapperEditorAdmin, self).changelist_view(request, extra_context=extra_context)


def get_added_context(request):
    context = {}
    try:
        token, _ = Token.objects.get_or_create(user=request.user)
        context['token'] = token
        context['has_write_access'] = is_allowed(request.user, group_names=['taxonomy', 'annotator-taxonomist'])
        context['email_verified'] = request.user.is_verified_for_ses
        request_scheme = "http" if settings.ENVIRONMENT == "local" else "https"
        context['base_url'] = f'{request_scheme}://{request.get_host()}/'
    except Exception as e:
        pass
    return context

@admin.register(models.Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name',)