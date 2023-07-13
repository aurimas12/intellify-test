
from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import (Configuration, DataPoint, OrganizationObject,
                          Project, ProjectTeam, UserAccount)
from users.serializers import (ConfigurationSerializer, DataPointSerializer,
                               OrganizationObjectSerializer, ProjectSerializer,
                               UserCreateSerializer, UserSerializer)
from users.tasks import generate_data

User = get_user_model()


class UserAPIView(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all()
    serializer_class = UserCreateSerializer

    def post(self, request):
        data = request.data

        serializer = UserCreateSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.create(serializer.validated_data)
        user = UserCreateSerializer(user)
        return Response(user.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


class ProjectAPIView(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_serializer_class(self):
        project_team = get_object_or_404(
            ProjectTeam, user__email=self.request.user.email)
        if project_team.role == ProjectTeam.ROLE_SIMPLE_USER:
            return OrganizationObjectSerializer

        return super(ProjectAPIView, self).get_serializer_class()

    def get_queryset(self):
        project_team = get_object_or_404(
            ProjectTeam, user__email=self.request.user.email)
        if project_team.role == ProjectTeam.ROLE_MODERATOR:
            return Project.objects.filter(id=project_team.project.id)
        elif project_team.role == ProjectTeam.ROLE_SIMPLE_USER:
            return OrganizationObject.objects.filter(
                id=project_team.project.id)
        return super().get_queryset()


@permission_classes([IsAuthenticated, ])
@api_view(['GET'])
def get_project_by_user(request):
    user = get_object_or_404(UserAccount, pk=request.user.pk)
    project_team = ProjectTeam.objects.get(user=user)
    project_info = Project.objects.filter(pk=project_team.project.pk).values()
    return Response(project_info)


class DataPointAPIList(generics.ListCreateAPIView):
    queryset = DataPoint.objects.all()
    serializer_class = DataPointSerializer

    def get(self, request):
        data = self.queryset.values_list('id', flat=True)
        return Response({'ids': data})


@api_view(['GET'])
def get_datapoint_by_id(request, pk=None):
    obj = get_object_or_404(DataPoint, pk=pk)
    serializer = DataPointSerializer(obj)
    return Response(serializer.data)


class ConfigurationView(generics.ListCreateAPIView, generics.RetrieveUpdateAPIView):
    queryset = Configuration.objects.all()
    serializer_class = ConfigurationSerializer

    def post(self, request):
        config_data = request.POST.get('config_data')
        configuration, created = Configuration.objects.update_or_create(
            user=request.user,
            defaults={'data': config_data}
        )
        return Response({'success': True, 'message': 'Configuration saved successfully.'})


@api_view(['GET'])
def get_average(request):
    result = DataPoint.objects.aggregate(Avg('value'))
    return Response(result.values())


@api_view(['GET'])
def get_hourly(request, start_hour=None, hour_range=None):
    # Datapoint created on this date range 2023-07-10 - 2023-07-11
    start_h, end_h = 0, 0

    if start_hour == 24:
        start_h = 0
    elif start_hour > 24:
        return Response('Hour value must be in range 0 - 24')

    if start_hour+hour_range == 24:
        end_h = 0
    elif start_hour + hour_range > 24:
        end_h = start_hour + hour_range - 24
    else:
        end_h = start_hour + hour_range

    start_h = '2023-07-10 ' + str(start_hour) + ':00:00'
    end_h = '2023-07-10 ' + str(end_h) + ':00:00'

    result = DataPoint.objects.filter(
        created_date__range=[start_h, end_h]).aggregate(Avg('value'))
    return Response(result)


@api_view(['GET'])
def generate_data_auth_user(request):
    generate_data.delay(request.user.is_authenticated)
    return Response({'action': 'generate data'})
