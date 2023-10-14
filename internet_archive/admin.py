from django.contrib import admin

from internet_archive.models import ArchiveSetting


@admin.register(ArchiveSetting)
class ArchiveSettingAdmin(admin.ModelAdmin):
    list_display = ['archive_method', 'number_of_urls']

    def has_add_permission(self, request):
        # Don't allow more than one object.
        if self.model.objects.count() >= 1:
            return False
        else:
            return True


