from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from core_apps.articles.models import Article
from core_apps.common.models import BaseModel

User = get_user_model()

# Create your models here.


class Rating(BaseModel):
    RATING_CHOICES = [
        (1, _("Poor")),
        (2, _("Fair")),
        (3, _("Good")),
        (4, _("Very Good")),
        (5, _("Excellent")),
    ]
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="ratings"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings")
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    review = models.TextField(blank=True)

    class Meta:
        verbose_name = _("Rating")
        verbose_name_plural = _("Ratings")
        unique_together = ("article", "user")

    def __str__(self):
        return (
            f"{self.user.first_name.title()} {self.user.last_name.title()} "
            f"rated {self.article.title.title()} as {self.get_rating_display()}."
        )
