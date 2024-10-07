from django.urls import path

from .views import RatingCreateAPIView

urlpatterns = [
    path(
        "rate_article/<uuid:article_id>/",
        RatingCreateAPIView.as_view(),
        name="rate-article",
    )
]
