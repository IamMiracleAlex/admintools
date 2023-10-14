from django.contrib import admin

from custom_admin.models import BulkEdit, FacetBulkEdit, DataRelease
from custom_admin.forms import ClassificationEditorForm, FacetBulkEditForm


@admin.register(BulkEdit)
class BulkEditAdmin(admin.ModelAdmin):
    change_list_template = "bulk-edit.html"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['form'] = ClassificationEditorForm()
        return super(BulkEditAdmin, self).changelist_view(request, extra_context=extra_context)


@admin.register(FacetBulkEdit)
class FacetBulkEditAdmin(admin.ModelAdmin):
    change_list_template = "facet_bulk_edit.html"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['form'] = FacetBulkEditForm()
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(DataRelease)
class DataReleaseAdmin(admin.ModelAdmin):
    change_list_template = "data-release.html"