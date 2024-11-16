from django.urls import path
from rest_framework.routers import DefaultRouter

from .views.job_post import JobPostViewSet
from .views.application import UpdateApplicantStatusView
from .views.notification import NotificationListView

router = DefaultRouter()
router.register("jobs", JobPostViewSet, basename="jobs")

urlpatterns = [
    path('jobs/<int:id>/applicants/<int:applicant_id>/status', UpdateApplicantStatusView.as_view(), name='UpdateApplicantStatus'),
    path('notifications', NotificationListView.as_view(), name='notifications'),
    path('notifications/<int:id>', NotificationListView.as_view(), name='notification_detail')
] + router.urls