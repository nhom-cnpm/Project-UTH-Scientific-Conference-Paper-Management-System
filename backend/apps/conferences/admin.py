from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Conference, Track, Topic, ConferenceTrackTopic, PolicySetting, SystemLog

# Register your models here.


@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = [
        'conference_id',
        'name',
        'acronym',
        'status_badge',
        'start_date',
        'submission_deadline',
        'days_remaining',
        'chair',
    ]
    
    list_filter = [
        'status',
        'start_date',
        'is_online',
        'is_hybrid',
        'created_at',
    ]
    
    search_fields = [
        'name',
        'acronym',
        'description',
        'venue',
        'city',
    ]
    
    readonly_fields = [
        'created_at',
        'updated_at',
        'conference_id'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'conference_id',
                'name',
                'acronym',
                'description',
                'website',
            )
        }),
        ('Dates & Deadlines', {
            'fields': (
                'start_date',
                'end_date',
                'submission_deadline',
                'review_deadline',
                'camera_ready_deadline',
            )
        }),
        ('Location', {
            'fields': (
                'venue',
                'city',
                'country',
                'is_online',
                'is_hybrid',
            )
        }),
        ('Organization', {
            'fields': (
                'chair',
                'status',
            )
        }),
        ('Settings', {
            'fields': (
                'max_papers_per_author',
                'max_reviewers_per_paper',
                'enable_ai_grammar_check',
                'enable_ai_abstract_summary',
                'enable_ai_similarity_check',
            ),
            'classes': ('collapse',)
        }),
        ('System', {
            'fields': (
                'is_deleted',
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'draft': 'gray',
            'open': 'green',
            'review': 'blue',
            'decision': 'orange',
            'completed': 'purple',
            'archived': 'black',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def days_remaining(self, obj):
        if obj.is_past_deadline():
            return format_html('<span style="color: red;">Closed</span>')
        days = obj.days_until_deadline()
        if days <= 7:
            color = 'red'
        elif days <= 30:
            color = 'orange'
        else:
            color = 'green'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} days</span>',
            color,
            days
        )
    days_remaining.short_description = 'Days Until Deadline'
    
    actions = ['open_submission', 'close_submission', 'complete_conference']
    
    def open_submission(self, request, queryset):
        count = 0
        for conference in queryset:
            try:
                conference.open_for_submission()
                count += 1
            except:
                pass
        self.message_user(request, f'{count} conferences opened for submission.')
    open_submission.short_description = 'Open for submission'
    
    def close_submission(self, request, queryset):
        count = 0
        for conference in queryset:
            try:
                conference.close_submission()
                count += 1
            except:
                pass
        self.message_user(request, f'{count} conferences closed submission.')
    close_submission.short_description = 'Close submission'
    
    def complete_conference(self, request, queryset):
        count = queryset.update(status='completed')
        self.message_user(request, f'{count} conferences marked as completed.')
    complete_conference.short_description = 'Mark as completed'


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = [
        'track_id',
        'conference',
        'name',
        'chair',
        'is_active',
        'created_at'
    ]
    
    list_filter = [
        'is_active',
        'created_at',
    ]
    
    search_fields = [
        'name',
        'conference__name',
        'description',
    ]
    
    readonly_fields = ['created_at']


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = [
        'topic_id',
        'name',
        'parent',
        'is_active',
        'created_at'
    ]
    
    list_filter = [
        'is_active',
        'parent',
    ]
    
    search_fields = ['name', 'description']
    
    readonly_fields = ['created_at']


@admin.register(ConferenceTrackTopic)
class ConferenceTrackTopicAdmin(admin.ModelAdmin):
    list_display = ['conference', 'track', 'topic']
    list_filter = ['conference']
    search_fields = ['conference__name', 'topic__name']


@admin.register(PolicySetting)
class PolicySettingAdmin(admin.ModelAdmin):
    list_display = [
        'policy_id',
        'conference',
        'max_paper_pages',
        'min_reviews_per_paper',
        'require_anonymous_submission',
        'updated_at'
    ]
    
    search_fields = ['conference__name']
    
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Conference', {
            'fields': ('conference',)
        }),
        ('Submission Policies', {
            'fields': (
                'allow_multiple_submissions',
                'require_anonymous_submission',
                'max_paper_pages',
                'min_paper_pages',
            )
        }),
        ('Review Policies', {
            'fields': (
                'min_reviews_per_paper',
                'allow_reviewer_discussion',
            )
        }),
        ('COI Policies', {
            'fields': (
                'require_coi_declaration',
                'auto_exclude_coauthors',
            )
        }),
        ('Decision Policies', {
            'fields': (
                'require_consensus',
            )
        }),
        ('File Settings', {
            'fields': (
                'allowed_file_formats',
                'max_file_size_mb',
            )
        }),
        ('Notifications', {
            'fields': (
                'send_confirmation_email',
                'send_reminder_emails',
                'reminder_days_before',
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    list_display = [
        'log_id',
        'conference',
        'log_type',
        'user',
        'ip_address',
        'created_at'
    ]
    
    list_filter = [
        'log_type',
        'created_at',
    ]
    
    search_fields = [
        'conference__name',
        'user__email',
        'description',
    ]
    
    readonly_fields = ['created_at']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False