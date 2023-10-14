from django.contrib import admin
from custom_logger.models import RequestLog, ChromeExtensionLog
from django.utils.html import format_html

@admin.register(RequestLog)
class LogAdmin(admin.ModelAdmin):

    list_display = ('user','time', 'duration','colored_url','request_method', 'response_status', 'short_response_body')
    list_filter = ('response_status', 'request_method', 'user')

    def colored_url(self, instance):
        """
        Colour code by response code for easy identification
        """
        if instance.response_status:
            response_status = int(instance.response_status)
            if response_status < 300:
                color = 'green'
            else:
                color = 'red'
        else:
            color = 'red'

        return format_html(f'<span style="color: {color};">{instance.request_url}</span>')

    colored_url.short_description = 'Endpoint'

    def get_readonly_fields(self, request, obj=None):
        """
        Make all fields read only
        """
        return [f.name for f in self.model._meta.get_fields()]


@admin.register(ChromeExtensionLog)
class ChromeExtensionLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'traceback', 'created_at']
    list_filter = ('user', 'created_at')

    def get_readonly_fields(self, request, obj=None):
        """
        Make all fields read only
        """
        return [f.name for f in self.model._meta.get_fields()]
