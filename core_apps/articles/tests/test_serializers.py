from datetime import datetime

import pytest
from faker import Factory as FactoryFaker
from rest_framework.exceptions import ValidationError
from taggit.models import Tag

from core_apps.articles.models import Article, ArticleView, Clap
from core_apps.articles.serializers import (
    ArticleSerializer,
    ClapSerializer,
    TagListField,
)
from core_apps.articles.tests.factories import ClapFactory
from core_apps.bookmarks.models import Bookmark
from core_apps.bookmarks.serializers import BookmarkSerializer
from core_apps.responses.models import Response
from core_apps.responses.serializers import ResponseSerializer

faker = FactoryFaker.create()


@pytest.mark.django_db
def test_to_representation_tag_field(normal_user):
    article = Article.objects.create(
        author=normal_user,
        title=faker.sentence(),
        body=faker.paragraph(),
        description=faker.sentence(),
    )

    assert article is not None
    assert article.author is not None
    assert article.body is not None
    assert article.description is not None

    fake_tags = faker.words(nb=5)

    article.tags.add(*fake_tags)
    tag_list_field = TagListField()
    representation = tag_list_field.to_representation(article.tags.all())

    assert article.tags.all() is not None
    assert article.tags.count() == len(representation)
    assert representation == fake_tags


@pytest.mark.django_db
def test_to_internal_value_tag_field():
    tag_list = TagListField()

    fake_tags = faker.words(nb=5)

    internal = tag_list.to_internal_value(fake_tags)

    assert all([isinstance(tag, Tag) for tag in internal])

    assert [tag.name for tag in internal] == fake_tags

    with pytest.raises(ValidationError):
        internal = tag_list.to_internal_value(faker.word())


@pytest.mark.django_db
def test_article_serializer(user_article):
    serializer = ArticleSerializer(user_article)

    assert "id" in serializer.data
    assert "title" in serializer.data
    assert "slug" in serializer.data
    assert "estimated_reading_time" in serializer.data
    assert "average_rating" in serializer.data
    assert "bookmarks" in serializer.data
    assert "bookmarks_count" in serializer.data
    assert "claps_count" in serializer.data
    assert "responses" in serializer.data
    assert "responses_count" in serializer.data
    assert "body" in serializer.data
    assert "description" in serializer.data
    assert "author_info" in serializer.data
    assert "banner_image" in serializer.data
    assert "tags" in serializer.data
    assert "views_count" in serializer.data
    assert "created_at" in serializer.data
    assert "updated_at" in serializer.data


@pytest.mark.django_db
def test_article_get_banner_image(user_article):
    serializer = ArticleSerializer(user_article)
    assert user_article.banner_image.url == serializer.data["banner_image"]


@pytest.mark.django_db
def test_article_get_views(user_article):
    serializer = ArticleSerializer(user_article)
    assert (
        ArticleView.objects.filter(article=user_article).count()
        == serializer.data["views_count"]
    )


@pytest.mark.django_db
def test_article_get_average_rating(user_article):
    serializer = ArticleSerializer(user_article)
    assert "average_rating" in serializer.data
    assert user_article.average_rating() == serializer.data["average_rating"]


@pytest.mark.django_db
def test_article_get_bookmarks(user_article):
    serializer = ArticleSerializer(user_article)
    bookmarks = Bookmark.objects.filter(article=user_article)

    assert BookmarkSerializer(bookmarks, many=True).data == serializer.data["bookmarks"]


@pytest.mark.django_db
def test_article_get_bookmarks_count(user_article):
    serializer = ArticleSerializer(user_article)
    assert (
        Bookmark.objects.filter(article=user_article).count()
        == serializer.data["bookmarks_count"]
    )


@pytest.mark.django_db
def test_article_get_claps_count(user_article):
    serializer = ArticleSerializer(user_article)
    assert (
        Clap.objects.filter(article=user_article).count()
        == serializer.data["claps_count"]
    )


@pytest.mark.django_db
def test_article_get_responses(user_article):
    serializer = ArticleSerializer(user_article)
    responses = Response.objects.filter(article=user_article)

    assert ResponseSerializer(responses, many=True).data == serializer.data["responses"]


@pytest.mark.django_db
def test_article_get_responses_count(user_article):
    serializer = ArticleSerializer(user_article)
    assert (
        Response.objects.filter(article=user_article).count()
        == serializer.data["responses_count"]
    )


@pytest.mark.django_db
def test_article_get_created_at(user_article):
    serializer = ArticleSerializer(user_article)
    format = "%Y-%m-%d: %H:%M:%S"
    assert datetime.strptime(serializer.data["created_at"], format)


@pytest.mark.django_db
def test_article_get_updated_at(user_article):
    serializer = ArticleSerializer(user_article)
    format = "%Y-%m-%d: %H:%M:%S"
    assert datetime.strptime(serializer.data["updated_at"], format)


@pytest.mark.django_db
def test_article_create(normal_user):
    validated_data = {
        "title": faker.sentence(),
        "body": faker.paragraph(),
        "description": faker.sentence(),
        "tags": faker.words(nb=3),
    }

    serializer = ArticleSerializer(data=validated_data)

    assert serializer.is_valid(raise_exception=True)
    article = serializer.save(author=normal_user)
    assert article is not None
    assert article.author == normal_user
    assert article.title == validated_data["title"]
    assert article.body == validated_data["body"]
    assert article.description == validated_data["description"]
    assert article.tags.count() == len(set(validated_data["tags"]))

    invalidate_data = {
        "title": faker.sentence(),
        "body": faker.paragraph(),
        "description": faker.sentence(),
        "tags": "tag",
    }

    serializer = ArticleSerializer(data=invalidate_data)

    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_article_update(user_article):
    serializer = ArticleSerializer(user_article)

    validated_data = {
        "title": faker.sentence(),
        "body": faker.paragraph(),
        "description": faker.sentence(),
        "tags": faker.words(nb=3),
    }

    serializer = ArticleSerializer(data=validated_data, instance=user_article)

    assert serializer.is_valid(raise_exception=True)
    article = serializer.save()
    assert article is not None
    assert article.author == user_article.author
    assert article.title == validated_data["title"]
    assert article.body == validated_data["body"]
    assert article.description == validated_data["description"]
    assert article.tags.count() == len(set(validated_data["tags"]))


@pytest.mark.django_db
def test_clap_serializer():
    clap = ClapFactory()
    serializer = ClapSerializer(clap)
    assert "id" in serializer.data
    assert "user_fullname" in serializer.data
    assert "article_title" in serializer.data


@pytest.mark.django_db
def test_clap_get_user_fullname():
    clap = ClapFactory()
    serializer = ClapSerializer(clap)
    assert (
        serializer.data["user_fullname"]
        == f"{clap.user.first_name.title()} {clap.user.last_name.title()}"
    )
