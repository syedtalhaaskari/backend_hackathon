from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Count, Sum, Avg, F, Q

from core.models.application import Application
from core.serializers.application import ApplicationSerializer, UnAuthApplicationSerializer
from core.permissions import ApplicationPermissions

class ApplicationViewSet(ModelViewSet):
    queryset = Application.objects.select_related('user').all()
    serializer_class = ApplicationSerializer
    permission_classes = (ApplicationPermissions,)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.validated_data['user'] = user
        serializer.save()
    
    @action(detail=False, methods=['GET'])
    def my_jobs(self, request: Request):
        user = request.user
        applications = Application.objects.filter(user=user)
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)