from rest_framework.urls import path
from rest_framework.routers import DefaultRouter

from .views import LoginAPIView, LogoutAPIView, UserAPIView, ProfileModelViewSet, ChangePasswordAPIView, ForgotPasswordAPIView, ForgotPasswordEmailVerificationAPIView

router = DefaultRouter()
router.register("profile", ProfileModelViewSet, basename='profile')

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('signup/', UserAPIView.as_view(), name="signup"),
    path('change-password/', ChangePasswordAPIView.as_view(), name="change_password"),
    path('forgot-password/', ForgotPasswordAPIView.as_view(), name="forgot_password"),
    path('forgot-password/email-verification', ForgotPasswordEmailVerificationAPIView.as_view(), name="forgot_password_email_verification"),
] + router.urls