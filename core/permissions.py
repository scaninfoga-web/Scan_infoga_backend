from rest_framework.permissions import BasePermission

class IsAdminUserType(BasePermission):
    def has_permission(self, request, view):
        token = get_token_from_header(request)
        user = get_user_from_token(token)
        return request.user.is_authenticated and getattr(request.user, 'user_type', '') == 'ADMIN'