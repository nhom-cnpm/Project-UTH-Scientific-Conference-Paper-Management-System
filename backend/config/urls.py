from django.urls import path, include

urlpatterns = [
    path("api/conferences/", include("apps.conferences.urls")),
]
