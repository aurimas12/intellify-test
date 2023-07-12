from rest_framework import permissions
from .models import ProjectTeam, UserAccount
from django.shortcuts import get_object_or_404


def is_user_info(account, obj):
    is_user = account.user == get_object_or_404(
        UserAccount, pk=account.user.pk)

    user = ProjectTeam.objects.filter(
        project__pk=obj.pk, user__email=account.user.email)
    return is_user, user


class IsAdmin(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        is_user, user = is_user_info(request, obj)
        if user:
            user_role = user[0].role
        else:
            return False

        return bool(is_user and user_role == ProjectTeam.ROLE_ADMIN)


class IsModerator(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        is_user, user = is_user_info(request, obj)
        if user:
            user_role = user[0].role
        else:
            return False

        return bool(is_user and user_role == ProjectTeam.ROLE_MODERATOR)


class IsSimpleUser(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        is_user, user = is_user_info(request, obj)
        if user:
            user_role = user[0].role
        else:
            return False

        return bool(is_user and user_role == ProjectTeam.ROLE_SIMPLE_USER)
