from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.
class User(AbstractUser):
    """
    Custom User model mở rộng từ AbstractUser của Django
    """
    USER_STATUS = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('pending', 'Pending Verification'),
    ]
    
    # Override email để bắt buộc và unique
    email = models.EmailField(
        _('email address'),
        unique=True,
        validators=[EmailValidator()],
        error_messages={
            'unique': _("A user with that email already exists."),
        }
    )
    
    # Thông tin cá nhân
    full_name = models.CharField(
        max_length=255,
        blank=True,
        help_text="Full name of the user"
    )
    
    affiliation = models.CharField(
        max_length=255,
        blank=True,
        help_text="University/Organization affiliation"
    )
    
    country = models.CharField(
        max_length=100,
        blank=True
    )
    
    # Bio/About
    bio = models.TextField(
        blank=True,
        help_text="Short biography"
    )
    
    # Contact info
    phone_number = models.CharField(
        max_length=20,
        blank=True
    )
    
    website = models.URLField(
        blank=True,
        help_text="Personal or professional website"
    )
    
    # ORCID (researcher ID)
    orcid = models.CharField(
        max_length=19,
        blank=True,
        help_text="ORCID iD (e.g., 0000-0002-1825-0097)"
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=USER_STATUS,
        default='pending'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_at = models.DateTimeField(null=True, blank=True)
    
    # Email verification
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, blank=True)
    
    # Password reset
    password_reset_token = models.CharField(max_length=100, blank=True)
    password_reset_expires = models.DateTimeField(null=True, blank=True)
    
    # Avatar
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True
    )
    
    # Preferences (JSON field)
    preferences = models.JSONField(
        default=dict,
        blank=True,
        help_text="User preferences and settings"
    )
    
    # Make email the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.full_name or self.username} ({self.email})"
    
    def save(self, *args, **kwargs):
        """Override save để xử lý logic"""
        # Auto-generate username from email if not provided
        if not self.username:
            self.username = self.email.split('@')[0]
        
        # Sync full_name với first_name, last_name
        if self.full_name and not self.first_name:
            name_parts = self.full_name.split(' ', 1)
            self.first_name = name_parts[0]
            if len(name_parts) > 1:
                self.last_name = name_parts[1]
        
        super().save(*args, **kwargs)
    
    def get_full_name(self):
        """Override để return full_name"""
        return self.full_name or super().get_full_name()
    
    def activate(self):
        """Activate user account"""
        self.status = 'active'
        self.email_verified = True
        self.save()
    
    def deactivate(self):
        """Deactivate user account"""
        self.status = 'inactive'
        self.is_active = False
        self.save()
    
    def suspend(self, reason=""):
        """Suspend user account"""
        self.status = 'suspended'
        self.is_active = False
        self.save()
        # TODO: Log suspension reason
    
    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login_at = timezone.now()
        self.save(update_fields=['last_login_at'])
    
    def has_role_in_conference(self, conference, role_name):
        """Check if user has specific role in conference"""
        return UserConferenceRole.objects.filter(
            user=self,
            conference=conference,
            role__name=role_name
        ).exists()
    
    def get_conferences_by_role(self, role_name):
        """Get all conferences where user has specific role"""
        return UserConferenceRole.objects.filter(
            user=self,
            role__name=role_name
        ).select_related('conference')


class Role(models.Model):
    """
    Roles trong hệ thống (Author, Reviewer, Chair, Admin)
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
    name = models.CharField(
        max_length=50,
        unique=True,
        choices=ROLE_TYPES
    )
    display_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    # Permissions (có thể dùng Django's built-in permissions)
    permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='custom_roles'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'roles'
        ordering = ['name']
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
    
    def __str__(self):
        return self.display_name or self.name
    
    def assign_to_user(self, user):
        """Assign role to user globally"""
        group, created = Group.objects.get_or_create(name=self.display_name)
        user.groups.add(group)


class UserConferenceRole(models.Model):
    """
    Vai trò của user trong một conference cụ thể
    Ví dụ: User A là Reviewer trong Conference X, Chair trong Conference Y
    """
    user_role_id = models.AutoField(primary_key=True)
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='conference_roles'
    )
    
    conference = models.ForeignKey(
        'conferences.Conference',  # Giả sử có Conference model
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
    
    # Có thể có thời hạn
    expires_at = models.DateTimeField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'user_conference_roles'
        unique_together = ['user', 'conference', 'role']
        ordering = ['-assigned_at']
        verbose_name = 'User Conference Role'
        verbose_name_plural = 'User Conference Roles'
        indexes = [
            models.Index(fields=['user', 'conference']),
            models.Index(fields=['conference', 'role']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.role.display_name} in {self.conference}"
    
    def clean(self):
        """Validation"""
        # Check expiration
        if self.expires_at and self.expires_at < timezone.now():
            raise ValidationError("Expiration date cannot be in the past")
    
    def is_expired(self):
        """Check if role is expired"""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
    
    def revoke(self):
        """Revoke role"""
        self.is_active = False
        self.save()


class UserNotificationPreference(models.Model):
    """
    Cài đặt notification của user
    """
    NOTIFICATION_TYPES = [
        ('email', 'Email'),
        ('in_app', 'In-App'),
        ('sms', 'SMS'),
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='notification_preferences'
    )
    
    # Email notifications
    email_on_paper_submitted = models.BooleanField(default=True)
    email_on_review_assigned = models.BooleanField(default=True)
    email_on_review_submitted = models.BooleanField(default=True)
    email_on_decision_made = models.BooleanField(default=True)
    email_on_discussion = models.BooleanField(default=True)
    
    # In-app notifications
    in_app_notifications = models.BooleanField(default=True)
    
    # Digest emails
    daily_digest = models.BooleanField(default=False)
    weekly_digest = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_notification_preferences'
        verbose_name = 'Notification Preference'
        verbose_name_plural = 'Notification Preferences'
    
    def __str__(self):
        return f"Notification preferences for {self.user.username}"


class UserActivity(models.Model):
    """
    Log hoạt động của user (audit trail)
    """
    ACTIVITY_TYPES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('profile_update', 'Profile Update'),
        ('password_change', 'Password Change'),
        ('paper_submit', 'Paper Submitted'),
        ('review_submit', 'Review Submitted'),
        ('role_assigned', 'Role Assigned'),
    ]
    
    activity_id = models.AutoField(primary_key=True)
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='activities'
    )
    
    activity_type = models.CharField(
        max_length=50,
        choices=ACTIVITY_TYPES
    )
    
    description = models.TextField(blank=True)
    
    # IP address
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    # User agent
    user_agent = models.TextField(blank=True)
    
    # Additional metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_activities'
        ordering = ['-created_at']
        verbose_name = 'User Activity'
        verbose_name_plural = 'User Activities'
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['activity_type']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.activity_type} at {self.created_at}"