from django.urls import path

from .views import ArticleSearchView, ProfileSearchView

urlpatterns = [
    path("article/", ArticleSearchView.as_view({"get": "list"}), name="article-search"),
    path("profile/", ProfileSearchView.as_view({"get": "list"}), name="profile-search"),
]
