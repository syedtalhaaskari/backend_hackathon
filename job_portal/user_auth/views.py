from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
# For Email Verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.contrib import messages

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser

from drf_yasg.utils import swagger_auto_schema

from core.serializers.notification import NotificationSerializer

from .permissions import ProfilePermission
from .models import JobSeeker, Employer
from .serializers import SignUpSerializer, LoginSerializer, JobSeekerSerializer, EmployerSerializer, ChangePasswordSerializer, ForgotPasswordSerializer, ForgotPasswordEmailVerificationSerializer
# For Email Verification
from .token import account_activation_token

class LoginAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request: Request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
class LogoutAPIView(APIView):
    def post(self, request: Request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

def verify_email(request, user):
    current_site = get_current_site(request)

    username = user.username
    email = user.email
    subject = "Verify Email"
    message = render_to_string('user_auth/verify_email_message.html', {
        'request': request,
        'user': username,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.id)),
        'token': account_activation_token.make_token(user),
    })
    email = EmailMessage(
        subject, message, to=[email]
    )
    email.content_subtype = 'html'
    email.send()

def verify_email_done(request):
    return render(request, 'user_auth/verify_email_done.html')

def verify_email_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if user.groups.filter(name='Employer').count() > 0:
            emp = Employer.objects.get(user__id = uid)
            emp.is_verified = True
            emp.save()
        else:
            emp = JobSeeker.objects.get(user__id = uid)
            emp.is_verified = True
            emp.save()
        messages.success(request, 'Your email has been verified.')
        return redirect('verify-email-complete')
    else:
        messages.warning(request, 'The link is invalid.')
    return render(request, 'user_auth/verify_email_confirm.html')

def verify_email_complete(request):
    return render(request, 'user_auth/verify_email_complete.html')

class UserAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(request_body=SignUpSerializer)
    def post(self, request: Request):
        try:
            data = request.data
            serializer = SignUpSerializer(data=data)
            
            if serializer.is_valid():
                role = serializer.validated_data.pop('role')
                group = Group.objects.filter(name=role).first()

                if group is None:
                    return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)
                
                serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
                user = User.objects.create(**serializer.validated_data)

                user.groups.set([group])
                if group.name == 'Job_Seeker':
                    JobSeeker.objects.create(user=user)
                elif group.name == 'Employer':
                    Employer.objects.create(user=user)
                content=f"Thank you for signing up click the line below to verify your account https://www.google.com"
                verify_email(request, user)
                notification_obj = {
                    "user": user.id,
                    "content": content,
                }
                notification_serializer = NotificationSerializer(data=notification_obj)
                if notification_serializer.is_valid():
                    notification_serializer.save()
                return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
# @swagger_auto_schema(methods=['GET', 'PUT', 'DELETE'])
class ProfileModelViewSet(ModelViewSet):
    # http_method_names = ('GET', 'PUT', 'DELETE')
    queryset = User.objects.all()
    serializer_class = JobSeekerSerializer
    permission_classes = (ProfilePermission,)
    parser_classes = (MultiPartParser,)

    # pagination_class = None

    def get_queryset(self):
        if self.request.user.groups.filter(name='Employer').count() > 0:
            return Employer.objects.filter(user__id=self.request.user.id)
        return JobSeeker.objects.filter(user__id=self.request.user.id)
    
    def get_serializer_class(self):
        if self.request.user.groups.filter(name='Employer').count() > 0:
            return EmployerSerializer
        return super().get_serializer_class()

class ChangePasswordAPIView(APIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def put(self, request):
        try:
            data = request.data

            serializer = self.serializer_class(data=data)
            
            if serializer.is_valid():
                data = serializer.validated_data
                if data['new_password'] != data['confirm_password']:
                    return Response({"error": "New and Confirm passwords does not match"}, status=status.HTTP_400_BAD_REQUEST)

                # encrypt old password
                old_password = authenticate(username=request.user.username, password=data['old_password'])
                if not old_password:
                    return Response({"error": "Invalid old password"}, status=status.HTTP_400_BAD_REQUEST)

                # encrypt new password
                request.user.password = make_password(data['new_password'])

                request.user.save()
                return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class ForgotPasswordAPIView(APIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=ForgotPasswordSerializer)
    def post(self, request):
        try:
            data = request.data

            serializer = self.serializer_class(data=data)
            
            if serializer.is_valid():
                data = serializer.validated_data

                user = User.objects.get(email=data['email'], username=data['username'])

                if user is not None:
                    content=f"To reset your password click the link: https://www.google.com"
                    notification_obj = {
                        "user": user.id,
                        "content": content,
                    }
                    # Send notification to User
                    notification_serializer = NotificationSerializer(data=notification_obj)
                    if notification_serializer.is_valid():
                        notification_serializer.save()
                    return Response({"message": "A verification link has been sent to your email"}, status=status.HTTP_200_OK)
                raise User.DoesNotExist                
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": 'Invalid User'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class ForgotPasswordEmailVerificationAPIView(APIView):
    serializer_class = ForgotPasswordEmailVerificationSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=ForgotPasswordEmailVerificationSerializer)
    def post(self, request):
        try:
            data = request.data

            serializer = self.serializer_class(data=data)
            
            if serializer.is_valid():
                data = serializer.validated_data
                if data['new_password'] != data['confirm_password']:
                    return Response({"error": "New and Confirm passwords does not match"}, status=status.HTTP_400_BAD_REQUEST)
                user = User.objects.get(username=data['username'])

                # encrypt new password
                user.password = make_password(data['new_password'])

                user.save()
                return Response({"message": "Password Reset successfully"}, status=status.HTTP_200_OK)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": 'Invalid User'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy

class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'registration/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    template_name = 'registration/password_reset_form.html'