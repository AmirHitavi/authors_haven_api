from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from .document import ArticleDocument, ProfileDocument


class ArticleDocumentSerializer(DocumentSerializer):
    """Serializer for the article document."""

    class Meta:
        document = ArticleDocument
        fields = ["title", "author", "slug", "description", "body", "created_at"]


class ProfileDocumentSerializer(DocumentSerializer):
    """Serializer for the profile document."""

    class Meta:
        document = ArticleDocument
        fields = [
            "user",
            "phone_number",
            "gender",
            "country",
            "city",
            "profile_photo",
            "twitter_handle",
            "followers_count",
        ]

    def get_user(self, obj):
        """Custom method to serialize user data."""
        return {
            "email": obj.user.email,
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
            "date_joined": obj.user.date_joined,
        }
