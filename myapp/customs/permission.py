from rest_framework import permissions

class ZonePermission(permissions.BasePermission):
    message = 'Zone permission not allowed.'

    def has_permission(self, request, view):
        return request.user.has_perm('myapp.view_zone')

    # def has_object_permission(self, request, view, obj):
    #     # Read permissions are allowed to any request,
    #     # so we'll always allow GET, HEAD or OPTIONS requests.
    #     if request.method in permissions.SAFE_METHODS:
    #         return True
    #     print("in has object permission")

    #     # Instance must have an attribute named `owner`.
    #     return obj.owner == request.user
