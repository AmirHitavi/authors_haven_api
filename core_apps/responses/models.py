from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from core_apps.articles.models import Article
from core_apps.common.models import BaseModel

User = get_user_model()


# Create your models here.


class Response(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="responses")
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="responses"
    )
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
    content = models.TextField(verbose_name=_("response content"))

    class Meta:
        verbose_name = _("Response")
        verbose_name_plural = _("Responses")
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.user.first_name.title()} {self.user.last_name.title()} "
        f"commented on {self.article.title}"
