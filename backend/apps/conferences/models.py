from django.db import models

class Conference(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    deadline = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
