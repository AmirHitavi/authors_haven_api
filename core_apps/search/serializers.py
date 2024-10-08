from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from .document import ArticleDocument


class ArticleDocumentSerializer(DocumentSerializer):
    """Serializer for the article document."""

    class Meta:
        document = ArticleDocument
        fields = ["title", "author", "slug", "description", "body", "created_at"]
