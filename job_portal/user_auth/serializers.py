from django.contrib.auth.models import User
from rest_framework import serializers

from .models import JobSeeker, Employer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "password",
            "last_login",
            "is_superuser",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "is_active",
            "date_joined",
            "groups",
        ]
        extra_kwargs = {
            'is_superuser': {'read_only': True},
            'is_staff': {'read_only': True},
            'is_active': {'read_only': True},
            'last_login': {'read_only': True},
            'date_joined': {'read_only': True},
            'password': {'write_only': True},
        }

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {
            'username': {'write_only': True},
            'password': {'write_only': True},
        }

class JobSeekerSerializer(serializers.ModelSerializer):
    http_method_names = ('GET', 'DELETE', 'PUT')
    class Meta:
        model = JobSeeker
        fields = '__all__'

class EmployerSerializer(serializers.ModelSerializer):
    http_method_names = ('GET', 'DELETE', 'PUT')
    class Meta:
        model = Employer
        fields = '__all__'