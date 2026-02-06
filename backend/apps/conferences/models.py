from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from accounts.models import User


# Create your models here.
class Conference(models.Model):
    CONFERENCE_STATUS = [
        ('draft', 'Draft'),
        ('open', 'Open for Submission'),
        ('review', 'In Review'),
        ('decision', 'Decision Making'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ]
    
    conference_id = models.AutoField(primary_key=True)
    
    # Basic Information
    name = models.CharField(
        max_length=255,
        help_text="Conference name"
    )
    
    acronym = models.CharField(
        max_length=50,
        blank=True,
        help_text="Short name/acronym (e.g., ICML, NeurIPS)"
    )
    
    description = models.TextField(
        help_text="Detailed conference description"
    )
    
    # Dates
    start_date = models.DateField(
        help_text="Conference start date"
    )
    
    end_date = models.DateField(
        help_text="Conference end date"
    )
    
    # Submission Deadlines
    submission_deadline = models.DateTimeField(
        help_text="Paper submission deadline"
    )
    
    review_deadline = models.DateTimeField(
        help_text="Review submission deadline"
    )
    
    camera_ready_deadline = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Camera-ready submission deadline"
    )
    
    # Location
    venue = models.CharField(
        max_length=255,
        help_text="Conference venue/location"
    )
    
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    
    # Online/Hybrid
    is_online = models.BooleanField(default=False)
    is_hybrid = models.BooleanField(default=False)
    
    # Conference Website
    website = models.URLField(blank=True)
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=CONFERENCE_STATUS,
        default='draft'
    )
    
    # Organizers
    chair = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='chaired_conferences',
        help_text="Program Chair"
    )
    
    # Settings
    max_papers_per_author = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1)]
    )
    
    max_reviewers_per_paper = models.IntegerField(
        default=3,
        validators=[MinValueValidator(1)]
    )
    
    # AI Features
    enable_ai_grammar_check = models.BooleanField(default=True)
    enable_ai_abstract_summary = models.BooleanField(default=True)
    enable_ai_similarity_check = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Soft delete
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'conferences'
        ordering = ['-start_date']
        verbose_name = 'Conference'
        verbose_name_plural = 'Conferences'
        indexes = [
            models.Index(fields=['status', 'start_date']),
            models.Index(fields=['submission_deadline']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.start_date.year})"
    
    def clean(self):
        """Validation"""
        # End date phải sau start date
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError("End date must be after start date")
        
        # Review deadline phải sau submission deadline
        if self.review_deadline and self.submission_deadline:
            if self.review_deadline <= self.submission_deadline:
                raise ValidationError("Review deadline must be after submission deadline")
        
        # Camera ready phải sau review deadline
        if self.camera_ready_deadline and self.review_deadline:
            if self.camera_ready_deadline <= self.review_deadline:
                raise ValidationError("Camera-ready deadline must be after review deadline")
    
    def is_submission_open(self):
        """Kiểm tra có đang mở submission không"""
        now = timezone.now()
        return (
            self.status == 'open' and
            now <= self.submission_deadline
        )
    
    def is_review_open(self):
        """Kiểm tra có đang trong review phase không"""
        now = timezone.now()
        return (
            self.status == 'review' and
            now <= self.review_deadline
        )
    
    def is_past_deadline(self):
        """Kiểm tra đã qua deadline chưa"""
        return timezone.now() > self.submission_deadline
    
    def days_until_deadline(self):
        """Số ngày còn lại đến deadline"""
        if self.is_past_deadline():
            return 0
        delta = self.submission_deadline - timezone.now()
        return delta.days
    
    def open_for_submission(self):
        """Mở conference cho submission"""
        if self.status != 'draft':
            raise ValidationError("Can only open conference from draft status")
        self.status = 'open'
        self.save()
    
    def close_submission(self):
        """Đóng submission, chuyển sang review"""
        if self.status != 'open':
            raise ValidationError("Can only close submission from open status")
        self.status = 'review'
        self.save()
    
    def complete(self):
        """Hoàn thành conference"""
        self.status = 'completed'
        self.save()
    
    def archive(self):
        """Archive conference"""
        self.status = 'archived'
        self.save()


class Track(models.Model):
    """
    Track/Topic trong conference (ví dụ: AI, ML, NLP, etc.)
    """
    track_id = models.AutoField(primary_key=True)
    
    conference = models.ForeignKey(
        Conference,
        on_delete=models.CASCADE,
        related_name='tracks'
    )
    
    name = models.CharField(
        max_length=255,
        help_text="Track name (e.g., Machine Learning, Computer Vision)"
    )
    
    description = models.TextField(blank=True)
    
    # Track chair
    chair = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='chaired_tracks'
    )
    
    # Settings
    max_papers = models.IntegerField(
        null=True,
        blank=True,
        help_text="Maximum papers for this track (optional)"
    )
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'tracks'
        unique_together = ['conference', 'name']
        ordering = ['conference', 'name']
    
    def __str__(self):
        return f"{self.conference.acronym} - {self.name}"


class Topic(models.Model):
    """
    Topic/Keywords cho paper
    """
    topic_id = models.AutoField(primary_key=True)
    
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Topic name (e.g., Deep Learning, Reinforcement Learning)"
    )
    
    description = models.TextField(blank=True)
    
    # Parent topic (for hierarchical topics)
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subtopics'
    )
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'topics'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class ConferenceTrackTopic(models.Model):
    """
    Many-to-many relationship: Conference có nhiều tracks và topics
    """
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE, null=True, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'conference_track_topics'
        unique_together = ['conference', 'track', 'topic']
    
    def __str__(self):
        return f"{self.conference.name} - {self.topic.name}"


class PolicySetting(models.Model):
    """
    Chính sách và cài đặt cho conference
    """
    policy_id = models.AutoField(primary_key=True)
    
    conference = models.OneToOneField(
        Conference,
        on_delete=models.CASCADE,
        related_name='policy_settings'
    )
    
    # Submission Policies
    allow_multiple_submissions = models.BooleanField(
        default=True,
        help_text="Allow authors to submit multiple papers"
    )
    
    require_anonymous_submission = models.BooleanField(
        default=True,
        help_text="Double-blind review (anonymous submission)"
    )
    
    max_paper_pages = models.IntegerField(
        default=8,
        validators=[MinValueValidator(1)]
    )
    
    min_paper_pages = models.IntegerField(
        default=4,
        validators=[MinValueValidator(1)]
    )
    
    # Review Policies
    min_reviews_per_paper = models.IntegerField(
        default=3,
        validators=[MinValueValidator(1)]
    )
    
    allow_reviewer_discussion = models.BooleanField(
        default=True,
        help_text="Allow reviewers to discuss papers"
    )
    
    # COI Policies
    require_coi_declaration = models.BooleanField(
        default=True,
        help_text="Require conflict of interest declaration"
    )
    
    auto_exclude_coauthors = models.BooleanField(
        default=True,
        help_text="Automatically exclude co-authors as reviewers"
    )
    
    # Decision Policies
    require_consensus = models.BooleanField(
        default=False,
        help_text="Require consensus among reviewers"
    )
    
    # File Format
    allowed_file_formats = models.JSONField(
        default=list,
        help_text="Allowed file formats (e.g., ['pdf', 'docx'])"
    )
    
    max_file_size_mb = models.IntegerField(
        default=10,
        validators=[MinValueValidator(1)],
        help_text="Maximum file size in MB"
    )
    
    # Notifications
    send_confirmation_email = models.BooleanField(default=True)
    send_reminder_emails = models.BooleanField(default=True)
    reminder_days_before = models.IntegerField(default=7)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'policy_settings'
    
    def __str__(self):
        return f"Policy Settings for {self.conference.name}"
    
    def clean(self):
        """Validation"""
        if self.min_paper_pages > self.max_paper_pages:
            raise ValidationError("Min pages cannot be greater than max pages")


class SystemLog(models.Model):
    """
    System logs cho conference (audit trail)
    """
    LOG_TYPES = [
        ('conference_created', 'Conference Created'),
        ('conference_updated', 'Conference Updated'),
        ('submission_opened', 'Submission Opened'),
        ('submission_closed', 'Submission Closed'),
        ('review_started', 'Review Phase Started'),
        ('decision_made', 'Decision Made'),
        ('system_backup', 'System Backup'),
        ('system_restore', 'System Restore'),
    ]
    
    log_id = models.AutoField(primary_key=True)
    
    conference = models.ForeignKey(
        Conference,
        on_delete=models.CASCADE,
        related_name='system_logs'
    )
    
    log_type = models.CharField(
        max_length=50,
        choices=LOG_TYPES
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='conference_logs'
    )
    
    description = models.TextField()
    
    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional metadata"
    )
    
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'system_logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['conference', 'log_type']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.log_type} - {self.conference.name} at {self.created_at}"