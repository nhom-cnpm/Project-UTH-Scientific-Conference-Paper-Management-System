from django.db import models

# Create your models here.
class conferences(models.Model):
    title = models.charField(max_length=200)
    content = models.textField()
    created_at = models.dateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title