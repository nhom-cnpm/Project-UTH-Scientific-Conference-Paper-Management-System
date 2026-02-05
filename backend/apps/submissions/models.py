from django.db import models

# Create your models here.
class Submission(models.Model):
    STATUS_CHOICES = [
        ("submitted", "Submitted"),
        ("under_review", "Under Review"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("camera_ready", "Camera Ready"),
    ]
    title = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="submitted",
        db_index = True
    )
    paper_id=models.CharField(max_length=30, null=True, blank=True)
    camera_ready_dealine = models.DateTimeField(null=True, blank=True)
    camere_ready_file = models.FileField(
        upload_to="camera_ready/",
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
<<<<<<< HEAD
        indexes = [models.Index(fields=["status"]), models.Index(fields=["paper_id"]),]
=======
        indexes = [models.Index(fields=["status"]), models.Index(fields=["paper_id"]),]
=======
# Create your models here.
>>>>>>> main
>>>>>>> b5d226157563910d980209022b3b2b6e8baa647a
