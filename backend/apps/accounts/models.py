from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    """
    Custom User model
    """
    USER_STATUS = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('pending', 'Pending Verification'),
    ]
    
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator()],
        error_messages={
            'unique': "A user with that email already exists.",
        }
    )
    
    full_name = models.CharField(max_length=255, blank=True)
    affiliation = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    orcid = models.CharField(max_length=19, blank=True)
    
    status = models.CharField(
        max_length=20,
        choices=USER_STATUS,
        default='pending'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_at = models.DateTimeField(null=True, blank=True)
    
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, blank=True)
    
    password_reset_token = models.CharField(max_length=100, blank=True)
    password_reset_expires = models.DateTimeField(null=True, blank=True)
    
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    preferences = models.JSONField(default=dict, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name or self.username} ({self.email})"
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email.split('@')[0]
        super().save(*args, **kwargs)
    
    def activate(self):
        self.status = 'active'
        self.email_verified = True
        self.save()
    
    def deactivate(self):
        self.status = 'inactive'
        self.is_active = False
        self.save()
    
    def update_last_login(self):
        self.last_login_at = timezone.now()
        self.save(update_fields=['last_login_at'])


class Role(models.Model):
    """
    Roles trong hệ thống
    """
    ROLE_TYPES = [
        ('author', 'Author'),
        ('reviewer', 'Reviewer'),
        ('pc_member', 'PC Member'),
        ('chair', 'Program Chair'),
        ('track_chair', 'Track Chair'),
        ('admin', 'Administrator'),
    ]
    
    role_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True, choices=ROLE_TYPES)
    display_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'roles'
        ordering = ['name']
    
    def __str__(self):
        return self.display_name or self.name


class UserConferenceRole(models.Model):
    """
    Vai trò của user trong conference cụ thể
    """
    user_role_id = models.AutoField(primary_key=True)
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='conference_roles'
    )
    
    conference = models.ForeignKey(
        'conferences.Conference',
        on_delete=models.CASCADE,
        related_name='user_roles'
    )
    
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name='user_conference_assignments'
    )
    
    assigned_at = models.DateTimeField(auto_now_add=True)
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='role_assignments_made'
    )
    
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'user_conference_roles'
        unique_together = ['user', 'conference', 'role']
        ordering = ['-assigned_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.role.display_name} in {self.conference}"
    
    def is_expired(self):
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
    
    def revoke(self):
        self.is_active = False
        self.save()


class UserNotificationPreference(models.Model):
    """
    Cài đặt notification
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='notification_preferences'
    )
    
    email_on_paper_submitted = models.BooleanField(default=True)
    email_on_review_assigned = models.BooleanField(default=True)
    email_on_review_submitted = models.BooleanField(default=True)
    email_on_decision_made = models.BooleanField(default=True)
    email_on_discussion = models.BooleanField(default=True)
    
    in_app_notifications = models.BooleanField(default=True)
    daily_digest = models.BooleanField(default=False)
    weekly_digest = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_notification_preferences'
    
    def __str__(self):
        return f"Notification preferences for {self.user.username}"


class UserActivity(models.Model):
    """
    Log hoạt động của user
    """
    ACTIVITY_TYPES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('profile_update', 'Profile Update'),
        ('password_change', 'Password Change'),
        ('paper_submit', 'Paper Submitted'),
        ('review_submit', 'Review Submitted'),
    ]
    
    activity_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_activities'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.activity_type}"