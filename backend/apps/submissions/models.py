from django.db import models
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from accounts.models import User
from conferences.models import Conference, Track, Topic

# Create your models here.

class Paper(models.Model):
    """
    Paper/Submission trong conference
    """
    PAPER_STATUS = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('revision_requested', 'Revision Requested'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    paper_id = models.AutoField(primary_key=True)
    
    # Conference relationship
    conference = models.ForeignKey(
        Conference,
        on_delete=models.CASCADE,
        related_name='papers'
    )
    
    # Track (optional)
    track = models.ForeignKey(
        Track,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='papers'
    )
    
    # Paper Information
    title = models.CharField(
        max_length=500,
        help_text="Paper title"
    )
    
    abstract = models.TextField(
        help_text="Paper abstract"
    )
    
    keywords = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma-separated keywords"
    )
    
    # Topics (many-to-many)
    topics = models.ManyToManyField(
        Topic,
        related_name='papers',
        blank=True
    )
    
    # File Upload
    pdf_file = models.FileField(
        upload_to='papers/%Y/%m/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text="Paper PDF file"
    )
    
    # Supplementary materials
    supplementary_file = models.FileField(
        upload_to='papers/supplementary/%Y/%m/',
        blank=True,
        null=True,
        help_text="Supplementary materials (code, data, etc.)"
    )
    
    # Authors
    authors = models.ManyToManyField(
        User,
        through='PaperAuthor',
        related_name='authored_papers'
    )
    
    # Submission info
    submitter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='submitted_papers',
        help_text="User who submitted the paper"
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=PAPER_STATUS,
        default='draft'
    )
    
    # Camera-ready version
    camera_ready_path = models.CharField(
        max_length=255,
        blank=True,
        help_text="Path to camera-ready version"
    )
    
    camera_ready_submitted_at = models.DateTimeField(
        null=True,
        blank=True
    )
    
    # AI Features
    ai_grammar_checked = models.BooleanField(default=False)
    ai_similarity_score = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Plagiarism similarity score (0-100%)"
    )
    ai_abstract_summary = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    
    # Soft delete
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'papers'
        ordering = ['-created_at']
        verbose_name = 'Paper'
        verbose_name_plural = 'Papers'
        indexes = [
            models.Index(fields=['conference', 'status']),
            models.Index(fields=['submitter', 'status']),
            models.Index(fields=['submitted_at']),
        ]
    
    def __str__(self):
        return f"{self.title[:50]} ({self.status})"
    
    def clean(self):
        """Validation"""
        # Check if conference accepts submissions
        if self.conference and not self.conference.is_submission_open():
            if self.status == 'submitted' and not self.pk:  # New submission
                raise ValidationError("Conference is not accepting submissions")
        
        # Check file size
        if self.pdf_file:
            max_size = self.conference.policy_settings.max_file_size_mb * 1024 * 1024
            if self.pdf_file.size > max_size:
                raise ValidationError(f"File size exceeds {self.conference.policy_settings.max_file_size_mb}MB")
    
    def submit(self):
        """Submit paper for review"""
        if self.status != 'draft':
            raise ValidationError("Can only submit papers in draft status")
        
        if not self.title or not self.abstract or not self.pdf_file:
            raise ValidationError("Paper must have title, abstract, and PDF file")
        
        # Check minimum authors
        if self.authors.count() < 1:
            raise ValidationError("Paper must have at least one author")
        
        self.status = 'submitted'
        self.submitted_at = timezone.now()
        self.save()
    
    def withdraw(self):
        """Withdraw paper"""
        if self.status not in ['submitted', 'under_review']:
            raise ValidationError("Can only withdraw submitted or under review papers")
        
        self.status = 'withdrawn'
        self.save()
    
    def accept(self):
        """Accept paper"""
        self.status = 'accepted'
        self.save()
    
    def reject(self):
        """Reject paper"""
        self.status = 'rejected'
        self.save()
    
    def request_revision(self):
        """Request revision"""
        self.status = 'revision_requested'
        self.save()
    
    def is_editable(self):
        """Check if paper can be edited"""
        return self.status in ['draft', 'revision_requested']
    
    def can_submit_camera_ready(self):
        """Check if can submit camera-ready version"""
        return self.status == 'accepted' and not self.camera_ready_path
    
    @property
    def author_list(self):
        """Get formatted author list"""
        return ", ".join([
            author.full_name or author.username 
            for author in self.authors.all()
        ])


class PaperAuthor(models.Model):
    """
    Many-to-many relationship với thông tin thêm
    """
    paper = models.ForeignKey(
        Paper,
        on_delete=models.CASCADE,
        related_name='paper_authors'
    )
    
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_papers'
    )
    
    order = models.IntegerField(
        default=1,
        help_text="Author order (1 = first author)"
    )
    
    is_corresponding = models.BooleanField(
        default=False,
        help_text="Is corresponding author?"
    )
    
    affiliation_override = models.CharField(
        max_length=255,
        blank=True,
        help_text="Override affiliation for this paper only"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'paper_authors'
        unique_together = ['paper', 'author']
        ordering = ['paper', 'order']
    
    def __str__(self):
        return f"{self.author.full_name} - {self.paper.title[:30]}"


class PaperVersion(models.Model):
    """
    Version history của paper (khi có revision)
    """
    version_id = models.AutoField(primary_key=True)
    
    paper = models.ForeignKey(
        Paper,
        on_delete=models.CASCADE,
        related_name='versions'
    )
    
    version_number = models.IntegerField(
        validators=[MinValueValidator(1)]
    )
    
    pdf_file = models.FileField(
        upload_to='papers/versions/%Y/%m/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    
    changes_summary = models.TextField(
        blank=True,
        help_text="Summary of changes from previous version"
    )
    
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='uploaded_versions'
    )
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'paper_versions'
        unique_together = ['paper', 'version_number']
        ordering = ['paper', '-version_number']
    
    def __str__(self):
        return f"{self.paper.title[:30]} - v{self.version_number}"


class CameraReadySubmission(models.Model):
    """
    Camera-ready submission (final version sau khi accept)
    """
    camera_ready_id = models.AutoField(primary_key=True)
    
    paper = models.OneToOneField(
        Paper,
        on_delete=models.CASCADE,
        related_name='camera_ready'
    )
    
    pdf_file = models.FileField(
        upload_to='papers/camera-ready/%Y/%m/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    
    source_files = models.FileField(
        upload_to='papers/camera-ready/source/%Y/%m/',
        blank=True,
        null=True,
        help_text="Source files (LaTeX, Word, etc.)"
    )
    
    copyright_form = models.FileField(
        upload_to='papers/camera-ready/copyright/%Y/%m/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    
    final_title = models.CharField(max_length=500)
    final_abstract = models.TextField()
    
    submitted_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='camera_ready_submissions'
    )
    
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    # Validation status
    is_validated = models.BooleanField(default=False)
    validation_notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'camera_ready_submissions'
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"Camera-ready: {self.paper.title[:30]}"


class Metadata(models.Model):
    """
    Additional metadata cho paper
    """
    metadata_id = models.AutoField(primary_key=True)
    
    paper = models.OneToOneField(
        Paper,
        on_delete=models.CASCADE,
        related_name='metadata'
    )
    
    # Additional info
    paper_type = models.CharField(
        max_length=50,
        choices=[
            ('full', 'Full Paper'),
            ('short', 'Short Paper'),
            ('poster', 'Poster'),
            ('demo', 'Demo'),
            ('workshop', 'Workshop Paper'),
        ],
        default='full'
    )
    
    # Research area
    primary_area = models.CharField(max_length=100, blank=True)
    secondary_area = models.CharField(max_length=100, blank=True)
    
    # Funding
    funding_source = models.TextField(
        blank=True,
        help_text="Funding acknowledgments"
    )
    
    # Ethics
    ethics_approval_required = models.BooleanField(default=False)
    ethics_approval_number = models.CharField(max_length=100, blank=True)
    
    # Data availability
    data_available = models.BooleanField(default=False)
    data_url = models.URLField(blank=True)
    
    # Code availability
    code_available = models.BooleanField(default=False)
    code_url = models.URLField(blank=True)
    
    # Preprint
    is_preprint = models.BooleanField(default=False)
    preprint_url = models.URLField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'paper_metadata'
    
    def __str__(self):
        return f"Metadata: {self.paper.title[:30]}"


class SubmissionActivity(models.Model):
    """
    Activity log cho submissions
    """
    ACTIVITY_TYPES = [
        ('created', 'Paper Created'),
        ('updated', 'Paper Updated'),
        ('submitted', 'Paper Submitted'),
        ('withdrawn', 'Paper Withdrawn'),
        ('file_uploaded', 'File Uploaded'),
        ('author_added', 'Author Added'),
        ('author_removed', 'Author Removed'),
        ('status_changed', 'Status Changed'),
    ]
    
    activity_id = models.AutoField(primary_key=True)
    
    paper = models.ForeignKey(
        Paper,
        on_delete=models.CASCADE,
        related_name='activities'
    )
    
    activity_type = models.CharField(
        max_length=50,
        choices=ACTIVITY_TYPES
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='submission_activities'
    )
    
    description = models.TextField()
    
    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional activity data"
    )
    
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'submission_activities'
        ordering = ['-created_at']
        verbose_name_plural = 'Submission Activities'
    
    def __str__(self):
        return f"{self.activity_type} - {self.paper.title[:30]}"