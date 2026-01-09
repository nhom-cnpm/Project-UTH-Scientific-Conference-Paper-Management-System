from django.db import models

# Create your models here.

# Gia Bảo
class Submission(models.Model):
    STATUS_CHOICES = [
        ("submitted", "Submitted"),
        ("under_review", "Under Review"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("camera_ready", "Camera Ready"),
    ]
    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE
    )#