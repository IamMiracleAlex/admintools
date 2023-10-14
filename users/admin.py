from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.shortcuts import render
from django.http import HttpResponseRedirect

from rest_framework.authtoken.models import Token
from social_django.models import Association, Nonce, UserSocialAuth
from allauth.socialaccount.models import SocialToken, SocialAccount, SocialApp
from oauth2_provider.models import AccessToken, Application, Grant, RefreshToken
from django_celery_beat.models import SolarSchedule, ClockedSchedule

from users.custom_filters import GroupFilter
from users.models import User, ClientUser
from annotation.utils import ExportCsvMixin


@admin.register(User)
class CustomUserAdmin(UserAdmin, ExportCsvMixin):
    list_display = ('email', 'is_staff', 'is_active', 'user_type',)
    list_filter = ('is_staff', 'is_active', 'user_type', GroupFilter)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'user_type', 'queue'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser','user_type','groups')}

        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    actions = ["add_to_group", "export_items_to_csv"]

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['groups'] = Group.objects.all()
        return super(CustomUserAdmin, self).changelist_view(request, extra_context=extra_context)

    def add_to_group(self, request, queryset):   
        # POST request
        if "grp" in request.POST:
            try:
                group = Group.objects.get(pk=request.POST.get("grp"))
                for user in queryset:
                    user.groups.clear() # I need to do this so the user doesn't get added to multipple groups
                    group.user_set.add(user)
                self.message_user(request,
                    "Added {} user(s) to the {} group".format(queryset.count(), group.name))
                return HttpResponseRedirect(request.get_full_path())
            except ValueError:
                self.message_user(request, "Invalid group selected. Select a group to assign user(s) to")
        return HttpResponseRedirect(request.get_full_path())

@admin.register(ClientUser)
class CLientUserAdmin(admin.ModelAdmin):
    list_display = ("user", "client", "is_admin")

    
# Remove these third party apps from the admin because it is unneccessary/
# exposes user's authentication tokens.    
admin.site.unregister(Token)
admin.site.unregister(Association)
admin.site.unregister(Nonce)
admin.site.unregister(UserSocialAuth)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialToken)
admin.site.unregister(SocialApp)
admin.site.unregister(AccessToken)
admin.site.unregister(Application)
admin.site.unregister(Grant)
admin.site.unregister(RefreshToken)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)