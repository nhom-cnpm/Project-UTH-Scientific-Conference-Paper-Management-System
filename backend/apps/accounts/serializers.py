from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Role, UserConferenceRole, UserNotificationPreference


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'full_name', 'affiliation', 'country', 
                  'bio', 'website', 'orcid', 'avatar', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'full_name', 'affiliation', 'country',
                  'bio', 'phone_number', 'website', 'orcid', 'avatar', 'status',
                  'email_verified', 'created_at', 'updated_at', 'last_login_at']
        read_only_fields = ['id', 'email_verified', 'created_at', 'updated_at', 'last_login_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password_confirm', 'full_name', 'affiliation', 'country']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords don't match"})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            full_name=validated_data.get('full_name', ''),
            affiliation=validated_data.get('affiliation', ''),
            country=validated_data.get('country', ''),
            status='pending'
        )
        return user


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password": "Passwords don't match"})
        return attrs


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['role_id', 'name', 'display_name', 'description']


class UserConferenceRoleSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    role_name = serializers.CharField(source='role.display_name', read_only=True)
    conference_name = serializers.CharField(source='conference.name', read_only=True)
    
    class Meta:
        model = UserConferenceRole
        fields = ['user_role_id', 'user', 'user_email', 'user_name', 'conference',
                  'conference_name', 'role', 'role_name', 'assigned_at', 'expires_at', 'is_active']
        read_only_fields = ['assigned_at']