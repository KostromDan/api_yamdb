from rest_framework.permissions import IsAuthenticated, SAFE_METHODS


class IsAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        return (super().has_permission(request, view)
                and (request.user.is_staff
                     or request.user.is_superuser
                     or request.user.role == 'admin'))


class IsAdminOrReadOnly(IsAdmin):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or super().has_permission(request, view))
