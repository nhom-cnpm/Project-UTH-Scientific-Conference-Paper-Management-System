"""
Custom permissions cho accounts app
"""
from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Chỉ cho phép owner hoặc admin truy cập
    """
    def has_object_permission(self, request, view, obj):
        # Admin có thể truy cập tất cả
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        # Owner có thể truy cập
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        return obj == request.user


class IsAdminUser(permissions.BasePermission):
    """
    Chỉ admin mới có quyền
    """
    def has_permission(self, request, view):
        return request.user and (request.user.is_staff or request.user.is_superuser)


class IsChairOrAdmin(permissions.BasePermission):
    """
    Chair hoặc Admin
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        return (
            request.user.is_staff or 
            request.user.is_superuser or
            request.user.groups.filter(name__in=['Chair', 'Program Chair']).exists()
        )


class CanManageRoles(permissions.BasePermission):
    """
    Chỉ Chair/Admin mới có thể quản lý roles
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Safe methods (GET, HEAD, OPTIONS) - anyone can view
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Only Chair/Admin can modify
        return (
            request.user.is_staff or
            request.user.is_superuser or
            request.user.groups.filter(name__in=['Chair', 'Admin']).exists()
        )


class IsProfileOwner(permissions.BasePermission):
    """
    Chỉ chủ profile mới có thể sửa
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for owner
        return obj == request.user