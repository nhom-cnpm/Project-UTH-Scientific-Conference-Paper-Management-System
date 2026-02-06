from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Proceedings, ProceedingsEditor, ProceedingsEntry,
    Section, ExportHistory, Copyright
)
# Register your models here.

class ProceedingsEditorInline(admin.TabularInline):
    """Inline cho editors"""
    model = ProceedingsEditor
    extra = 1
    fields = ['editor', 'role', 'order', 'affiliation_override']
    autocomplete_fields = ['editor']


class ProceedingsEntryInline(admin.TabularInline):
    """Inline cho entries"""
    model = ProceedingsEntry
    extra = 0
    fields = ['paper', 'page_start', 'page_end', 'section', 'display_order', 'is_included']
    readonly_fields = ['paper']
    autocomplete_fields = ['paper']


@admin.register(Proceedings)
class ProceedingsAdmin(admin.ModelAdmin):
    list_display = [
        'proceedings_id',
        'title_short',
        'conference',
        'status_badge',
        'publication_date',
        'total_papers',
        'total_pages',
    ]
    
    list_filter = [
        'status',
        'publication_date',
        'publisher',
        'created_at',
    ]
    
    search_fields = [
        'title',
        'subtitle',
        'conference__name',
        'isbn',
        'publisher',
    ]
    
    readonly_fields = [
        'proceedings_id',
        'created_at',
        'updated_at',
        'published_at',
    ]
    
    autocomplete_fields = ['conference']
    
    inlines = [ProceedingsEditorInline, ProceedingsEntryInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'proceedings_id',
                'conference',
                'title',
                'subtitle',
                'description',
            )
        }),
        ('Publication Details', {
            'fields': (
                'isbn',
                'doi_prefix',
                'publisher',
                'publisher_location',
                'publication_date',
            )
        }),
        ('Volume & Series', {
            'fields': (
                'volume_number',
                'series_name',
            )
        }),
        ('Files', {
            'fields': (
                'cover_image',
                'full_proceedings_pdf',
            )
        }),
        ('Status & Statistics', {
            'fields': (
                'status',
                'total_papers',
                'total_pages',
                'keywords',
            )
        }),
        ('Timestamps', {
            'fields': (
                'created_at',
                'updated_at',
                'published_at',
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
            'in_preparation': 'orange',
            'published': 'green',
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
    
    actions = ['publish_proceedings', 'calculate_stats']
    
    def publish_proceedings(self, request, queryset):
        count = 0
        for proceedings in queryset:
            try:
                proceedings.publish()
                count += 1
            except:
                pass
        self.message_user(request, f'{count} proceedings published.')
    publish_proceedings.short_description = 'Publish selected proceedings'
    
    def calculate_stats(self, request, queryset):
        for proceedings in queryset:
            proceedings.calculate_statistics()
        self.message_user(request, 'Statistics updated.')
    calculate_stats.short_description = 'Calculate statistics'


@admin.register(ProceedingsEditor)
class ProceedingsEditorAdmin(admin.ModelAdmin):
    list_display = ['editor', 'proceedings_title', 'role', 'order']
    list_filter = ['role']
    search_fields = ['editor__email', 'proceedings__title']
    autocomplete_fields = ['proceedings', 'editor']
    
    def proceedings_title(self, obj):
        return obj.proceedings.title[:50]
    proceedings_title.short_description = 'Proceedings'


@admin.register(ProceedingsEntry)
class ProceedingsEntryAdmin(admin.ModelAdmin):
    list_display = [
        'entry_id',
        'paper_title',
        'proceedings_title',
        'page_range',
        'section',
        'display_order',
        'is_included',
    ]
    
    list_filter = [
        'is_included',
        'section',
        'proceedings',
    ]
    
    search_fields = [
        'paper__title',
        'proceedings__title',
        'section',
        'doi',
    ]
    
    readonly_fields = ['created_at', 'updated_at', 'page_count']
    
    autocomplete_fields = ['proceedings', 'paper']
    
    fieldsets = (
        ('Entry Information', {
            'fields': (
                'proceedings',
                'paper',
                'section',
                'display_order',
            )
        }),
        ('Pages', {
            'fields': (
                'page_start',
                'page_end',
                'page_count',
            )
        }),
        ('DOI & Files', {
            'fields': (
                'doi',
                'final_pdf',
            )
        }),
        ('Status', {
            'fields': (
                'is_included',
            )
        }),
        ('Timestamps', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',)
        }),
    )
    
    def paper_title(self, obj):
        return obj.paper.title[:50]
    paper_title.short_description = 'Paper'
    
    def proceedings_title(self, obj):
        return obj.proceedings.title[:50]
    proceedings_title.short_description = 'Proceedings'
    
    def page_range(self, obj):
        if obj.page_start and obj.page_end:
            return f"{obj.page_start}-{obj.page_end} ({obj.page_count} pp.)"
        return "-"
    page_range.short_description = 'Pages'
    
    actions = ['generate_dois']
    
    def generate_dois(self, request, queryset):
        count = 0
        for entry in queryset:
            if entry.generate_doi():
                count += 1
        self.message_user(request, f'{count} DOIs generated.')
    generate_dois.short_description = 'Generate DOIs'


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['section_id', 'name', 'proceedings_title', 'order', 'section_editor']
    list_filter = ['proceedings']
    search_fields = ['name', 'proceedings__title']
    autocomplete_fields = ['proceedings', 'section_editor']
    
    def proceedings_title(self, obj):
        return obj.proceedings.title[:50]
    proceedings_title.short_description = 'Proceedings'


@admin.register(ExportHistory)
class ExportHistoryAdmin(admin.ModelAdmin):
    list_display = [
        'export_id',
        'proceedings_title',
        'export_format',
        'exported_by',
        'file_size_mb',
        'created_at'
    ]
    
    list_filter = ['export_format', 'created_at']
    search_fields = ['proceedings__title', 'exported_by__email']
    readonly_fields = ['created_at']
    autocomplete_fields = ['proceedings', 'exported_by']
    
    def proceedings_title(self, obj):
        return obj.proceedings.title[:50]
    proceedings_title.short_description = 'Proceedings'
    
    def file_size_mb(self, obj):
        return f"{obj.file_size / (1024 * 1024):.2f} MB"
    file_size_mb.short_description = 'File Size'


@admin.register(Copyright)
class CopyrightAdmin(admin.ModelAdmin):
    list_display = [
        'copyright_id',
        'entry_paper',
        'copyright_holder',
        'copyright_year',
        'license_type',
        'form_signed',
    ]
    
    list_filter = ['copyright_form_signed', 'copyright_year', 'license_type']
    search_fields = ['copyright_holder', 'entry__paper__title']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['entry']
    
    def entry_paper(self, obj):
        return obj.entry.paper.title[:50]
    entry_paper.short_description = 'Paper'
    
    def form_signed(self, obj):
        if obj.copyright_form_signed:
            return format_html('<span style="color: green;">✓ Signed</span>')
        return format_html('<span style="color: red;">✗ Not Signed</span>')
    form_signed.short_description = 'Form Status'