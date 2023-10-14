from django.contrib import admin

from annotation import models
from annotation import admin_mixins as mixins


class CustomDepartmentFilter(admin.SimpleListFilter):
    title = 'department'
    parameter_name = 'department'

    def lookups(self, request, model_admin):
        intent_data_queryset = models.IntentData.objects.order_by('-department')\
            .values('department').distinct()
        return (
            (depatment['department'],)*2 for depatment in intent_data_queryset
        )
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(entity__department__exact=self.value())


class CategoryListFilter(mixins.CategoryFilterMixin, admin.SimpleListFilter):
    title = ('category')
    parameter_name = 'category'

    def lookups(self, request, model_admin):
        department = request.GET.get('department')
        intentdata_qs = models.IntentData.objects.all()
        
        if department:
            intentdata_qs = intentdata_qs.filter(department=department)

        categories = intentdata_qs.values('category').order_by('category').distinct()

        return  ((category['category'],)*2 for category in categories)


class SubCategoryListFilter(mixins.SubCategoryFilterMixin, admin.SimpleListFilter):
    title = ('subcategory')
    parameter_name = 'subcategory'

    def lookups(self, request, model_admin):
        category = request.GET.get('category')
        intentdata_qs = models.IntentData.objects.all()

        if category:
            intentdata_qs = intentdata_qs.filter(category=category)
        
        subcategories = intentdata_qs.values('subcategory').order_by('subcategory').distinct()

        return ((subcategory['subcategory'],)*2 for subcategory in subcategories)


class SubSetListFilter(mixins.SubsetFilterMixin, admin.SimpleListFilter):
    title = ('subset')
    parameter_name = 'subset'

    def lookups(self, request, model_admin):
        subcategory = request.GET.get('subcategory')
        intentdata_qs = models.IntentData.objects.all()
        
        if subcategory:
            intentdata_qs = intentdata_qs.filter(subcategory=subcategory)

        subsets = intentdata_qs.values('subset').order_by('subset').distinct()

        return ((subset['subset'],)*2 for subset in subsets)
