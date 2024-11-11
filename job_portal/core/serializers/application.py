from django.contrib.auth.models import User
from rest_framework import serializers

from user_auth.serializers import UserSerializer, EmployerSerializer, JobSeekerSerializer

from core.models.job_post import JobPost
from core.models.application import Application
from core.serializers.job_post import JobPostSerializer

class ApplicationSerializer(serializers.ModelSerializer):
    job_post = JobPostSerializer(read_only=True)
    job_seeker = JobSeekerSerializer(read_only=True)

    class Meta:
        model = Application
        fields = '__all__'
        extra_kwargs = {
            'job_post': {'read_only': True},
        }