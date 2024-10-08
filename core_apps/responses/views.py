from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404

from core_apps.articles.models import Article

from .models import Response
from .serializers import ResponseSerializer

# Create your views here.


class ResponseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        article_id = self.kwargs.get("article_id")
        return Response.objects.filter(article__id=article_id, parent=None)

    def perform_create(self, serializer):
        user = self.request.user
        article_id = self.kwargs.get("article_id")
        article = get_object_or_404(Article, id=article_id)
        serializer.save(article=article, user=user)


class ResponseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
    lookup_field = "id"

    def perform_update(self, serializer):
        user = self.request.user
        response = self.get_object()

        if user != response.user:
            raise PermissionDenied("You do not have permission to edit this response.")

        serializer.save()

    def perform_destroy(self, serializer):
        user = self.request.user
        response = self.get_object()

        if user != response.user:
            raise PermissionDenied(
                "You do not have permission to delete this response."
            )

        serializer.delete()
