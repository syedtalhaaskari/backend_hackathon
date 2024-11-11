from rest_framework.routers import DefaultRouter

from .views.job_post import JobPostViewSet

router = DefaultRouter()
router.register("jobs", JobPostViewSet, basename="jobs")

urlpatterns = [] + router.urls