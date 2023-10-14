from rest_framework import permissions
from users.models import ClientUser

class IsStaffPermission(permissions.BasePermission):
    message = "Only an admin can perform this operation"

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        else:
            return request.user.is_staff


class IsClientAdminPermission(permissions.BasePermission):
    message = "Only client admins can perform this operation"

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        else:
            client_user = ClientUser.objects.get(user=request.user)
            return request.user.user_type == "client" and client_user.is_admin 
