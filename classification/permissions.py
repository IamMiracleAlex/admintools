from rest_framework.permissions import BasePermission, SAFE_METHODS
from .utils import is_allowed
from django.conf import settings

class TaxonomistOrReadOnly(BasePermission):
    """
    Object level permission to allow only certain types of users have 
    access to the complete actions on a particular Object
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        has_perm = bool (
                request.user and
                is_allowed(request.user, group_names=['taxonomy','annotator-taxonomist' ]) and
                request.user.is_authenticated
            )
        if settings.ENVIRONMENT == "prod": 
            return bool(has_perm)
        else:
            return any([has_perm, request.user.is_superuser])

  