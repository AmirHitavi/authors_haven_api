from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from core_apps.common.models import BaseModel

# Create your models here.

User = get_user_model()


class Profile(BaseModel):
    class Gender(models.TextChoices):
        MALE = "M", _("Male")
        FEMALE = "F", _("Female")
        OTHER = "OTHER", _("Other")

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = PhoneNumberField(verbose_name=_("Phone Number"), max_length=30)
    about_me = models.TextField(
        _("About Me"), default="Say something about yourself..."
    )
    gender = models.CharField(_("Gender"), choices=Gender.choices, default=Gender.OTHER)
    country = CountryField(verbose_name=_("Country"), default="US")
    city = models.CharField(_("City"), default="Memphis", max_length=255)
    profile_photo = models.ImageField(
        verbose_name=_("Profile Photo"), default="/default_profile.png"
    )
    twitter_handle = models.CharField(
        verbose_name=_("Twitter Handle"), max_length=20, blank=True, null=True
    )
    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name="following", blank=True
    )

    def __str__(self):
        return f"{self.user.first_name}'s Profile"

    def follow(self, profile):
        self.followers.add(profile)

    def unfollow(self, profile):
        self.followers.remove(profile)

    def check_following(self, profile):
        return self.followers.filter(pk_id=profile.pk_id).exists()
