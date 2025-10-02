"""
Views for User app
"""
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.db import transaction

from .models import User, StudentProfile, TransportOrganizer
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserSerializer,
    StudentProfileSerializer, StudentProfileCreateSerializer,
    TransportOrganizerSerializer, TransportOrganizerCreateSerializer,
    ChangePasswordSerializer
)

User = get_user_model()


class UserRegistrationView(APIView):
    """
    User registration endpoint
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'User registered successfully',
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """
    User login endpoint
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'Login successful',
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Get and update user profile
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    """
    Change user password
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentProfileView(generics.RetrieveUpdateAPIView):
    """
    Get and update student profile
    """
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        try:
            return self.request.user.student_profile
        except StudentProfile.DoesNotExist:
            return None
    
    def get(self, request, *args, **kwargs):
        profile = self.get_object()
        if not profile:
            return Response(
                {'message': 'Student profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(profile)
        return Response(serializer.data)


class StudentProfileCreateView(APIView):
    """
    Create student profile
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        # Check if user is a student
        if request.user.role != 'student':
            return Response(
                {'message': 'Only students can create student profiles'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if profile already exists
        if hasattr(request.user, 'student_profile'):
            return Response(
                {'message': 'Student profile already exists'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = StudentProfileCreateSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                profile = serializer.save(user=request.user)
                return Response(
                    StudentProfileSerializer(profile).data, 
                    status=status.HTTP_201_CREATED
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransportOrganizerProfileView(generics.RetrieveUpdateAPIView):
    """
    Get and update transport organizer profile
    """
    serializer_class = TransportOrganizerSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        try:
            return self.request.user.organizer_profile
        except TransportOrganizer.DoesNotExist:
            return None
    
    def get(self, request, *args, **kwargs):
        profile = self.get_object()
        if not profile:
            return Response(
                {'message': 'Transport organizer profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(profile)
        return Response(serializer.data)


class TransportOrganizerCreateView(APIView):
    """
    Create transport organizer profile
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        # Check if user is a transport organizer
        if request.user.role != 'transport_organizer':
            return Response(
                {'message': 'Only transport organizers can create organizer profiles'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if profile already exists
        if hasattr(request.user, 'organizer_profile'):
            return Response(
                {'message': 'Transport organizer profile already exists'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = TransportOrganizerCreateSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                profile = serializer.save(user=request.user)
                return Response(
                    TransportOrganizerSerializer(profile).data, 
                    status=status.HTTP_201_CREATED
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """
    Logout user by blacklisting refresh token
    """
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)