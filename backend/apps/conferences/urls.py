from django.urls import path
from .views import ConferenceListCreateView

urlpatterns = [
    path("", ConferenceListCreateView.as_view(), name="conference-list"),
]

