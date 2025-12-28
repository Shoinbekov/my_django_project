from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_staff


class IsOwner(permissions.BasePermission):
    """
    Доступ только владельцу объекта.
    Если пользователь не авторизован → 401, а не 403.
    """

    def has_permission(self, request, view):
        # Если не авторизован → возвращаем False для IsAuthenticated
        # но не поднимаем 403 сами
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
