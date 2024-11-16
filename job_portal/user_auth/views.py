from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from core.serializers.notification import NotificationSerializer

from .permissions import ProfilePermission
from .models import JobSeeker, Employer
from .serializers import UserSerializer, LoginSerializer, JobSeekerSerializer, EmployerSerializer, ChangePasswordSerializer, ForgotPasswordSerializer, ForgotPasswordEmailVerificationSerializer

class LoginAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request: Request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
class LogoutAPIView(APIView):
    def post(self, request: Request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

class UserAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request: Request):
        try:
            data = request.data

            serializer = UserSerializer(data=data)
            
            if serializer.is_valid():
                groups = serializer.validated_data.pop('groups')
                serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
                user = User.objects.create(**serializer.validated_data)
                user.groups.set(groups)
                for group in groups:
                    if group.name == 'Job_Seeker':
                        JobSeeker.objects.create(user=user)
                    elif group.name == 'Employer':
                        Employer.objects.create(user=user)
                content=f"Thank you for signing up click the line below to verify your account https://www.google.com"
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
        
class ProfileModelViewSet(ModelViewSet):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    permission_classes = (ProfilePermission,)
    # pagination_class = None
    
    def get_queryset(self):
        if self.request.user.groups.filter(name='Job_Seeker').count() > 0:
            return JobSeeker.objects.filter(user__id=self.request.user.id)
        return super().get_queryset()
    
    def get_serializer_class(self):
        if self.request.user.groups.filter(name='Job_Seeker').count() > 0:
            return JobSeekerSerializer
        return super().get_serializer_class()
    
class ChangePasswordAPIView(APIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

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
    