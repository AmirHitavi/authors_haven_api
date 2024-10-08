from django.urls import path

from .views import ArticleSearchView

urlpatterns = [
    path("article/", ArticleSearchView.as_view({"get": "list"}), name="article-search")
]
