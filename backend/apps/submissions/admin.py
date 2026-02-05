from django.contrib import admin
from .models import Submission, Topic

# Register your models here.
@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("id", "title",  "topic", "status", "paper_id", "camera_ready_deadline")
    list_filter = ("status",)
    search_fields = ("title", "paper_id")