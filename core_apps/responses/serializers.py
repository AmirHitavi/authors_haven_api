from rest_framework import serializers

from .models import Response


class ResponseSerializer(serializers.ModelSerializer):
    user_fullname = serializers.SerializerMethodField(read_only=True)
    article_title = serializers.CharField(source="article.title", read_only=True)

    class Meta:
        model = Response
        fields = [
            "id",
            "user_fullname",
            "article_title",
            "content",
            "parent",
            "created_at",
        ]

    def get_user_fullname(self, obj):
        return f"{obj.user.first_name.title()} {obj.user.last_name.title()}"
