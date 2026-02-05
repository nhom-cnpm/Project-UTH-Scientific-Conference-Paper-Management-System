from django.urls import path
from . import views

urlpatterns = [
    path(
        "<int:submission_id>/decision/",
        views.decision_submission,
        name="decision-submission"
    ),
    path(
        "<int:submission_id>/camera-ready/",
        views.upload_camera_ready,
        name="camera-ready"
    ),
]