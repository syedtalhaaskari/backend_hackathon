from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from core.permissions import IsOwner
from core.models.job_post import JobPost
from core.models.application import Application
from core.serializers.application import ApplicationSerializer
from core.serializers.notification import NotificationSerializer

class UpdateApplicantStatusView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = ApplicationSerializer

    def put(self, request, id, applicant_id):    
        try:
            job_post = JobPost.objects.get(id=id, user=request.user)
        except JobPost.DoesNotExist:
            return Response({"error": "Job post not found or you do not have permission."}, status=status.HTTP_404_NOT_FOUND)

        try:
            job_seeker = User.objects.get(pk=applicant_id)
        except JobPost.DoesNotExist:
            return Response({"error": "Invalid Applicant"}, status=status.HTTP_404_NOT_FOUND)

        try:
            job_application = Application.objects.get(job_post=job_post, job_seeker=job_seeker)
        except Application.DoesNotExist:
            return Response({"error": "Job application not found."}, status=status.HTTP_404_NOT_FOUND)
        try:
            job_application.status=request.data.get('status')
            job_application.save()


            content=f"Job Post Id: {job_post.id}\nStatus: {job_application.status}\n"
            notification_obj = {
                "user": job_post.user.id,
                "content": content,
            }
            # Send notification to Job Seeker
            notification_serializer = NotificationSerializer(data=notification_obj)
            if notification_serializer.is_valid():
                notification_serializer.save()
            else:
                return Response(notification_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Application status updated successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
