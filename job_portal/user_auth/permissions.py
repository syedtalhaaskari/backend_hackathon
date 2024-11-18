from rest_framework.request import Request
from rest_framework.permissions import BasePermission

class ProfilePermission(BasePermission):
    def has_permission(self, request: Request, view):
        if request.method == 'GET':
            return True
        if request.method == 'POST':
            return False
        return True
    
    def has_object_permission(self, request: Request, view, obj):
        if request.method in ['GET']:
            return True
        if request.user.id == obj.user.id and request.method in ['PUT', 'PATCH']:
            return True

        if request.user.id == obj.user.id or request.user.is_superuser:
            return True

        return False