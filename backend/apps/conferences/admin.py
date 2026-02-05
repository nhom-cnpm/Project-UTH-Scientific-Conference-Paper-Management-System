from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
# Register your models here.


from .models import (
    Conference, Track, Topic, Paper, PaperAuthor,
    Reviewer, ReviewAssignment, Review, Decision,
    Role, Permission, RolePermission, UserConferenceRole,
    PolicySetting, ConflictOfInterest, SystemLog, Notification
)


@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'start_date', 'submission_deadline', 'is_submission_open_display', 'created_date']
    list_filter = ['status', 'created_date', 'start_date']
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'created_date', 'updated_date']
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'name', 'description', 'status')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date', 'submission_deadline', 
                      'review_deadline', 'camera_ready_deadline', 'notification_date')
        }),
        ('Policy Settings', {
            'fields': ('single_blind', 'double_blind', 'coi_enforced', 'ai_enabled')
        }),
        ('AI Features', {
            'fields': ('grammar_check_enabled', 'abstract_summary_enabled', 'similarity_check_enabled'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_date', 'updated_date', 'is_deleted'),
            'classes': ('collapse',)
        }),
    )
    
    def is_submission_open_display(self, obj):
        if obj.is_submission_open():
            return format_html('<span style="color: green;">✓ Open</span>')
        return format_html('<span style="color: red;">✗ Closed</span>')
    is_submission_open_display.short_description = 'Submission Status'


class TopicInline(admin.TabularInline):
    model = Topic
    extra = 1


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ['name', 'conference', 'created_date']
    list_filter = ['conference', 'created_date']
    search_fields = ['name', 'description']
    inlines = [TopicInline]


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'track', 'get_conference']
    list_filter = ['track__conference']
    search_fields = ['name', 'description']
    
    def get_conference(self, obj):
        return obj.track.conference.name
    get_conference.short_description = 'Conference'


class PaperAuthorInline(admin.TabularInline):
    model = PaperAuthor
    extra = 1
    fields = ['user', 'author_order', 'is_corresponding']


class ReviewAssignmentInline(admin.TabularInline):
    model = ReviewAssignment
    extra = 0
    fields = ['reviewer', 'status', 'assigned_at']
    readonly_fields = ['assigned_at']


@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = ['title', 'conference', 'track', 'status', 'submitted_at', 'num_reviews']
    list_filter = ['status', 'conference', 'track', 'submitted_at']
    search_fields = ['title', 'abstract']
    readonly_fields = ['id', 'submitted_at', 'updated_at']
    inlines = [PaperAuthorInline, ReviewAssignmentInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'conference', 'track', 'title', 'abstract', 'status')
        }),
        ('Files', {
            'fields': ('pdf_path', 'camera_ready_path')
        }),
        ('Timestamps', {
            'fields': ('submitted_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def num_reviews(self, obj):
        count = obj.review_assignments.filter(status='completed').count()
        total = obj.review_assignments.count()
        return f"{count}/{total}"
    num_reviews.short_description = 'Reviews'


@admin.register(Reviewer)
class ReviewerAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'get_email', 'expertise_preview']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'expertise']
    
    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'Name'
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
    
    def expertise_preview(self, obj):
        return obj.expertise[:100] + '...' if len(obj.expertise) > 100 else obj.expertise
    expertise_preview.short_description = 'Expertise'


@admin.register(ReviewAssignment)
class ReviewAssignmentAdmin(admin.ModelAdmin):
    list_display = ['paper', 'reviewer', 'status', 'assigned_at', 'has_review']
    list_filter = ['status', 'assigned_at', 'paper__conference']
    search_fields = ['paper__title', 'reviewer__user__username']
    readonly_fields = ['assigned_at']
    
    def has_review(self, obj):
        if hasattr(obj, 'review'):
            return format_html('<span style="color: green;">✓</span>')
        return format_html('<span style="color: red;">✗</span>')
    has_review.short_description = 'Review Submitted'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['get_paper_title', 'get_reviewer', 'score', 'confidence', 'submitted_at']
    list_filter = ['score', 'confidence', 'submitted_at']
    search_fields = ['assignment__paper__title', 'assignment__reviewer__user__username']
    readonly_fields = ['submitted_at', 'updated_at']
    
    fieldsets = (
        ('Assignment', {
            'fields': ('assignment',)
        }),
        ('Scores', {
            'fields': ('score', 'confidence')
        }),
        ('Comments', {
            'fields': ('comment_to_author', 'comment_to_chair')
        }),
        ('Timestamps', {
            'fields': ('submitted_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_paper_title(self, obj):
        return obj.assignment.paper.title
    get_paper_title.short_description = 'Paper'
    
    def get_reviewer(self, obj):
        return obj.assignment.reviewer.user.get_full_name()
    get_reviewer.short_description = 'Reviewer'


@admin.register(Decision)
class DecisionAdmin(admin.ModelAdmin):
    list_display = ['get_paper_title', 'result', 'decided_by', 'decided_at']
    list_filter = ['result', 'decided_at', 'paper__conference']
    search_fields = ['paper__title', 'justification']
    readonly_fields = ['decided_at']
    
    def get_paper_title(self, obj):
        return obj.paper.title
    get_paper_title.short_description = 'Paper'


class RolePermissionInline(admin.TabularInline):
    model = RolePermission
    extra = 1


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'role_type', 'num_permissions']
    list_filter = ['role_type']
    search_fields = ['name', 'description']
    inlines = [RolePermissionInline]
    
    def num_permissions(self, obj):
        return obj.permissions.count()
    num_permissions.short_description = 'Permissions'


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['code', 'description']
    search_fields = ['code', 'description']


@admin.register(UserConferenceRole)
class UserConferenceRoleAdmin(admin.ModelAdmin):
    list_display = ['user', 'conference', 'role', 'assigned_at']
    list_filter = ['role', 'conference', 'assigned_at']
    search_fields = ['user__username', 'user__email', 'conference__name']
    readonly_fields = ['assigned_at']


@admin.register(PolicySetting)
class PolicySettingAdmin(admin.ModelAdmin):
    list_display = ['conference', 'single_blind', 'double_blind', 'coi_enforced', 'ai_enabled']
    list_filter = ['single_blind', 'double_blind', 'coi_enforced', 'ai_enabled']
    search_fields = ['conference__name']


@admin.register(ConflictOfInterest)
class ConflictOfInterestAdmin(admin.ModelAdmin):
    list_display = ['get_paper_title', 'get_reviewer', 'reason_preview', 'declared_at']
    list_filter = ['declared_at', 'paper__conference']
    search_fields = ['paper__title', 'reviewer__user__username', 'reason']
    readonly_fields = ['declared_at']
    
    def get_paper_title(self, obj):
        return obj.paper.title
    get_paper_title.short_description = 'Paper'
    
    def get_reviewer(self, obj):
        return obj.reviewer.user.get_full_name()
    get_reviewer.short_description = 'Reviewer'
    
    def reason_preview(self, obj):
        return obj.reason[:50] + '...' if len(obj.reason) > 50 else obj.reason
    reason_preview.short_description = 'Reason'


@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    list_display = ['action', 'user', 'conference', 'level', 'created_at']
    list_filter = ['level', 'created_at', 'conference']
    search_fields = ['action', 'details', 'user__username']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Log Information', {
            'fields': ('action', 'level', 'user', 'conference')
        }),
        ('Details', {
            'fields': ('details',)
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'type', 'is_read', 'created_at']
    list_filter = ['type', 'is_read', 'created_at', 'conference']
    search_fields = ['title', 'message', 'user__username']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Notification Details', {
            'fields': ('user', 'conference', 'type', 'title', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'created_at')
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} notifications marked as read.')
    mark_as_read.short_description = 'Mark selected notifications as read'
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} notifications marked as unread.')
    mark_as_unread.short_description = 'Mark selected notifications as unread'
