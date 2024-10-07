from django.core.files.storage import default_storage
from django.http import Http404
from django.shortcuts import get_object_or_404
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from .exceptions import YouAlreadyClapped
from .filters import ArticleFilter
from .models import Article, ArticleView, Clap
from .pagination import ArticlePagination
from .permissions import IsAuthorOrReadOnly
from .renderers import ArticleJSONRenderer, ArticlesJSONRenderer
from .serializers import ArticleSerializer, ClapSerializer

# Create your views here.


class ArticleListCreateAPIView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    renderer_classes = [ArticlesJSONRenderer]
    pagination_class = ArticlePagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filter_class = ArticleFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArticleRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    lookup_field = "id"
    renderer_classes = [ArticleJSONRenderer]
    parser_classes = [MultiPartParser, FormParser]

    def perform_update(self, serializer):
        instance = serializer.save(author=self.request.user)
        if "banner_image" in self.request.FILES:
            if (
                instance["banner_image"]
                and instance["banner_image"].name != "./default_banner.png"
            ):
                default_storage.delete(instance.banner_image.path)
                instance.banner_image == self.request.FILES["banner_image"]
                instance.save()

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)

        viewer_ip = request.GET.get("REMOTE_ADDR", None)

        ArticleView.record(viewer_ip=viewer_ip, article=instance, user=request.user)

        return Response(serializer.data)


class ClapCreateDestroyAPIView(generics.CreateAPIView, generics.DestroyAPIView):
    queryset = Clap.objects.all()
    serializer_class = ClapSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        article_id = kwargs.get("article_id")
        article = get_object_or_404(Article, id=article_id)

        if Clap.objects.filter(article=article, user=user).exists():
            raise YouAlreadyClapped()

        clap = Clap.objects.create(article=article, user=user)
        clap.save()

        return Response(
            {
                "status_code": status.HTTP_201_CREATED,
                "detail": "clap added to article.",
            },
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request, *args, **kwargs):
        user = request.user
        article_id = kwargs.get("article_id")
        article = get_object_or_404(Article, id=article_id)

        clap = get_object_or_404(Clap, article=article, user=user)
        clap.delete()

        return Response(
            {
                "status_code": status.HTTP_204_NO_CONTENT,
                "detail": "clap deleted from article.",
            },
            status=status.HTTP_204_NO_CONTENT,
        )
