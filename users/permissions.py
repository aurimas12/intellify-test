from rest_framework import permissions
from .models import ProjectTeam, UserAccount
from django.shortcuts import get_object_or_404


class IsAdmin(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        is_user = request.user == get_object_or_404(
            UserAccount, pk=request.user.pk)

        user = ProjectTeam.objects.filter(
            project__pk=obj.pk, user__email=request.user.email)

        if user:
            user_role = user[0].role
        else:
            return False

        return bool(is_user and user_role == ProjectTeam.ROLE_ADMIN)


class IsModerator(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        is_user = request.user == get_object_or_404(
            UserAccount, pk=request.user.pk)

        user = ProjectTeam.objects.filter(
            project__pk=obj.pk, user__email=request.user.email)

        if user:
            user_role = user[0].role
        else:
            return False

        return bool(is_user and user_role == ProjectTeam.ROLE_MODERATOR)


class IsSimpleUser(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        is_user = request.user == get_object_or_404(
            UserAccount, pk=request.user.pk)

        user = ProjectTeam.objects.filter(
            project__pk=obj.pk, user__email=request.user.email)

        if user:
            user_role = user[0].role
        else:
            return False

        return bool(is_user and user_role == ProjectTeam.ROLE_SIMPLE_USER)
