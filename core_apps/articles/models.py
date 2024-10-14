from autoslug.fields import AutoSlugField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager

from core_apps.common.models import BaseModel

from .read_time_engine import ArticleReadTimeEngine

User = get_user_model()

# Create your models here.


class Clap(BaseModel):
    article = models.ForeignKey(
        "Article", on_delete=models.CASCADE, related_name="claps"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="clap")

    class Meta:
        verbose_name = _("Clap")
        verbose_name_plural = _("Claps")
        unique_together = ("article", "user")
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"{self.user.first_name.title()} {self.user.last_name.title()} clapped {self.article.title}"


class Article(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")
    title = models.CharField(verbose_name=_("article title"), max_length=255)
    slug = AutoSlugField(populate_from="title", always_update=True, unique=True)
    body = models.TextField(verbose_name=_("article content"))
    description = models.CharField(
        verbose_name=_("article description"), max_length=255
    )
    banner_image = models.ImageField(
        verbose_name=_("article banner image"), default="./default_banner.png"
    )
    tags = TaggableManager()

    clap = models.ManyToManyField(User, through=Clap, related_name="clapped_articles")

    def __str__(self):
        return f"{self.title.title()} Article"

    @property
    def estimated_reading_time(self):
        return ArticleReadTimeEngine.estimate_reading_time(self)

    def article_views_count(self):
        return self.article_views.count()

    def average_rating(self):
        ratings = self.ratings.all()

        if ratings.count() > 0:
            total_ratings = sum([rating.rating for rating in ratings])
            average_rating = total_ratings / ratings.count()
            return round(average_rating, 2)
        average_rating = None

        return average_rating


class ArticleView(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="user_views"
    )
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="article_views"
    )
    viewer_ip = models.GenericIPAddressField(
        verbose_name=_("IP address"), blank=True, null=True
    )

    class Meta:
        verbose_name = _("Article View")
        verbose_name_plural = _("Article Views")
        unique_together = ("user", "article", "viewer_ip")

    def __str__(self):
        if self.user:
            return f"{self.article.title.title()} viewed by {self.user.first_name.title()} {self.user.last_name.title()}"
        else:
            return f"{self.article.title.title()} viewed by anonymous user"

    @classmethod
    def record(cls, article, user, viewer_ip):
        view, _ = cls.objects.get_or_create(
            article=article, user=user, viewer_ip=viewer_ip
        )
        view.save()
        return view
