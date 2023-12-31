from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework import serializers

from users.models import (Configuration, DataPoint, Organization,
                          OrganizationObject, Project, ProjectTeam, TimeSeries)

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')

    def validate(self, data):
        user = User(**data)
        password = data.get('password')

        try:
            validate_password(password, user)
        except exceptions.ValidationError as e:
            serializer_errors = serializers.as_serializer_error(e)
            raise exceptions.ValidationError(
                {'password': serializer_errors['non_field_errors']}
            )
        return data

    def create(self, validate_data):
        user = User.objects.create_user(
            email=validate_data['email'],
            password=validate_data['password']
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']


class ConfigurationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Configuration
        fields = '__all__'


class OrganizationSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)

    class Meta:
        model = Organization
        fields = ['name', 'description', 'users']


class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    organization = OrganizationSerializer()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description',
                  'created_date', 'owner', 'organization']


class ProjectTeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectTeam
        fields = '__all__'


class OrganizationObjectSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()

    class Meta:
        model = OrganizationObject
        fields = ['id', 'name', 'description', 'project']


class DataPointSerializer(serializers.ModelSerializer):
    object = OrganizationObjectSerializer()

    class Meta:

        model = DataPoint
        fields = ['id', 'name', 'value', 'project_name',
                  'object_name', 'created_date', 'object']


class TimeSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSeries
        fields = '__all__'
