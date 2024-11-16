from rest_framework.request import Request
from rest_framework.permissions import BasePermission

from user_auth.models import Employer

class IsOwner(BasePermission):
    def has_permission(self, request: Request, view):
        return request.user.groups.filter(name = 'Employer').exists() or request.user.is_superuser
    
    def has_object_permission(self, request: Request, view, obj):
        return obj.job_post.user.id == request.user.id
    
class IsOwnerOrAdmin(BasePermission):
    def has_permission(self, request: Request, view):
        return request.user.groups.filter(name = 'Employer').exists() or request.user.is_superuser
    
    def has_object_permission(self, request: Request, view, obj):
        if request.method in ('GET', 'DELETE'):
            return obj.job_post.user.id == request.user.id or request.user.is_superuser
        return obj.job_post.user.id == request.user.id

class IsJobSeeker(BasePermission):
    def has_permission(self, request: Request, view):
        return request.user.groups.filter(name = 'Job_Seeker').exists()
    
    def has_object_permission(self, request: Request, view, obj):
        return request.user.groups.filter(name = 'Job_Seeker').exists()

class JobPostPermissions(BasePermission):
    def has_permission(self, request: Request, view):
        if request.method == 'GET':
            return True
        if request.user.groups.filter(name = 'Employer').exists() or request.user.is_superuser:
            return True
        else:
            return False
    
    def has_object_permission(self, request: Request, view, obj):
        if request.method == 'GET':
            return True
        if (request.method == 'PUT' or request.method == 'PATCH') and request.user.groups.filter(name = 'Employer').exists() and request.user.id == obj.user_id:
            return True
        return (request.user.groups.filter(name = 'Employer').exists() and request.user.id == obj.user_id) or request.user.is_superuser

class PostPermissions(BasePermission):
    def has_permission(self, request: Request, view):
        if request.method == 'GET':
            return request.user.is_authenticated
        
        if request.user.groups.filter(name__in = ('Superuser', 'Moderator', 'Author')).exists() or request.user.is_superuser:
            return True
        
        return False
    
    def has_object_permission(self, request: Request, view, obj):
        if request.method == 'GET':
            return request.user.is_authenticated
        if request.user.groups.filter(name='Author').exists():
            if obj.owner_id == request.user.id or obj.authors.filter(id=request.user.id):
                return True

        if request.method == 'PUT' or request.method == 'PATCH':
            return False

        if request.user.groups.filter(name__in = ('Superuser', 'Moderator')).exists() or request.user.is_superuser:
            return True

        return False
    
class CommentPermissions(BasePermission):
    def has_permission(self, request: Request, view):
        if request.method == 'GET':
            return request.user.is_authenticated
        
        if request.user.groups.filter(name__in = ('Superuser', 'Moderator', 'Author')).exists() or request.user.is_superuser:
            return True
        
        return False
    
    def has_object_permission(self, request: Request, view, obj):
        if request.method == 'GET':
            return request.user.is_authenticated

        if request.user.groups.filter(name='Author').exists() and obj.user.id == request.user.id:
            return True

        if request.method == 'PUT' or request.method == 'PATCH':
            return False

        if request.user.groups.filter(name__in = ('Superuser', 'Moderator')).exists() or request.user.is_superuser:
            return True

        return False
    
class LikePermissions(BasePermission):
    def has_permission(self, request: Request, view):
        if request.method == 'GET':
            return request.user.is_authenticated
        
        if request.user.groups.filter(name__in = ('Superuser', 'Moderator', 'Author')).exists() or request.user.is_superuser:
            return True
        
        return False
    
    def has_object_permission(self, request: Request, view, obj):
        if request.method == 'GET':
            return request.user.is_authenticated

        if request.user.groups.filter(name='Author').exists() and obj.user.id == request.user.id:
            return True

        if request.method == 'PUT' or request.method == 'PATCH':
            return False

        if request.user.groups.filter(name__in = ('Superuser', 'Moderator')).exists() or request.user.is_superuser:
            return True

        return False