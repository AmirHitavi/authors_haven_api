from django.urls import path

from .views import ArticleListCreateAPIView, ArticleRetrieveUpdateDestroyAPIView

urlpatterns = [
    path("", ArticleListCreateAPIView.as_view(), name="article-list-create"),
    path(
        "<uuid:id>/",
        ArticleRetrieveUpdateDestroyAPIView.as_view(),
        name="article-retrieve-update-destroy",
    ),
]
