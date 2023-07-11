
from users.permissions import IsSimpleUser, IsAdmin
from .models import Configuration
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
from rest_framework import generics
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import OrganizationObject, DataPoint, Project, Configuration
from users.serializers import DataPointSerializer, UserCreateSerializer, ConfigurationSerializer, ProjectSerializer
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
User = get_user_model()


class RegisterView(APIView):
    def post(self, request):
        data = request.data

        serializer = UserCreateSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.create(serializer.validated_data)
        user = UserCreateSerializer(user)
        return Response(user.data, status=status.HTTP_201_CREATED)


class DataPointAPIList(generics.ListCreateAPIView):
    queryset = DataPoint.objects.all()
    serializer_class = DataPointSerializer

    def get(self, request):
        data = self.queryset.values_list('id', flat=True)
        return Response({'ids': data})

    def get(self, request, pk=None):
        # data = self.queryset.values_list('id', flat=True)
        return Response({'ids': 'data'})


@api_view(['GET'])
def get_datapoint_by_id(request, pk=None):
    target_date = datetime(2023, 7, 10, 12, 10, 12, 11)
    print(DataPoint.objects.filter(created_date__gte=target_date))
    print(DataPoint.objects.filter(id=930).first().value)
    print(target_date)
    obj = get_object_or_404(DataPoint, pk=pk)
    serializer = DataPointSerializer(obj)
    return Response(serializer.data)

# 2023-07-10 12:10:37.803000+00:00


class ProjectAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdmin | IsSimpleUser]


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

        return JsonResponse({'success': True, 'message': 'Configuration saved successfully.'})
