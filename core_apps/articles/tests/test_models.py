import math

import pytest

from core_apps.articles.models import ArticleView
from core_apps.articles.read_time_engine import (
    SECONDS_PER_IMAGE,
    SECONDS_PER_TAG,
    WORDS_PER_MINUTE,
    ArticleReadTimeEngine,
)
from core_apps.articles.tests.factories import ArticleViewFactory, ClapFactory
from core_apps.ratings.tests.factories import RatingFactory


@pytest.mark.django_db
def test_create_article(user_article):
    assert user_article.author
    assert user_article.title
    assert user_article.slug
    assert user_article.body
    assert user_article.description
    assert user_article.banner_image.url


@pytest.mark.django_db
def test_str_article(user_article):
    assert str(user_article) == f"{user_article.title.title()} Article"


@pytest.mark.django_db
def test_estimated_reading_time_article(user_article):
    word_counts_article_title = ArticleReadTimeEngine.word_count(user_article.title)
    word_counts_article_content = ArticleReadTimeEngine.word_count(user_article.body)
    word_counts_article_description = ArticleReadTimeEngine.word_count(
        user_article.description
    )

    words_counts = (
        word_counts_article_title
        + word_counts_article_content
        + word_counts_article_description
    )
    reading_time = words_counts / WORDS_PER_MINUTE
    if user_article.banner_image:
        reading_time += SECONDS_PER_IMAGE / 60
    article_tags = user_article.tags.count()
    reading_time += (article_tags * SECONDS_PER_TAG) / 60

    assert math.ceil(reading_time) == user_article.estimated_reading_time


@pytest.mark.django_db
def test_article_views_count(user_article):
    assert user_article.article_views_count() == 0

    for _ in range(10):
        article_view = ArticleViewFactory(article=user_article)

    assert user_article.article_views_count() == user_article.article_views.count()


@pytest.mark.django_db
def test_article_average_rating(user_article):
    assert user_article.average_rating() is None

    # rate
    for _ in range(10):
        RatingFactory(article=user_article)
    assert user_article.ratings.count() == 10

    assert user_article.average_rating() > 0

    ratings = user_article.ratings.all()
    total_ratings = round(
        sum([rating.rating for rating in ratings]) / ratings.count(), 2
    )
    assert user_article.average_rating() == total_ratings


@pytest.mark.django_db
def test_create_clap():
    clap = ClapFactory()
    assert clap
    assert clap.user is not None
    assert clap.article is not None


@pytest.mark.django_db
def test_str_clap():
    clap = ClapFactory()
    assert (
        str(clap)
        == f"{clap.user.first_name.title()} {clap.user.last_name.title()} clapped {clap.article.title}"
    )


@pytest.mark.django_db
def test_create_article_view():
    article_view = ArticleViewFactory()
    assert article_view is not None
    assert article_view.article is not None
    assert article_view.user is not None
    assert article_view.viewer_ip is not None


@pytest.mark.django_db
def test_create_article_view_without_ip(user_article, normal_user):
    article_view = ArticleView.objects.create(user=normal_user, article=user_article)
    assert article_view is not None
    assert article_view.user is not None
    assert article_view.user == normal_user
    assert article_view.article is not None
    assert article_view.article == user_article
    assert article_view.viewer_ip is None


@pytest.mark.django_db
def test_create_article_view_without_user(user_article, normal_user):
    article_view = ArticleView.objects.create(article=user_article)
    assert article_view is not None
    assert article_view.article is not None
    assert article_view.article == user_article
    assert article_view.user is None
    assert article_view.viewer_ip is None


@pytest.mark.django_db
def test_str_article_view():
    article_view = ArticleViewFactory()

    assert article_view is not None
    assert (
        str(article_view)
        == f"{article_view.article.title.title()} viewed by {article_view.user.first_name.title()} {article_view.user.last_name.title()}"
    )

    article_view.user = None
    article_view.save()

    assert article_view is not None
    assert (
        str(article_view)
        == f"{article_view.article.title.title()} viewed by anonymous user"
    )


@pytest.mark.django_db
def test_article_view_record(user_article, normal_user):
    article_view = ArticleView.record(
        article=user_article, user=normal_user, viewer_ip=None
    )
    assert article_view is not None
    assert article_view.article is not None
    assert article_view.article == user_article
    assert article_view.user is not None
    assert article_view.user == normal_user
    assert article_view.viewer_ip is None
