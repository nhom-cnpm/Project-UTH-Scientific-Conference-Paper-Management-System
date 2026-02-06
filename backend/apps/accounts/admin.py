from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, Role, UserConferenceRole, UserNotificationPreference, UserActivity

# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'full_name', 'status', 'email_verified', 'created_at']
    list_filter = ['status', 'email_verified', 'is_staff', 'created_at']
    search_fields = ['email', 'username', 'full_name', 'affiliation']
    
    fieldsets = (
        ('Login', {'fields': ('email', 'username', 'password')}),
        ('Personal', {'fields': ('full_name', 'affiliation', 'country', 'bio')}),
        ('Contact', {'fields': ('phone_number', 'website', 'orcid')}),
        ('Status', {'fields': ('status', 'email_verified', 'is_active', 'is_staff', 'is_superuser')}),
        ('Dates', {'fields': ('created_at', 'updated_at', 'last_login_at'), 'classes': ('collapse',)}),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'last_login_at']


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['role_id', 'name', 'display_name', 'created_at']
    search_fields = ['name', 'display_name']


@admin.register(UserConferenceRole)
class UserConferenceRoleAdmin(admin.ModelAdmin):
    list_display = ['user_role_id', 'user', 'conference', 'role', 'is_active', 'assigned_at']
    list_filter = ['role', 'is_active']
    search_fields = ['user__email', 'conference__name']


@admin.register(UserNotificationPreference)
class UserNotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_on_paper_submitted', 'email_on_review_assigned', 'updated_at']
    search_fields = ['user__email']


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['activity_id', 'user', 'activity_type', 'ip_address', 'created_at']
    list_filter = ['activity_type', 'created_at']
    search_fields = ['user__email', 'description']
    readonly_fields = ['created_at']
    
    def has_add_permission(self, request):
        return False