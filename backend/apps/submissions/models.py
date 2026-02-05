from django.db import models
from django.utils import timezone
import random
# Create your models here.
class Topic (models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
def generate_unique_paper_id():
    while True:
        paper_id = f"{random.randint(1000,9999)}"
        if not Submission.objects.filter(paper_id=paper_id).exists():
            return paper_id
class Submission(models.Model):
    STATUS_CHOICES = [
        ("submitted", "Submitted"),
        ("under_review", "Under Review"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("camera_ready", "Camera Ready"),
    ]
    title = models.CharField(max_length=255)
    topic = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="submitted"
    )
    paper_id=models.CharField(
        max_length=4,
        unique=True,
        editable=False,
        default=generate_unique_paper_id
        )
    camera_ready_deadline = models.DateTimeField(null=True, blank=True)
    camera_ready_file = models.FileField(
        upload_to="camera_ready/",
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.paper_id or 'NO-ID'} | {self.title}"

