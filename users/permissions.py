from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from users.models import ProjectTeam, UserAccount


def user_project_info(account):
    is_user = account.user == get_object_or_404(
        UserAccount, pk=account.user.pk)

    project_team = ProjectTeam.objects.get(
        user__email=account.user.email)

    return is_user, project_team


class IsAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        is_user, project_team = user_project_info(request)
        return bool(is_user and project_team.role == ProjectTeam.ROLE_ADMIN)


class IsModerator(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        is_user, project_team = user_project_info(request, obj)
        return bool(is_user and project_team.role == ProjectTeam.ROLE_MODERATOR)


class IsSimpleUser(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        is_user, project_team = user_project_info(request, obj)
        return bool(is_user and project_team.role == ProjectTeam.ROLE_SIMPLE_USER)
