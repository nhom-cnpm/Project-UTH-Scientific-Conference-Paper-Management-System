from django.urls import path
from .views import AssignReviewerView, MyAssignedPapersView, SubmitReviewView

urlpatterns = [
    path("assign/", AssignReviewerView.as_view(), name="assign-reviewer"),
    path("my-assignments/", MyAssignedPapersView.as_view(), name="my-assignments"),
    path("submit/", SubmitReviewView.as_view(), name="submit-review"),
]
