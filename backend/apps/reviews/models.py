from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.

class ReviewAssignment(models.Model):
    """
    Phân công reviewer cho paper
    Một paper có thể được assign cho nhiều reviewer
    Một reviewer không thể được assign cho cùng 1 paper 2 lần
    """
    ASSIGNMENT_STATUS = [
        ('pending', 'Pending'),           # Chờ reviewer phản hồi
        ('accepted', 'Accepted'),         # Reviewer đã chấp nhận
        ('declined', 'Declined'),         # Reviewer từ chối
        ('coi_declared', 'COI Declared'), # Xung đột lợi ích
    ]
    
    assignment_id = models.AutoField(primary_key=True)
    
    paper = models.ForeignKey(
        'papers.Paper',
        on_delete=models.CASCADE,
        related_name='review_assignments'
    )
    
    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review_assignments',
        limit_choices_to={'groups__name__in': ['Reviewer', 'PC Member']}
    )
    
    status = models.CharField(
        max_length=20,
        choices=ASSIGNMENT_STATUS,
        default='pending'
    )
    
    assigned_at = models.DateTimeField(auto_now_add=True)
    response_date = models.DateTimeField(null=True, blank=True)
    
    # Deadline cho review
    review_deadline = models.DateTimeField(null=True, blank=True)
    
    # Lý do từ chối hoặc COI
    decline_reason = models.TextField(blank=True)
    coi_reason = models.TextField(blank=True)
    
    # Assigned by (Chair/Admin)
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='assignments_created'
    )
    
    class Meta:
        db_table = 'review_assignments'
        unique_together = ['paper', 'reviewer']
        ordering = ['-assigned_at']
        verbose_name = 'Review Assignment'
        verbose_name_plural = 'Review Assignments'
        indexes = [
            models.Index(fields=['status', 'assigned_at']),
            models.Index(fields=['reviewer', 'status']),
        ]
    
    def __str__(self):
        return f"Assignment #{self.assignment_id}: {self.paper.title[:40]} → {self.reviewer.username}"
    
    def clean(self):
        """Validation trước khi save"""
        # Kiểm tra reviewer không phải là tác giả
        if self.paper.authors.filter(id=self.reviewer.id).exists():
            raise ValidationError("Reviewer không thể là tác giả của paper này")
    
    def accept(self):
        """Reviewer chấp nhận review"""
        if self.status != 'pending':
            raise ValidationError("Chỉ có thể accept assignment ở trạng thái pending")
        
        self.status = 'accepted'
        self.response_date = timezone.now()
        self.save()
        return True
    
    def decline(self, reason=""):
        """Reviewer từ chối review"""
        if self.status != 'pending':
            raise ValidationError("Chỉ có thể decline assignment ở trạng thái pending")
        
        self.status = 'declined'
        self.decline_reason = reason
        self.response_date = timezone.now()
        self.save()
        return True
    
    def declare_coi(self, reason):
        """Khai báo xung đột lợi ích"""
        if not reason:
            raise ValidationError("Lý do COI là bắt buộc")
        
        if self.status not in ['pending', 'accepted']:
            raise ValidationError("Không thể khai báo COI ở trạng thái này")
        
        self.status = 'coi_declared'
        self.coi_reason = reason
        self.response_date = timezone.now()
        self.save()
        return True
    
    def is_overdue(self):
        """Kiểm tra có quá hạn không"""
        if self.review_deadline and self.status == 'accepted':
            return timezone.now() > self.review_deadline
        return False
    
    def can_create_review(self):
        """Kiểm tra có thể tạo review không"""
        return self.status == 'accepted'


class Review(models.Model):
    """
    Review chi tiết của reviewer cho paper
    Một assignment chỉ có 1 review
    """
    REVIEW_STATUS = [
        ('draft', 'Draft'),               # Đang soạn thảo
        ('submitted', 'Submitted'),       # Đã submit
        ('revised', 'Revised'),           # Đã chỉnh sửa
        ('finalized', 'Finalized'),       # Đã hoàn tất
    ]
    
    CONFIDENCE_LEVEL = [
        (1, 'Low - Not confident'),
        (2, 'Medium - Somewhat confident'),
        (3, 'High - Very confident'),
        (4, 'Expert - Absolutely confident'),
    ]
    
    RECOMMENDATION = [
        ('strong_accept', 'Strong Accept'),
        ('accept', 'Accept'),
        ('weak_accept', 'Weak Accept'),
        ('borderline', 'Borderline'),
        ('weak_reject', 'Weak Reject'),
        ('reject', 'Reject'),
        ('strong_reject', 'Strong Reject'),
    ]
    
    review_id = models.AutoField(primary_key=True)
    
    assignment = models.OneToOneField(
        ReviewAssignment,
        on_delete=models.CASCADE,
        related_name='review'
    )
    
    # Điểm đánh giá (1-10)
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Overall score: 1 (worst) - 10 (best)"
    )
    
    # Recommendation
    recommendation = models.CharField(
        max_length=20,
        choices=RECOMMENDATION,
        help_text="Recommendation for paper acceptance"
    )
    
    # Mức độ tự tin
    confidence_level = models.IntegerField(
        choices=CONFIDENCE_LEVEL,
        default=2,
        help_text="Reviewer's confidence level"
    )
    
    # Nội dung review chi tiết
    content_review = models.TextField(
        help_text="Detailed review (strengths, weaknesses, suggestions)"
    )
    
    # Comment cho tác giả (public)
    comment_to_author = models.TextField(
        help_text="Comments visible to authors",
        blank=True
    )
    
    # Comment cho Chair (confidential)
    comment_to_chair = models.TextField(
        help_text="Confidential comments for chairs only",
        blank=True
    )
    
    # Trạng thái
    status = models.CharField(
        max_length=20,
        choices=REVIEW_STATUS,
        default='draft'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    finalized_at = models.DateTimeField(null=True, blank=True)
    
    # Soft delete
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'reviews'
        ordering = ['-created_at']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        indexes = [
            models.Index(fields=['status', 'submitted_at']),
        ]
    
    def __str__(self):
        return f"Review #{self.review_id} by {self.reviewer.username} - Score: {self.score}"
    
    def clean(self):
        """Validation"""
        if self.assignment.status != 'accepted':
            raise ValidationError("Chỉ có thể tạo review khi assignment đã được accepted")
        
        if self.status in ['submitted', 'finalized']:
            if not self.content_review or not self.score or not self.recommendation:
                raise ValidationError("Content, score và recommendation là bắt buộc")
    
    @property
    def reviewer(self):
        return self.assignment.reviewer
    
    @property
    def paper(self):
        return self.assignment.paper
    
    def submit(self):
        """Submit review"""
        if self.status == 'finalized':
            raise ValidationError("Review đã finalized, không thể submit lại")
        
        if not self.content_review or not self.score or not self.recommendation:
            raise ValidationError("Vui lòng điền đầy đủ thông tin review")
        
        self.status = 'submitted'
        self.submitted_at = timezone.now()
        self.save()
        return True
    
    def revise(self):
        """Cho phép chỉnh sửa lại"""
        if self.status == 'finalized':
            raise ValidationError("Review đã finalized, không thể revise")
        
        self.status = 'revised'
        self.save()
        return True
    
    def finalize(self):
        """Finalize review - Chair only"""
        if self.status not in ['submitted', 'revised']:
            raise ValidationError("Chỉ có thể finalize review đã submitted")
        
        self.status = 'finalized'
        self.finalized_at = timezone.now()
        self.save()
        return True
    
    def is_editable(self):
        """Kiểm tra có thể edit không"""
        return self.status in ['draft', 'revised'] and not self.is_deleted


class ReviewDiscussion(models.Model):
    """
    Thảo luận nội bộ giữa reviewers và chairs
    """
    discussion_id = models.AutoField(primary_key=True)
    
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='discussions'
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review_discussions'
    )
    
    message = models.TextField()
    
    # Reply to another discussion (threading)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'review_discussions'
        ordering = ['created_at']
        verbose_name = 'Review Discussion'
        verbose_name_plural = 'Review Discussions'
    
    def __str__(self):
        return f"Discussion by {self.user.username} on Review #{self.review.review_id}"