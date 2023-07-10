
from .models import Configuration
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
import datetime
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


class RetrieveUserView(APIView):
    def get(self, request):
        objects = OrganizationObject.objects.all()
        projects = Project.objects.all()
        print(len(objects), projects[0].title)
        # DataPoint.objects.create({
        #     'name': 'demo', 'object': objects[0], 'value': 12, 'project name': projects[0].title, 'project object': objects[0].name
        # })
        # c = DataPoint(
        #     name='demo1', object=objects[0], value=12, project_name=projects[0].title, object_name=objects[0].name, created_date='2023-09-13 15:35:12.559642'
        # )
        # c.save()

        import random
        print(random.uniform(1.0, 100.0))
        import pandas as pd
        from datetime import datetime

        datelist = pd.date_range(datetime.today(), periods=300).tolist()

        print(datelist[0])
        count = 0
        # obj1 = objects[:3]
        obj2 = objects[3:]
        for o in obj2:
            for d in datelist:
                val = random.uniform(1.0, 100.0)
                c = DataPoint(
                    name='test ' + o.name + ' ' + str(count), object=o, value=val, project_name=projects[1].title, object_name=o.name, created_date=datelist
                )
                c.save()
                count += 1
                if count == 100:
                    count = 0
                    break

        return Response({'data': 123}, status=status.HTTP_200_OK)


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
    obj = get_object_or_404(DataPoint, pk=pk)
    serializer = DataPointSerializer(obj)
    return Response(serializer.data)


@api_view(['GET'])
def get_aggregate_data(request, pk=None):
    # obj = get_object_or_404(DataPoint, pk=pk)
    # serializer = DataPointSerializer(obj)
    # print(DataPoint.objects.aggregate(Avg('value'))) #average value time series

    d = DataPoint.objects.filter(created_date__gt='2023-07-10 12:10:37')
    print(len(d), d)
    return Response({'fd': "serializer.data"})


# 2023-07-10 12:10:37.803371+00:00
# 2023-07-10 17:35:25.450812+00:00

class ProjectAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


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
