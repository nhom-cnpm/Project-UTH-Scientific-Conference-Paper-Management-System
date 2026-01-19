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

