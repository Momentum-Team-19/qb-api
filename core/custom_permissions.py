from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # If it's a read-only method, allow access
        if request.method in permissions.SAFE_METHODS:
            return True
        # For other methods, only allow if user is authenticated
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow read-only methods for all
        if request.method in permissions.SAFE_METHODS:
            return True
        # For other methods, only allow if user is the author
        return obj.author == request.user
