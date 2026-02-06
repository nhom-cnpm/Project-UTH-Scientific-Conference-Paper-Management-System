from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    Paper, PaperAuthor, PaperVersion, 
    CameraReadySubmission, Metadata, SubmissionActivity
)

# Register your models here.
class PaperAuthorInline(admin.TabularInline):
    """Inline để hiển thị authors trong Paper admin"""
    model = PaperAuthor
    extra = 1
    fields = ['author', 'order', 'is_corresponding', 'affiliation_override']
    autocomplete_fields = ['author']


@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = [
        'paper_id',
        'title_short',
        'conference',
        'track',
        'submitter',
        'status_badge',
        'submitted_at',
        'author_count',
    ]
    
    list_filter = [
        'status',
        'conference',
        'track',
        'submitted_at',
        'created_at',
    ]
    
    search_fields = [
        'title',
        'abstract',
        'keywords',
        'submitter__email',
        'authors__email',
    ]
    
    readonly_fields = [
        'paper_id',
        'created_at',
        'updated_at',
        'submitted_at',
        'camera_ready_submitted_at',
    ]
    
    autocomplete_fields = ['conference', 'track', 'submitter', 'topics']
    
    inlines = [PaperAuthorInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'paper_id',
                'conference',
                'track',
                'title',
                'abstract',
                'keywords',
                'topics',
            )
        }),
        ('Files', {
            'fields': (
                'pdf_file',
                'supplementary_file',
            )
        }),
        ('Submission', {
            'fields': (
                'submitter',
                'status',
                'submitted_at',
            )
        }),
        ('Camera Ready', {
            'fields': (
                'camera_ready_path',
                'camera_ready_submitted_at',
            ),
            'classes': ('collapse',)
        }),
        ('AI Features', {
            'fields': (
                'ai_grammar_checked',
                'ai_similarity_score',
                'ai_abstract_summary',
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
    
    def title_short(self, obj):
        return obj.title[:60] + '...' if len(obj.title) > 60 else obj.title
    title_short.short_description = 'Title'
    
    def status_badge(self, obj):
        colors = {
            'draft': 'gray',
            'submitted': 'blue',
            'under_review': 'orange',
            'revision_requested': 'purple',
            'accepted': 'green',
            'rejected': 'red',
            'withdrawn': 'black',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def author_count(self, obj):
        count = obj.authors.count()
        return format_html(
            '<span style="font-weight: bold;">{}</span>',
            count
        )
    author_count.short_description = 'Authors'
    
    actions = ['accept_papers', 'reject_papers', 'request_revision']
    
    def accept_papers(self, request, queryset):
        count = 0
        for paper in queryset:
            try:
                paper.accept()
                count += 1
            except:
                pass
        self.message_user(request, f'{count} papers accepted.')
    accept_papers.short_description = 'Accept selected papers'
    
    def reject_papers(self, request, queryset):
        count = 0
        for paper in queryset:
            try:
                paper.reject()
                count += 1
            except:
                pass
        self.message_user(request, f'{count} papers rejected.')
    reject_papers.short_description = 'Reject selected papers'
    
    def request_revision(self, request, queryset):
        count = 0
        for paper in queryset:
            try:
                paper.request_revision()
                count += 1
            except:
                pass
        self.message_user(request, f'{count} papers marked for revision.')
    request_revision.short_description = 'Request revision'


@admin.register(PaperAuthor)
class PaperAuthorAdmin(admin.ModelAdmin):
    list_display = [
        'author',
        'paper_title',
        'order',
        'is_corresponding',
        'created_at'
    ]
    
    list_filter = [
        'is_corresponding',
        'created_at',
    ]
    
    search_fields = [
        'author__email',
        'author__full_name',
        'paper__title',
    ]
    
    autocomplete_fields = ['paper', 'author']
    
    def paper_title(self, obj):
        return obj.paper.title[:50]
    paper_title.short_description = 'Paper'


@admin.register(PaperVersion)
class PaperVersionAdmin(admin.ModelAdmin):
    list_display = [
        'version_id',
        'paper_title',
        'version_number',
        'uploaded_by',
        'uploaded_at'
    ]
    
    list_filter = [
        'version_number',
        'uploaded_at',
    ]
    
    search_fields = [
        'paper__title',
        'uploaded_by__email',
    ]
    
    readonly_fields = ['uploaded_at']
    
    autocomplete_fields = ['paper', 'uploaded_by']
    
    def paper_title(self, obj):
        return obj.paper.title[:50]
    paper_title.short_description = 'Paper'


@admin.register(CameraReadySubmission)
class CameraReadySubmissionAdmin(admin.ModelAdmin):
    list_display = [
        'camera_ready_id',
        'paper_title',
        'submitted_by',
        'submitted_at',
        'is_validated',
    ]
    
    list_filter = [
        'is_validated',
        'submitted_at',
    ]
    
    search_fields = [
        'paper__title',
        'final_title',
        'submitted_by__email',
    ]
    
    readonly_fields = ['submitted_at']
    
    autocomplete_fields = ['paper', 'submitted_by']
    
    def paper_title(self, obj):
        return obj.paper.title[:50]
    paper_title.short_description = 'Paper'


@admin.register(Metadata)
class MetadataAdmin(admin.ModelAdmin):
    list_display = [
        'metadata_id',
        'paper_title',
        'paper_type',
        'data_available',
        'code_available',
    ]
    
    list_filter = [
        'paper_type',
        'data_available',
        'code_available',
        'ethics_approval_required',
    ]
    
    search_fields = [
        'paper__title',
        'primary_area',
        'secondary_area',
    ]
    
    readonly_fields = ['created_at', 'updated_at']
    
    autocomplete_fields = ['paper']
    
    def paper_title(self, obj):
        return obj.paper.title[:50]
    paper_title.short_description = 'Paper'


@admin.register(SubmissionActivity)
class SubmissionActivityAdmin(admin.ModelAdmin):
    list_display = [
        'activity_id',
        'paper_title',
        'activity_type',
        'user',
        'ip_address',
        'created_at'
    ]
    
    list_filter = [
        'activity_type',
        'created_at',
    ]
    
    search_fields = [
        'paper__title',
        'user__email',
        'description',
    ]
    
    readonly_fields = ['created_at']
    
    autocomplete_fields = ['paper', 'user']
    
    def paper_title(self, obj):
        return obj.paper.title[:50]
    paper_title.short_description = 'Paper'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


