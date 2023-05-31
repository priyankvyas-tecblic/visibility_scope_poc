from rest_framework import permissions

class RolePermission(permissions.BasePermission):
    
    def has_permission(self, request, view, rank):
        if request.user.user_role <= rank:
            return True
        return False
    
class OperationalHeadPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.user_role is "operational_head":
            return True
        return False

class ZonePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.user_role in ["zonal_head", "operational_head"]:
            return True
        return False

    # def has_object_permission(self, request, view, obj):
    #     # Read permissions are allowed to any request,
    #     # so we'll always allow GET, HEAD or OPTIONS requests.
    #     if request.method in permissions.SAFE_METHODS:
    #         return True
    #     print("in has object permission")

    #     # Instance must have an attribute named `owner`.
    #     return obj.owner == request.user
    
class StatePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.user_role in ["state_coordinator", "zonal_head", "operational_head"]:
            return True
        return False
    
class DistrictPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.user_role in ["asset_monitoring_officer", "state_coordinator", "zonal_head", "operational_head"]:
            return True
        return False

class ClusterPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.user_role in ["area_manager", "asset_monitoring_officer", "state_coordinator", "zonal_head", "operational_head"]:
            return True
        return False
    
class PremisePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.user_role in ["warehouse_supervisor", "area_manager", "asset_monitoring_officer", "state_coordinator", "zonal_head", "operational_head"]:
            return True
        return False
    
class WarehousePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.user_role in ["warehouse_supervisor", "area_manager", "asset_monitoring_officer", "state_coordinator", "zonal_head", "operational_head"]:
            return True
        return False
    
class CheckSpecificPermission(permissions.BasePermission):
    role_permission_mapping = {"operational_head":OperationalHeadPermission(), "zonal_head":ZonePermission(), "state_coordinator":StatePermission(), "asset_monitoring_officer":DistrictPermission(), "area_manager":PremisePermission(), "warehouse_supervisor":WarehousePermission()}
    role_wise_parent = {"zonal_head":5, "state_coordinator":4, "asset_monitoring_officer":3, "area_manager":2, "warehouse_supervisor":1}
    
    def has_object_permission(self, request, view, obj):
        user_role = request.user.user_role
        if user_role is "operational_head":
            return True
        if self.role_permission_mapping.get(user_role).has_permission(request) is False:
            return False

        specific_permission = request.user.specific_permissions.all()
        warehouse_obj = obj
        if obj is None:
            return False
        for _ in range(self.role_wise_parent.get(user_role)+1):
            warehouse_obj = warehouse_obj.fk
            if warehouse_obj in specific_permission:
                return True

        return False