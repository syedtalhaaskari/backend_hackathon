from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from core.filters.jobs import JobPostFilter
from core.models.job_post import JobPost
from core.serializers.job_post import JobPostSerializer, UnAuthJobPostSerializer, JobPostToggleSerializer
from core.permissions import JobPostPermissions

class JobPostViewSet(ModelViewSet):
    queryset = JobPost.objects.select_related('user').prefetch_related('user__employer').filter(is_enabled=True).all()
    serializer_class = JobPostSerializer
    permission_classes = (JobPostPermissions,)
    filter_backends = [DjangoFilterBackend]
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