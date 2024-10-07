from rest_framework import serializers

from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    article_title = serializers.CharField(source="article.title", read_only=True)
    user_fullname = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Rating
        fields = ["id", "article_title", "user_fullname", "rating", "review"]

    def get_user_fullname(self, obj):
        return f"{obj.user.first_name.title()} {obj.user.last_name.title()}"
