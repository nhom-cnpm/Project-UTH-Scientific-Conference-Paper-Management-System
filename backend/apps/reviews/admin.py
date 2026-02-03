from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.core.exceptions import ValidationError  
from .models import ReviewAssignment, Review, ReviewDiscussion

# Register your models here.
@admin.register(ReviewAssignment)
class ReviewAssignmentAdmin(admin.ModelAdmin):
    list_display = [
        'assignment_id',
        'get_paper_link',
        'get_reviewer',
        'status_badge',
        'assigned_at',
        'review_deadline',
        'overdue_indicator',
        'has_review'
    ]
    
    list_filter = [
        'status',
        'assigned_at',
        'review_deadline',
    ]
    
    search_fields = [
        'paper__title',
        'reviewer__username',
        'reviewer__email',
    ]
    
    readonly_fields = [
        'assigned_at',
        'response_date',
        'assignment_id'
    ]
    
    fieldsets = (
        ('Assignment Information', {
            'fields': (
                'assignment_id',
                'paper',
                'reviewer',
                'assigned_by',
                'review_deadline'
            )
        }),
        ('Status', {
            'fields': (
                'status',
                'assigned_at',
                'response_date',
            )
        }),
        ('Reasons', {
            'fields': (
                'decline_reason',
                'coi_reason',
            ),
            'classes': ('collapse',)
        }),
    )
    
    def get_paper_link(self, obj):
        url = reverse('admin:papers_paper_change', args=[obj.paper.id])
        return format_html('<a href="{}">{}</a>', url, obj.paper.title[:50])
    get_paper_link.short_description = 'Paper'
    
    def get_reviewer(self, obj):
        return f"{obj.reviewer.get_full_name()} ({obj.reviewer.username})"
    get_reviewer.short_description = 'Reviewer'
    
    def status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'accepted': 'green',
            'declined': 'red',
            'coi_declared': 'gray',
        }
        color = colors.get(obj.status, 'blue')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def overdue_indicator(self, obj):
        if obj.is_overdue():
            return format_html('<span style="color: red; font-weight: bold;">⚠ OVERDUE</span>')
        return '✓'
    overdue_indicator.short_description = 'Deadline Status'
    
    def has_review(self, obj):
        try:
            obj.review
            return format_html('<span style="color: green;">✓ Yes</span>')
        except Review.DoesNotExist:
            return format_html('<span style="color: gray;">✗ No</span>')
    has_review.short_description = 'Review Submitted'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'review_id',
        'get_paper',
        'get_reviewer',
        'score',
        'recommendation',
        'confidence_level',
        'status_badge',
        'submitted_at',
        'is_deleted'
    ]
    
    list_filter = [
        'status',
        'recommendation',
        'confidence_level',
        'score',
        'submitted_at',
        'is_deleted'
    ]
    
    search_fields = [
        'assignment__paper__title',
        'assignment__reviewer__username',
        'content_review',
    ]
    
    readonly_fields = [
        'review_id',
        'created_at',
        'updated_at',
        'submitted_at',
        'finalized_at'
    ]
    
    fieldsets = (
        ('Review Information', {
            'fields': (
                'review_id',
                'assignment',
                'status',
            )
        }),
        ('Evaluation', {
            'fields': (
                'score',
                'recommendation',
                'confidence_level',
            )
        }),
        ('Content', {
            'fields': (
                'content_review',
                'comment_to_author',
                'comment_to_chair',
            )
        }),
        ('Timestamps', {
            'fields': (
                'created_at',
                'updated_at',
                'submitted_at',
                'finalized_at',
            ),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_deleted',)
        }),
    )
    
    def get_paper(self, obj):
        return obj.paper.title[:50]
    get_paper.short_description = 'Paper'
    
    def get_reviewer(self, obj):
        return obj.reviewer.username
    get_reviewer.short_description = 'Reviewer'
    
    def status_badge(self, obj):
        colors = {
            'draft': 'gray',
            'submitted': 'blue',
            'revised': 'orange',
            'finalized': 'green',
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    actions = ['finalize_reviews']
    
    def finalize_reviews(self, request, queryset):
        """Bulk finalize reviews"""
        count = 0
        for review in queryset:
            try:
                review.finalize()
                count += 1
            except ValidationError:
                pass
        self.message_user(request, f'{count} reviews đã được finalized.')
    finalize_reviews.short_description = 'Finalize selected reviews'


@admin.register(ReviewDiscussion)
class ReviewDiscussionAdmin(admin.ModelAdmin):
    list_display = [
        'discussion_id',
        'get_review',
        'user',
        'message_preview',
        'created_at',
        'is_deleted'
    ]
    
    list_filter = [
        'created_at',
        'is_deleted',
    ]
    
    search_fields = [
        'user__username',
        'message',
        'review__assignment__paper__title',
    ]
    
    readonly_fields = ['created_at', 'updated_at']
    
    def get_review(self, obj):
        return f"Review #{obj.review.review_id}"
    get_review.short_description = 'Review'
    
    def message_preview(self, obj):
        return obj.message[:100] + '...' if len(obj.message) > 100 else obj.message
    message_preview.short_description = 'Message'