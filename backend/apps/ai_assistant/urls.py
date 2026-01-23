from django.urls import path
from . import views

urlpatterns = [
    path("grammar-check/", views.GrammarCheckView.as_view(), name="grammar-check"),
    path("summary/", views.AbstractSummaryView.as_view(), name="abstract-summary"),
    path("similarity/", views.SimilarityCheckView.as_view(), name="similarity-check"),
]
