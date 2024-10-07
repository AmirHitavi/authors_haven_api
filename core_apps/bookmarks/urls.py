from django.urls import path

from .views import BookmarkDestroyAPIView, BookmarkListCreateAPIView

urlpatterns = [
    path(
        "create-bookmark-article/<uuid:article_id>/",
        BookmarkListCreateAPIView.as_view(),
        name="create-bookmark-article",
    ),
    path(
        "destroy-bookmark-article/<uuid:article_id>/",
        BookmarkDestroyAPIView.as_view(),
        name="destroy-bookmark-article",
    ),
]
