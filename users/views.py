
from .tasks import generate_data
from users.permissions import IsSimpleUser, IsAdmin
from .models import Configuration, ProjectTeam
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from datetime import datetime
from os import truncate
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.db.models import Avg
from sqlite3 import Timestamp
from rest_framework.views import APIView
from rest_framework import generics, viewsets
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import OrganizationObject, DataPoint, Project, Configuration, UserAccount, ProjectTeam
from users.serializers import DataPointSerializer, ProjectTeamSerializer, UserCreateSerializer, ConfigurationSerializer, ProjectSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
User = get_user_model()


# GET agregated timeseries by data point hourly,
# GET agregated timeseries by data point daily
# GET agregated timeseries by data point monthly


# GET all users
# POST create user
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


# GET projects
# GET projects by Project id
class ProjectAPIView(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    # permission_classes = [IsAdmin | IsSimpleUser]

# GET projects by User


@permission_classes([IsAuthenticated, ])
@api_view(['GET'])
def get_project_by_user(request):
    user = get_object_or_404(UserAccount, pk=request.user.pk)
    project_team = ProjectTeam.objects.get(user=user)
    project_info = Project.objects.filter(pk=project_team.project.pk).values()

    return Response(project_info)


# GET  all datapoint ids
# POST user can create datapoint
class DataPointAPIList(generics.ListCreateAPIView):
    queryset = DataPoint.objects.all()
    serializer_class = DataPointSerializer

    def get(self, request):
        data = self.queryset.values_list('id', flat=True)
        return Response({'ids': data})


# GET  datapoint by id
@api_view(['GET'])
def get_datapoint_by_id(request, pk=None):
    obj = get_object_or_404(DataPoint, pk=pk)
    serializer = DataPointSerializer(obj)
    return Response(serializer.data)


# POST store configuration in json format
# PUT edit configuration json
class ConfigurationView(generics.ListCreateAPIView, generics.RetrieveUpdateAPIView):  # not working
    queryset = Configuration.objects.all()
    serializer_class = ConfigurationSerializer

    def post(self, request):
        # Retrieve data from the request body
        config_data = request.POST.get('config_data')

        # Create or update the configuration
        configuration, created = Configuration.objects.update_or_create(
            user=request.user,
            defaults={'data': config_data}
        )

        return Response({'success': True, 'message': 'Configuration saved successfully.'})


# agregated datapoints
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


# Generated  timeseries data
@api_view(['GET'])
def generate_data_auth_user(request):
    generate_data.delay(request.user.email)

    return Response({'action': 'generate data'})
