from django.urls import path
from . import views
from .views import accepted_submisisons

urlpatterns = [
    path(
        "submission/accepted/",
        views.accepted_list,
        name="accepted-list"
    ),
    path(
        "program/",
        views.program_json,
        name="program-json"
    ),
    path(
        "accepted/",
        accepted_submisisons, 
        name="accepted-list",
    )
]