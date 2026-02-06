from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from accounts.models import User
from conferences.models import Conference
from submissions.models import Paper

# Create your models here.
class Proceedings(models.Model):
    """
    Proceedings - Kỷ yếu hội nghị (tập hợp các papers đã accept)
    """
    PROCEEDINGS_STATUS = [
        ('draft', 'Draft'),
        ('in_preparation', 'In Preparation'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    proceedings_id = models.AutoField(primary_key=True)
    
    conference = models.OneToOneField(
        Conference,
        on_delete=models.CASCADE,
        related_name='proceedings'
    )
    
    # Proceedings Information
    title = models.CharField(
        max_length=500,
        help_text="Proceedings title"
    )
    
    subtitle = models.CharField(
        max_length=500,
        blank=True
    )
    
    isbn = models.CharField(
        max_length=20,
        blank=True,
        help_text="ISBN number"
    )
    
    doi_prefix = models.CharField(
        max_length=50,
        blank=True,
        help_text="DOI prefix (e.g., 10.1234)"
    )
    
    # Publisher Information
    publisher = models.CharField(
        max_length=255,
        blank=True,
        help_text="Publisher name (e.g., Springer, IEEE)"
    )
    
    publisher_location = models.CharField(
        max_length=255,
        blank=True
    )
    
    # Publication Date
    publication_date = models.DateField(
        null=True,
        blank=True,
        help_text="Official publication date"
    )
    
    # Volume and Series
    volume_number = models.CharField(
        max_length=50,
        blank=True
    )
    
    series_name = models.CharField(
        max_length=255,
        blank=True,
        help_text="Series name (e.g., LNCS)"
    )
    
    # Files
    cover_image = models.ImageField(
        upload_to='proceedings/covers/%Y/',
        blank=True,
        null=True,
        help_text="Proceedings cover image"
    )
    
    full_proceedings_pdf = models.FileField(
        upload_to='proceedings/pdf/%Y/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text="Complete proceedings PDF"
    )
    
    # Editors
    editors = models.ManyToManyField(
        User,
        through='ProceedingsEditor',
        related_name='edited_proceedings'
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=PROCEEDINGS_STATUS,
        default='draft'
    )
    
    # Metadata
    description = models.TextField(blank=True)
    keywords = models.CharField(max_length=500, blank=True)
    
    # Statistics
    total_pages = models.IntegerField(
        default=0,
        help_text="Total number of pages"
    )
    
    total_papers = models.IntegerField(
        default=0,
        help_text="Total number of papers included"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    # Soft delete
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'proceedings'
        verbose_name = 'Proceedings'
        verbose_name_plural = 'Proceedings'
        ordering = ['-publication_date']
    
    def __str__(self):
        return f"{self.title} ({self.conference.acronym})"
    
    def clean(self):
        """Validation"""
        if self.publication_date and self.conference:
            if self.publication_date < self.conference.end_date:
                raise ValidationError(
                    "Publication date should be after conference end date"
                )
    
    def publish(self):
        """Publish proceedings"""
        if self.status != 'in_preparation':
            raise ValidationError("Can only publish proceedings in preparation")
        
        if not self.full_proceedings_pdf:
            raise ValidationError("Proceedings PDF is required for publication")
        
        self.status = 'published'
        self.published_at = timezone.now()
        self.save()
    
    def generate_table_of_contents(self):
        """Generate table of contents"""
        entries = self.entries.filter(is_included=True).order_by('page_start')
        return entries
    
    def calculate_statistics(self):
        """Calculate and update statistics"""
        entries = self.entries.filter(is_included=True)
        
        self.total_papers = entries.count()
        
        # Calculate total pages
        total = 0
        for entry in entries:
            if entry.page_start and entry.page_end:
                total += (entry.page_end - entry.page_start + 1)
        
        self.total_pages = total
        self.save(update_fields=['total_papers', 'total_pages'])


class ProceedingsEditor(models.Model):
    """
    Editors của proceedings
    """
    proceedings = models.ForeignKey(
        Proceedings,
        on_delete=models.CASCADE,
        related_name='editor_assignments'
    )
    
    editor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='proceedings_editor_roles'
    )
    
    role = models.CharField(
        max_length=100,
        default='Editor',
        help_text="Editor role (e.g., Chief Editor, Associate Editor)"
    )
    
    order = models.IntegerField(
        default=1,
        help_text="Display order"
    )
    
    affiliation_override = models.CharField(
        max_length=255,
        blank=True,
        help_text="Override affiliation for this proceedings"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'proceedings_editors'
        unique_together = ['proceedings', 'editor']
        ordering = ['proceedings', 'order']
    
    def __str__(self):
        return f"{self.editor.full_name} - {self.role}"


class ProceedingsEntry(models.Model):
    """
    Entry/Paper trong proceedings
    """
    entry_id = models.AutoField(primary_key=True)
    
    proceedings = models.ForeignKey(
        Proceedings,
        on_delete=models.CASCADE,
        related_name='entries'
    )
    
    paper = models.OneToOneField(
        Paper,
        on_delete=models.CASCADE,
        related_name='proceedings_entry',
        help_text="Accepted paper to include"
    )
    
    # Page numbers
    page_start = models.IntegerField(
        null=True,
        blank=True,
        help_text="Starting page number"
    )
    
    page_end = models.IntegerField(
        null=True,
        blank=True,
        help_text="Ending page number"
    )
    
    # DOI
    doi = models.CharField(
        max_length=100,
        blank=True,
        help_text="DOI for this paper"
    )
    
    # Order in proceedings
    display_order = models.IntegerField(
        default=1,
        help_text="Display order in proceedings"
    )
    
    # Section (optional)
    section = models.CharField(
        max_length=255,
        blank=True,
        help_text="Section/Chapter (e.g., 'Machine Learning')"
    )
    
    # Inclusion status
    is_included = models.BooleanField(
        default=True,
        help_text="Include in final proceedings"
    )
    
    # Final PDF
    final_pdf = models.FileField(
        upload_to='proceedings/papers/%Y/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text="Final formatted PDF"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'proceedings_entries'
        verbose_name = 'Proceedings Entry'
        verbose_name_plural = 'Proceedings Entries'
        ordering = ['proceedings', 'display_order']
        unique_together = ['proceedings', 'paper']
    
    def __str__(self):
        return f"{self.paper.title} (pp. {self.page_start}-{self.page_end})"
    
    def clean(self):
        """Validation"""
        # Check paper is accepted
        if self.paper.status != 'accepted':
            raise ValidationError("Only accepted papers can be included in proceedings")
        
        # Check page numbers
        if self.page_start and self.page_end:
            if self.page_end < self.page_start:
                raise ValidationError("End page must be >= start page")
    
    @property
    def page_count(self):
        """Calculate number of pages"""
        if self.page_start and self.page_end:
            return self.page_end - self.page_start + 1
        return 0
    
    def generate_doi(self):
        """Generate DOI for this entry"""
        if self.proceedings.doi_prefix:
            # Format: {doi_prefix}/{conference_year}.{entry_id}
            year = self.proceedings.conference.start_date.year
            self.doi = f"{self.proceedings.doi_prefix}/{year}.{self.entry_id}"
            self.save(update_fields=['doi'])
            return self.doi
        return None


class Section(models.Model):
    """
    Section/Chapter trong proceedings
    """
    section_id = models.AutoField(primary_key=True)
    
    proceedings = models.ForeignKey(
        Proceedings,
        on_delete=models.CASCADE,
        related_name='sections'
    )
    
    name = models.CharField(
        max_length=255,
        help_text="Section name (e.g., 'Deep Learning', 'NLP')"
    )
    
    description = models.TextField(blank=True)
    
    order = models.IntegerField(
        default=1,
        help_text="Display order"
    )
    
    # Optional section editor
    section_editor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='edited_sections'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'proceedings_sections'
        unique_together = ['proceedings', 'name']
        ordering = ['proceedings', 'order']
    
    def __str__(self):
        return f"{self.name} - {self.proceedings.title}"
    
    def get_entries(self):
        """Get all entries in this section"""
        return ProceedingsEntry.objects.filter(
            proceedings=self.proceedings,
            section=self.name,
            is_included=True
        ).order_by('display_order')


class ExportHistory(models.Model):
    """
    History của proceedings exports
    """
    EXPORT_FORMATS = [
        ('pdf', 'PDF'),
        ('epub', 'EPUB'),
        ('xml', 'XML'),
        ('bibtex', 'BibTeX'),
    ]
    
    export_id = models.AutoField(primary_key=True)
    
    proceedings = models.ForeignKey(
        Proceedings,
        on_delete=models.CASCADE,
        related_name='exports'
    )
    
    export_format = models.CharField(
        max_length=20,
        choices=EXPORT_FORMATS
    )
    
    file_path = models.FileField(
        upload_to='proceedings/exports/%Y/%m/',
        help_text="Exported file"
    )
    
    exported_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='proceedings_exports'
    )
    
    file_size = models.BigIntegerField(
        default=0,
        help_text="File size in bytes"
    )
    
    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text="Export metadata"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'proceedings_exports'
        ordering = ['-created_at']
        verbose_name_plural = 'Export Histories'
    
    def __str__(self):
        return f"{self.export_format.upper()} export of {self.proceedings.title}"


class Copyright(models.Model):
    """
    Copyright information cho papers trong proceedings
    """
    copyright_id = models.AutoField(primary_key=True)
    
    entry = models.OneToOneField(
        ProceedingsEntry,
        on_delete=models.CASCADE,
        related_name='copyright_info'
    )
    
    copyright_holder = models.CharField(
        max_length=255,
        help_text="Copyright holder (usually authors or publisher)"
    )
    
    copyright_year = models.IntegerField(
        help_text="Copyright year"
    )
    
    license_type = models.CharField(
        max_length=100,
        blank=True,
        help_text="License type (e.g., CC BY 4.0, All Rights Reserved)"
    )
    
    license_url = models.URLField(
        blank=True,
        help_text="URL to license text"
    )
    
    copyright_statement = models.TextField(
        blank=True,
        help_text="Full copyright statement"
    )
    
    # Copyright form
    copyright_form_signed = models.BooleanField(
        default=False,
        help_text="Copyright form signed by authors"
    )
    
    copyright_form_file = models.FileField(
        upload_to='proceedings/copyright/%Y/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text="Signed copyright form"
    )
    
    signed_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'proceedings_copyrights'
    
    def __str__(self):
        return f"Copyright: {self.entry.paper.title}"