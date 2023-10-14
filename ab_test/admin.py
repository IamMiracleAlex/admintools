from django.contrib import admin

from users.models import User
from ab_test.models import TestInProgress, TestResult, TestSetup


class TestSetupAdmin(admin.ModelAdmin):
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['users'] = User.objects.all()
        return super(TestSetupAdmin, self).changelist_view(request, extra_context=extra_context)

admin.site.register(TestSetup, TestSetupAdmin)
admin.site.register(TestInProgress)
admin.site.register(TestResult)
