# For password reset
from django.contrib.auth import views as auth_views

from rest_framework.urls import path
from rest_framework.routers import DefaultRouter

from .views import verify_email, verify_email_done, verify_email_confirm, verify_email_complete, LoginAPIView, LogoutAPIView, UserAPIView, ProfileModelViewSet, ChangePasswordAPIView, ForgotPasswordAPIView, ForgotPasswordEmailVerificationAPIView

router = DefaultRouter()
router.register("profile", ProfileModelViewSet, basename='profile')

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('signup/', UserAPIView.as_view(), name="signup"),
    path('change-password/', ChangePasswordAPIView.as_view(), name="change_password"),
    # path('forgot-password/', ForgotPasswordAPIView.as_view(), name="forgot_password"),
    # path('forgot-password/email-verification', ForgotPasswordEmailVerificationAPIView.as_view(), name="forgot_password_email_verification"),
    # For Email Verification
    path('verify-email/', verify_email, name='verify-email'),
    path('verify-email/done/', verify_email_done, name='verify-email-done'),
    path('verify-email-confirm/<uidb64>/<token>/', verify_email_confirm, name='verify-email-confirm'),
    path('verify-email/complete/', verify_email_complete, name='verify-email-complete'),
    # For forgot password
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
] + router.urls