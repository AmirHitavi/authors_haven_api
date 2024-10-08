from django_elasticsearch_dsl_drf.filter_backends import (
    DefaultOrderingFilterBackend,
    FilteringFilterBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    SearchFilterBackend,
)
from django_elasticsearch_dsl_drf.pagination import PageNumberPagination
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from rest_framework import permissions

from .document import ArticleDocument
from .serializers import ArticleDocumentSerializer

# Create your views here.


class ArticleSearchView(DocumentViewSet):
    document = ArticleDocument
    serializer_class = ArticleDocumentSerializer
    pagination_class = PageNumberPagination
    permission_classes = [permissions.AllowAny]
    lookup_field = "id"
    filter_backends = [
        FilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]
    # Define search fields
    search_fields = [
        "title",
        "description",
        "body",
        "author_first_name",
        "author_last_name",
        "tags",
    ]
    # Define filter fields
    filter_fields = {"slug": "slug.raw", "tags": "tags", "created_at": "created_at"}
    # Define ordering fields
    ordering_fields = {"created_at": "created_at"}
    # Specify default ordering
    ordering = ["created_at"]
