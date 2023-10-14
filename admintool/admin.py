from django.contrib import admin

from admintool.models import DataStatus, Status


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass


@admin.register(DataStatus)
class DataStatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'value', 'date']
    list_filter = ['name']
    search_fields = ['name']
