from rest_framework import serializers
from taggit.models import Tag

from core_apps.bookmarks.models import Bookmark
from core_apps.bookmarks.serializers import BookmarkSerializer
from core_apps.profiles.serializers import ProfileSerializer

from .models import Article, ArticleView


class TagListField(serializers.Field):
    def to_representation(self, value):
        return [tag.name for tag in value.all()]

    def to_internal_value(self, data):
        if not isinstance(data, list):
            raise serializers.ValidationError("Expected a list of tags.")

        tag_objs = []
        for tag_name in data:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tag_objs.append(tag)
        return tag_objs


class ArticleSerializer(serializers.ModelSerializer):
    author_info = ProfileSerializer(source="author.profile", read_only=True)
    banner_image = serializers.SerializerMethodField()
    estimated_reading_time = serializers.ReadOnlyField()
    tags = TagListField()
    views = serializers.SerializerMethodField()
    average_rating = serializers.ReadOnlyField()
    bookmarks = serializers.SerializerMethodField()
    bookmarks_count = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_banner_image(self, obj):
        return obj.banner_image.url

    def get_views(self, obj):
        return ArticleView.objects.filter(article=obj).count()

    def get_average_rating(self, obj):
        return obj.average_rating()

    def get_bookmarks(self, obj):
        bookmarks = Bookmark.objects.filter(article=obj)
        return BookmarkSerializer(bookmarks, many=True).data

    def get_bookmarks_count(self, obj):
        return Bookmark.objects.filter(article=obj).count()

    def get_created_at(self, obj):
        now = obj.created_at
        return now.strftime("%Y-%m-%d: %H:%M:%S")

    def get_updated_at(self, obj):
        time = obj.updated_at
        return time.strftime("%Y-%m-%d: %H:%M:%S")

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "slug",
            "estimated_reading_time",
            "average_rating",
            "bookmarks",
            "bookmarks_count",
            "body",
            "description",
            "author_info",
            "banner_image",
            "tags",
            "views",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        tags = validated_data.pop("tags")
        article = Article.objects.create(**validated_data)
        article.tags.set(tags)
        article.save()
        return article

    def update(self, instance, validated_data):
        instance.author = validated_data.get("author", instance.author)
        instance.title = validated_data.get("title", instance.title)
        instance.body = validated_data.get("body", instance.body)
        instance.description = validated_data.get("description", instance.description)
        instance.banner_image = validated_data.get(
            "banner_image", instance.banner_image
        )
        instance.updated_at = validated_data.get("updated_at", instance.updated_at)

        if "tags" in validated_data:
            instance.tags.set(instance["tags"])

        instance.save()
        return instance
