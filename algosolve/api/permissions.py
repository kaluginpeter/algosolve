from rest_framework import permissions


class CutsomBasePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return request.user == obj.author


class ProfilePermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return True
        return request.user.is_authenticated
