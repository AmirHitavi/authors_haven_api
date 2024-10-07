from uuid import UUID

from django.db import IntegrityError
from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound, ValidationError

from core_apps.articles.models import Article

from .exceptions import YouAlreadyHaveBookmarked
from .models import Bookmark
from .serializers import BookmarkSerializer

# Create your views here.


class BookmarkListCreateAPIView(generics.ListCreateAPIView):
    queryset = Bookmark.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookmarkSerializer

    def perform_create(self, serializer):
        article_id = self.kwargs.get("article_id")
        if article_id:
            try:
                article = Article.objects.get(id=article_id)
            except Article.DoesNotExist:
                raise ValidationError("Invalid 'article_id' provided")
        else:
            raise ValidationError("'article_id' is required.")

        try:
            serializer.save(article=article, user=self.request.user)
        except IntegrityError:
            raise YouAlreadyHaveBookmarked()


class BookmarkDestroyAPIView(generics.DestroyAPIView):
    queryset = Bookmark.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def get_object(self):
        user = self.request.user
        article_id = self.kwargs.get("article_id")

        try:
            UUID(str(article_id), version=4)
        except ValueError:
            raise ValidationError("Invalid 'article_id' provided.")

        try:
            bookmark = Bookmark.objects.get(article__id=article_id, user=user)
        except Bookmark.DoesNotExist:
            raise NotFound("Bookmark not found or it doesn't belong to you.")

        return bookmark

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise ValidationError("You cannot delete a bookmark that is not yours.")
        instance.delete()
