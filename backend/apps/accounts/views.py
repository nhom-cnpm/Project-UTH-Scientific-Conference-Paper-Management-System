from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, Role, UserConferenceRole, UserNotificationPreference
from .serializers import (
    UserSerializer, UserDetailSerializer, UserRegistrationSerializer,
    PasswordChangeSerializer, RoleSerializer, UserConferenceRoleSerializer
)
from .permissions import IsOwnerOrAdmin, IsAdminUser

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            return UserDetailSerializer
        return UserSerializer
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Lấy thông tin user hiện tại"""
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['patch'])
    def update_profile(self, request):
        """Update profile"""
        user = request.user
        allowed_fields = ['full_name', 'affiliation', 'country', 'bio', 'phone_number', 'website', 'orcid']
        
        for field, value in request.data.items():
            if field in allowed_fields:
                setattr(user, field, value)
        
        user.save()
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """Đổi mật khẩu"""
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({'error': 'Old password is incorrect'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Password changed successfully'})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Đăng ký user mới"""
    serializer = UserRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        # Tạo notification preferences
        UserNotificationPreference.objects.create(user=user)
        
        return Response({
            'message': 'Registration successful',
            'user_id': user.id
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Login"""
    email = request.data.get('email')
    password = request.data.get('password')
    
    user = authenticate(username=email, password=password)
    
    if user:
        if user.status != 'active':
            return Response({'error': f'Account is {user.status}'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        user.update_last_login()
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserDetailSerializer(user).data
        })
    
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class RoleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]


class UserConferenceRoleViewSet(viewsets.ModelViewSet):
    queryset = UserConferenceRole.objects.all()
    serializer_class = UserConferenceRoleSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return UserConferenceRole.objects.all()
        return UserConferenceRole.objects.filter(user=user)