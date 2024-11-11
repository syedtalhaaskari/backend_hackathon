from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from .permissions import ProfilePermission
from .models import JobSeeker, Employer
from .serializers import UserSerializer, LoginSerializer, JobSeekerSerializer, EmployerSerializer

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
    http_method_names = ('POST')
    permission_classes = (AllowAny)

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
                return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class ProfileModelViewSet(ModelViewSet):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    permission_classes = (ProfilePermission,)
    
    def get_queryset(self):
        queryset = Employer.objects.filter(user__id=self.request.user.id)
        return queryset