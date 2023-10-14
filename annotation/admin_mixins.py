from django.contrib import admin

from annotation import models


class CategoryFilterMixin:
    def queryset(self, request, queryset):
        if queryset:
            model_name = queryset.model.__name__
            if model_name == models.FacetProperty.__name__:
                if self.value():
                    queryset = queryset.filter(entity__category__exact=self.value())
            
            if model_name == models.IntentData.__name__:
                department = request.GET.get('department', '')

                if self.value() or (department and self.value()):
                    queryset = queryset.filter(category=self.value())
        return queryset


class SubCategoryFilterMixin:
    def queryset(self, request, queryset):
        if queryset:
            model_name = queryset.model.__name__
            if model_name == models.FacetProperty.__name__:
                if self.value():
                    queryset = queryset.filter(entity__subcategory__exact=self.value())
            
            if model_name == models.IntentData.__name__:
                category = request.GET.get('category', '')
                if self.value() or (category and self.value()):
                    queryset = queryset.filter(subcategory=self.value())
        return queryset


class SubsetFilterMixin:
    def queryset(self, request, queryset):
        if queryset:
            model_name = queryset.model.__name__
            if model_name == models.FacetProperty.__name__:
                if self.value():
                    queryset = queryset.filter(entity__subset__exact=self.value())
            
            if model_name == models.IntentData.__name__:
                subset = request.GET.get('subset', '')
                if self.value() or (subset and self.value()):
                    queryset = queryset.filter(subset=self.value())
        return queryset