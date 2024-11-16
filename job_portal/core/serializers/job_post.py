from rest_framework import serializers

from user_auth.serializers import UserSerializer

from core.models.job_post import JobPost

class UnAuthJobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = '__all__'
        extra_kwargs = {
            'salary_range': {'write_only': True},
        }
        
class JobPostToggleSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = (
            'id',
            'is_enabled',
        )
        
class JobPostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = JobPost
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
        }