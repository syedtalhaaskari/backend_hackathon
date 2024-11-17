from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User

from core.filters.jobs import JobPostFilter
from core.models.application import Application
from core.models.job_post import JobPost
from core.serializers.notification import NotificationSerializer
from core.serializers.job_post import JobPostSerializer, UnAuthJobPostSerializer, JobPostToggleSerializer
from core.serializers.application import ApplyApplicationSerializer, UserOwnAppliedApplicationSerializer
from core.permissions import JobPostPermissions, IsJobSeeker, IsOwnerOrAdmin

from user_auth.serializers import UserSerializer

class JobPostViewSet(ModelViewSet):
    queryset = JobPost.objects.select_related('user').prefetch_related('user__employer').filter(is_enabled=True).all()
    serializer_class = JobPostSerializer
    permission_classes = (JobPostPermissions,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = JobPostFilter
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        user = self.request.user
        serializer.validated_data['user'] = user
        serializer.save()
        
    def get_serializer_class(self):
        if self.request.user.is_authenticated == False:
            return UnAuthJobPostSerializer
        return super().get_serializer_class()
    
    @action(detail=False, methods=['GET'])
    def my_jobs(self, request: Request):
        user = request.user
        job_posts = JobPost.objects.filter(user=user)
        serializer = JobPostSerializer(job_posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['PUT'], serializer_class=JobPostToggleSerializer)
    def toggle(self, request: Request, pk=None):
        job_posts = JobPost.objects.get(pk=pk)
        job_posts.is_enabled = not job_posts.is_enabled
        job_posts.save(update_fields=['is_enabled'])
        return Response("Success", status=status.HTTP_200_OK)
    
    @action(detail=True, methods=('POST',), serializer_class=ApplyApplicationSerializer, permission_classes=[IsAuthenticated, IsJobSeeker])
    def apply(self, request: Request, pk=None):
        job_post = JobPost.objects.get(pk=pk)
        if job_post.user.id == request.user.id:
            return Response("Applicant and Employer cannot be same", status=status.HTTP_400_BAD_REQUEST)
        my_application = Application.objects.filter(job_post=pk)

        if my_application.count() > 0:
            return Response("Already applied", status=status.HTTP_400_BAD_REQUEST)
        data_obj = {
            'job_post': job_post,
            'job_seeker': request.user,
        }
        application = Application.objects.create(**data_obj)
        content=f"Job Post Id: {job_post.id}\nJob Seeker Id: {request.user.id}\nApplication Id: {application.id}"
        notification_obj = {
            "user": job_post.user.id,
            "content": content,
        }
        # Send notification to employer
        notification_serializer = NotificationSerializer(data=notification_obj)
        if notification_serializer.is_valid():
            notification_serializer.save()

        return Response("Applied Successfully", status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['GET'], serializer_class=UserOwnAppliedApplicationSerializer, permission_classes=[IsAuthenticated, IsJobSeeker])
    def my_applications(self, request: Request):
        user = request.user
        applications = Application.objects.filter(job_seeker=user)
        serializer = UserOwnAppliedApplicationSerializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['GET'], serializer_class=JobPostToggleSerializer, permission_classes=[IsOwnerOrAdmin, IsAuthenticated])
    def applicants(self, request: Request, pk=None):
        job_post = JobPost.objects.get(pk=pk)
        if job_post.user != request.user:
            return Response('You do not have permission to access this', status=status.HTTP_403_FORBIDDEN)

        applicants = Application.objects.filter(job_post=job_post)
        users = User.objects.filter(id__in=applicants.values_list('job_seeker')).all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)