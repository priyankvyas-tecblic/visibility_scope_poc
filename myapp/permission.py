from rest_framework import permissions
from django.db.models import Q
from django.db.models.query import EmptyQuerySet
from myapp.models import SpecificPermission


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

class CheckSpecificPermission(permissions.BasePermission):
    permission_class = SpecificPermission()
    for i in permission_class.get_deferred_fields():
        print('i: ', i)
    # role_permission_mapping = {"operational_head":"", "zonal_head":zone_fk, "state_coordinator":state_fk, "asset_monitoring_officer":district_fk, "area_manager":premise_fk, "warehouse_supervisor":warehouse_fk}
    
    def has_object_permission(self, request, view, obj):
        user_role = request.user.user_role    
        specific_permission = request.user.specific_permissions.filter(Q(warehouse_fk=obj))
        if specific_permission is EmptyQuerySet:
            return False
        
        return True