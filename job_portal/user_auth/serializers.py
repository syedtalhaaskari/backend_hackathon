from django.contrib.auth.models import User
from rest_framework import serializers

from .models import JobSeeker, Employer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
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
            'id': {'read_only': True},
            'is_superuser': {'read_only': True},
            'is_staff': {'read_only': True},
            'is_active': {'read_only': True},
            'last_login': {'read_only': True},
            'date_joined': {'read_only': True},
            'password': {'write_only': True},
        }

class SignUpSerializer(serializers.ModelSerializer):
    role = serializers.CharField()

    class Meta:
        model = User
        fields = [
            "password",
            "username",
            "role",
        ]

class ForgotPasswordEmailVerificationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

class ForgotPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {
            'username': {'write_only': True},
            'password': {'write_only': True},
        }

class JobSeekerSerializer(serializers.ModelSerializer):
    http_method_names = ('GET', 'PUT', 'DELETE')
    class Meta:
        ref_name = 'Job Seeker'
        model = JobSeeker
        fields = [
            'id',
            'gender',
            'date_of_birth',
            'qualification',
            'country',
            'city',
            'profile_image',
            'cv_file'
        ]
        read_only_fields = [
            'id',
        ]

class EmployerSerializer(serializers.ModelSerializer):
    http_method_names = ('GET', 'DELETE', 'PUT')
    class Meta:
        model = Employer
        fields = '__all__'
        read_only_fields = [
            'id',
        ]