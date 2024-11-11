from rest_framework.urls import path
from rest_framework.routers import DefaultRouter

from .views import LoginAPIView, LogoutAPIView, UserAPIView, ProfileModelViewSet

router = DefaultRouter()
router.register("profile", ProfileModelViewSet, basename='profile')

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('signup/', UserAPIView.as_view(), name="signup"),
] + router.urls