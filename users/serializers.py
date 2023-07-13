from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from .models import DataPoint, Configuration, OrganizationObject, Project, ProjectTeam, TimeSeries
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
        fields = ["id", "first_name", "last_name", "email"]


class OrganizationObjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganizationObject
        fields = '__all__'


class DataPointSerializer(serializers.ModelSerializer):
    object = OrganizationObjectSerializer()

    class Meta:

        model = DataPoint
        fields = ["id", "name", "value", "project_name",
                  "object_name", "created_date", "object"]


class ConfigurationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Configuration
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'


class ProjectTeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectTeam
        fields = '__all__'


class TimeSeriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeSeries
        fields = '__all__'
