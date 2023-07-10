from rest_framework import permissions
from .models import OrganizationProject


# class IsAdmin(permissions.IsAuthenticated):
#     def has_object_permission(self, request, view, obj):
#         user_role = OrganizationProject.objects.filter(user=request.user).role
#         return bool(request.user == obj.user and request.user.is_staff and user_role == OrganizationProject.ROLE_ADMIN)


# class IsModerator(permissions.IsAuthenticated):
#     def has_object_permission(self, request, view, obj):
#         user_role = OrganizationProject.objects.filter(user=request.user).role
#         return bool(request.user == obj.user and user_role == OrganizationProject.ROLE_MODERATOR)


# class IsSimpleUser(permissions.IsAuthenticated):
#     def has_object_permission(self, request, view, obj):
#         user_role = OrganizationProject.objects.filter(user=request.user).role
#         return bool(request.user == obj.user and user_role == OrganizationProject.ROLE_SIMPLE_USER)
