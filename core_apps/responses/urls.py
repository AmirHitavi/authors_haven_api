from django.urls import path

from .views import ResponseListCreateAPIView, ResponseRetrieveUpdateDestroyAPIView

urlpatterns = [
    path(
        "article/<uuid:article_id>/",
        ResponseListCreateAPIView.as_view(),
        name="article-responses",
    ),
    path(
        "<uuid:id>/",
        ResponseRetrieveUpdateDestroyAPIView.as_view(),
        name="article-details",
    ),
]
