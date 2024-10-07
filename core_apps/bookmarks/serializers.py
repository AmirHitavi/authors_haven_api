from rest_framework import serializers

from .models import Bookmark


class BookmarkSerializer(serializers.ModelSerializer):
    article_title = serializers.CharField(source="article.title", read_only=True)
    user_fullname = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Bookmark
        fields = ["id", "article_title", "user_fullname", "created_at"]

    def get_user_fullname(self, obj):
        return f"{obj.user.first_name.title()} f{obj.user.last_name.title()}"
