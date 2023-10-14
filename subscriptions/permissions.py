from rest_framework import permissions
from users.models import ClientUser

class ClientPermission(permissions.BasePermission):

    """ Only Superusers and Client users can access this resource"""
    
    def has_object_permission(self, request, view, obj):
        if request.user.user_type == "client":
            client_user = ClientUser.objects.get(user = request.user)
            if request.method in ["PUT", "PATCH"]:
                return client_user.client == obj and client_user.is_admin
            else:
                return client_user.client == obj
        else:
            return request.user.is_superuser
        