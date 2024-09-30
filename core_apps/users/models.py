from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core_apps.common.models import BaseModel

# Create your models here.


class CustomUserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
            return True
        except ValidationError:
            raise ValidationError(_("You must provide a valid email address."))

    def create_user(self, *, first_name, last_name, email, password, **extra_fields):
        """
        Creates and Saves a new user with the given first name, last name
        email and password.
        """
        if not first_name:
            raise ValueError(_("Users must have a first name."))

        if not last_name:
            raise ValueError(_("Users must have a last name."))

        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("Users must have an email."))

        user = self.model(
            first_name=first_name, last_name=last_name, email=email, **extra_fields
        )
        user.set_password(password)

        extra_fields.setdefault("is_active", False)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        user.save(using=self._db)
        return user

    def create_superuser(
        self, *, first_name, last_name, email, password, **extra_fields
    ):
        """
        Creates and Saves a new superuser with the given first name, last name
        email and password.
        """
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_active") is not True:
            raise ValueError(
                _("Superusers must have 'is_active' attribute set to True.")
            )

        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                _("Superusers must have 'is_staff' attribute set to True.")
            )

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                _("Superusers must have 'is_superuser' attribute set to True.")
            )

        if not password:
            raise ValueError(_("Superusers must have password."))

        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            **extra_fields,
        )

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    first_name = models.CharField(verbose_name=_("first name"), max_length=255)
    last_name = models.CharField(verbose_name=_("last name"), max_length=255)
    email = models.EmailField(verbose_name=_("email"), max_length=255, unique=True)

    is_active = models.BooleanField(verbose_name=_("is active"), default=False)
    is_staff = models.BooleanField(verbose_name=_("is staff"), default=False)
    is_superuser = models.BooleanField(verbose_name=_("is superuser"), default=False)

    date_joined = models.DateTimeField(
        verbose_name=_("date joined"), default=timezone.now
    )

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    @property
    def get_full_name(self):
        return f"{self.first_name.title()} {self.last_name.title()}"

    @property
    def get_short_name(self):
        return f"{self.first_name.title()}"
