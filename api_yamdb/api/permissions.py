from rest_framework.permissions import IsAuthenticated


class IsAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        super(IsAdmin, self).has_permission(request, view)
        return (super(IsAdmin, self).has_permission(request, view)
                and (request.user.is_staff
                     or request.user.is_superuser
                     or request.user.role == 'admin'))
