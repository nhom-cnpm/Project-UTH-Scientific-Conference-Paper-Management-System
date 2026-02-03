from django.conf import settings
from django.db import models

from apps.conferences.models import Conference

class Review(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    conference = models.ForeignKey(
        Conference,
        on_delete=models.CASCADE,
        related_name='reviewers'
    )

    def __str__(self):
        return self.name


from django.core.validators import MinValueValidator, MaxValueValidator


from conferences.models import Paper

User = settings.AUTH_USER_MODEL


class ReviewAssignment(models.Model):
    STATUS_CHOICES = [
        ("assigned", "assigned"),
        ("completed", "completed"),
        ("declined", "declined"),
    ]

    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, related_name="review_assignments")
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review_assignments")

    assigned_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_review_assignments"
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="assigned")
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("paper", "reviewer")

    def __str__(self):
        return f"paper={self.paper_id} reviewer={self.reviewer_id} status={self.status}"


class Review(models.Model):
    assignment = models.OneToOneField(ReviewAssignment, on_delete=models.CASCADE, related_name="review")
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"assignment={self.assignment_id} score={self.score}"
