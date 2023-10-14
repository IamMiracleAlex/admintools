from typing import Optional, Dict
from rest_framework.authtoken.models import Token

from django.contrib import admin
from django.conf import settings

from .models import Subscription


class SubscriptionAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        #Passing authentication token as context data to template to be picked up by javascript
        extra_context = extra_context or {}
        token, _ = Token.objects.get_or_create(user=request.user)
        request_scheme = "http" if settings.ENVIRONMENT == "dev" else "https"
        extra_context['base_url'] = f'{request_scheme}://{request.get_host()}/'
        extra_context['token'] = token
        return super(SubscriptionAdmin, self).changelist_view(request, extra_context=extra_context)

admin.site.register(Subscription, SubscriptionAdmin)
