from rest_framework.permissions import BasePermission

from accounts.models import UserRole


class IsStaff(BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user.is_staff
    

class IsOwner(BasePermission):
    """
    Allow access to user relations such as notifications.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user.id == request.user.id
    

class IsSelfOrStaff(BasePermission):
    """
    Custom permission to allow access to the user's details
    """
    def has_object_permission(self, request, view, obj):
        return obj.email == request.user.email or request.user.is_staff
    

class IsSeller(BasePermission):
    """
    Regulate modifications and deletions on objects
    """
    def has_object_permission(self, request, view, obj):
        return obj.seller.id == request.user.id
    

class IsFarmer(BasePermission):
    """
    Regulate modifications and deletions on objects
    """
    def has_permission(self, request, view):
        return request.user.role == UserRole.FARMER
