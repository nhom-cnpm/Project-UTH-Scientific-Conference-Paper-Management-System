from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    User, Role, UserConferenceRole, 
    UserNotificationPreference, UserActivity
)

# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User Admin"""
    
    list_display = [
        'email',
        'username',
        'full_name',
        'affiliation',
        'status_badge',
        'email_verified_badge',
        'created_at',
        'last_login_at'
    ]
    
    list_filter = [
        'status',
        'email_verified',
        'is_staff',
        'is_superuser',
        'created_at',
    ]
    
    search_fields = [
        'email',
        'username',
        'full_name',
        'affiliation',
    ]
    
    readonly_fields = [
        'created_at',
        'updated_at',
        'last_login_at',
        'date_joined',
    ]
    
    fieldsets = (
        ('Login Information', {
            'fields': ('email', 'username', 'password')
        }),
        ('Personal Information', {
            'fields': (
                'full_name',
                'first_name',
                'last_name',
                'affiliation',
                'country',
                'bio',
            )
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'website', 'orcid')
        }),
        ('Status', {
            'fields': (
                'status',
                'email_verified',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
        ('Avatar', {
            'fields': ('avatar',),
            'classes': ('collapse',)
        }),
        ('Permissions', {
            'fields': ('groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Important Dates', {
            'fields': (
                'created_at',
                'updated_at',
                'last_login_at',
                'date_joined',
            ),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        ('Required Information', {
            'classes': ('wide',),
            'fields': ('email', 'username', 'full_name', 'password1', 'password2'),
        }),
        ('Optional Information', {
            'classes': ('collapse',),
            'fields': ('affiliation', 'country', 'status'),
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'active': 'green',
            'inactive': 'gray',
            'suspended': 'red',
            'pending': 'orange',
        }
        color = colors.get(obj.status, 'blue')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def email_verified_badge(self, obj):
        if obj.email_verified:
            return format_html('<span style="color: green;">✓ Verified</span>')
        return format_html('<span style="color: red;">✗ Not Verified</span>')
    email_verified_badge.short_description = 'Email Status'
    
    actions = ['activate_users', 'deactivate_users', 'verify_emails']
    
    def activate_users(self, request, queryset):
        count = queryset.update(status='active', is_active=True)
        self.message_user(request, f'{count} users activated.')
    activate_users.short_description = 'Activate selected users'
    
    def deactivate_users(self, request, queryset):
        count = queryset.update(status='inactive', is_active=False)
        self.message_user(request, f'{count} users deactivated.')
    deactivate_users.short_description = 'Deactivate selected users'
    
    def verify_emails(self, request, queryset):
        count = queryset.update(email_verified=True)
        self.message_user(request, f'{count} emails verified.')
    verify_emails.short_description = 'Verify emails for selected users'


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['role_id', 'name', 'display_name', 'created_at']
    search_fields = ['name', 'display_name', 'description']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'display_name', 'description')
        }),
        ('Permissions', {
            'fields': ('permissions',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserConferenceRole)
class UserConferenceRoleAdmin(admin.ModelAdmin):
    list_display = [
        'user_role_id',
        'get_user',
        'get_conference',
        'get_role',
        'is_active',
        'assigned_at',
        'expires_at',
        'is_expired_indicator'
    ]
    
    list_filter = [
        'role',
        'is_active',
        'assigned_at',
    ]
    
    search_fields = [
        'user__email',
        'user__full_name',
        'conference__name',
    ]
    
    readonly_fields = ['assigned_at']
    
    def get_user(self, obj):
        return obj.user.full_name or obj.user.username
    get_user.short_description = 'User'
    
    def get_conference(self, obj):
        return str(obj.conference)
    get_conference.short_description = 'Conference'
    
    def get_role(self, obj):
        return obj.role.display_name
    get_role.short_description = 'Role'
    
    def is_expired_indicator(self, obj):
        if obj.is_expired():
            return format_html('<span style="color: red;">✗ Expired</span>')
        return format_html('<span style="color: green;">✓ Active</span>')
    is_expired_indicator.short_description = 'Expiration Status'


@admin.register(UserNotificationPreference)
class UserNotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'email_on_paper_submitted',
        'email_on_review_assigned',
        'in_app_notifications',
        'updated_at'
    ]
    
    search_fields = ['user__email', 'user__full_name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = [
        'activity_id',
        'get_user',
        'activity_type',
        'ip_address',
        'created_at'
    ]
    
    list_filter = [
        'activity_type',
        'created_at',
    ]
    
    search_fields = [
        'user__email',
        'user__full_name',
        'description',
        'ip_address',
    ]
    
    readonly_fields = ['created_at']
    
    def get_user(self, obj):
        return obj.user.full_name or obj.user.username
    get_user.short_description = 'User'
    
    def has_add_permission(self, request):
        # Không cho phép tạo activity manually
        return False
    
    def has_change_permission(self, request, obj=None):
        # Không cho phép sửa activity
        return False