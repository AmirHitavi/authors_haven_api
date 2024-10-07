from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from core_apps.articles.models import Article

User = get_user_model()

# Create your models here.


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="bookmarks"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Bookmark")
        verbose_name_plural = _("Bookmarks")
        unique_together = ("user", "article")
        ordering = ("-created_at",)

    def __str__(self):
        return (
            f"{self.user.first_name.title()} {self.user.last_name.title()} "
            f"bookmarked {self.article.title.title()}."
        )
