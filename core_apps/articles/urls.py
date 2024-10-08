from django.urls import path

from .views import (
    ArticleListCreateAPIView,
    ArticleRetrieveUpdateDestroyAPIView,
    ClapCreateDestroyAPIView,
)

urlpatterns = [
    path("", ArticleListCreateAPIView.as_view(), name="article-list-create"),
    path(
        "<uuid:id>/",
        ArticleRetrieveUpdateDestroyAPIView.as_view(),
        name="article-retrieve-update-destroy",
    ),
    path(
        "<uuid:article_id>/clap/",
        ClapCreateDestroyAPIView.as_view(),
        name="clap-create-destroy",
    ),
]
