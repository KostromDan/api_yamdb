from rest_framework.permissions import BasePermissionы


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_staff
                or request.user.is_superuser
                or request.user.role == 'admin')
