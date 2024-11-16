from rest_framework import serializers

from user_auth.serializers import JobSeekerSerializer

from core.models.job_post import JobPost
from core.models.application import Application
from core.serializers.job_post import JobPostSerializer

class UserOwnAppliedApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'

class ApplyApplicationSerializer(serializers.ModelSerializer):
    job_post = JobPostSerializer(read_only=True)
    job_seeker = JobSeekerSerializer(read_only=True)

    class Meta:
        model = Application
        fields = '__all__'
        extra_kwargs = {
            'job_post': {'read_only': True},
        }
        read_only_fields = [
            'status'
        ]

class ApplicationSerializer(serializers.ModelSerializer):
    job_post = JobPostSerializer(read_only=True)
    job_seeker = JobSeekerSerializer(read_only=True)

    class Meta:
        model = Application
        fields = '__all__'
        extra_kwargs = {
            'job_post': {'read_only': True},
        }