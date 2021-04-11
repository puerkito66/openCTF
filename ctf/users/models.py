"""
The OpenCTF Accounting Models Runtime Module.

This module defines two main models:
* The Profile Model.
* The Team Model.

There's also a class definition for the Django User that avoids the problem of
case-sensitive usernames.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from .managers import CaseInsensitiveUserManager


User = get_user_model()


class CaseInsensitiveUser(AbstractUser):
    """User class that avoids the problem of case-sensitive usernames.

    Due to Django usernames being saved and processed case-sensitive, this can be a
    problem. For example, if a user or a team is named "Foo", by common sense "Foo",
    "foo", "foO", "FOO", etc. should mean the same user/team. But Django lacks this
    common sense, so this class, rather than fix, pretends to avoid this problem.

    If this is not a problem for you, you can leave this as-is, else change
    `AUTH_USER_MODEL` in your settings file to this class.

        see: https://code.djangoproject.com/ticket/32543
    """

    objects = CaseInsensitiveUserManager()


class Profile(models.Model):
    """
    Profile Model.
    A profile wrapper for the Django User model that manages the details of the
    participants of the CTF and some other details like verification, etc.
    """

    class Sex(models.IntegerChoices):
        FEMALE = 0, _("Female")
        MALE = 1, _("Male")

        __empty__ = _("Non of the above")

    # The user this profile belongs to.
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)

    # Information stuff
    country = models.CharField(
        verbose_name=_("country"), max_length=50, blank=True, null=False
    )
    institution = models.CharField(
        verbose_name=_("institution"), max_length=100, blank=True, null=False
    )
    sex = models.IntegerField(
        verbose_name=_("sex"), choices=Sex.choices, null=True, null=True
    )
    age = models.SmallIntegerField(_("age"), blank=True)

    # Account management
    is_banned = models.BooleanField(
        verbose_name=_("user ban status"),
        help_text=_("Is the user banned?"),
        null=False,
        default=False,
    )

    def __str__(self):
        return _("Profile[") + self.user.username + "]"
