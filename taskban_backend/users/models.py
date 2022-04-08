import os

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Avatar(models.Model):
    photo = models.ImageField(upload_to="avatars")

    def __str__(self):
        return os.path.basename(self.photo.name)


class User(AbstractUser):
    """
    Default custom user model for Taskban Backend.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    avatar = models.ForeignKey(
        "Avatar", null=True, blank=True, on_delete=models.PROTECT
    )
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
