"""
The OpenCTF Accounting Models Runtime Module.

This module defines two main models:
* The Player Models (ProfilePlayer and Team Models)
* The Challenges Models (Challenge and Submission Models)

There's also a class definition for the Django User that fixes the problem of
case-sensitive usernames.
"""

import hashlib

from functools import reduce

from django.conf import settings

from django.core.validators import ValidationError
from django.contrib.auth.models import AbstractUser

from django.db import models
from django.utils import timezone

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from .managers import CaseInsensitiveUserManager
from .validators import TeamnameValidator


class User(AbstractUser):
    """User class that avoids the problem of case-sensitive usernames.

    Due to Django usernames being saved and processed case-sensitive, this can be a
    problem. For example, if a user or a team is named "Foo", by common sense "Foo",
    "foo", "foO", "FOO", etc. should mean the same user/team. But Django lacks this
    common sense, so this class, rather than fix, pretends to avoid this problem.
        see: https://code.djangoproject.com/ticket/32543
    """

    objects = CaseInsensitiveUserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")


class Team(models.Model):
    """
    Team Model.

    This model manages the Team Profile for the participants.
    """

    teamname = models.CharField(
        verbose_name=_("teamname"),
        help_text=_("The teamname, same as a username. Required."),
        unique=True,
        max_length=50,
        blank=False,
        validators=[TeamnameValidator()],
    )
    password = models.CharField(_("password"), max_length=128, blank=False)

    institution = models.CharField(_("institution"), max_length=100, blank=True)
    country = models.CharField(_("country"), max_length=100, blank=True)

    is_banned = models.BooleanField(
        verbose_name=_("team ban status"),
        help_text=_("Is the team banned?"),
        null=False,
        default=False,
    )

    @property
    def score(self):
        """Calculates the team general score."""
        return reduce(
            lambda x, y: x + y,
            self.members.aggregate(
                score=Sum(
                    "submition__challenge__score", filter=Q(submition__correct=True)
                )
            ).values_list("score", flat=True),
        )

    def __str__(self):
        return _("Team[") + self.teamname + "]"


class Player(models.Model):
    """
    Player Model.
    A profile wrapper for the Django User model that manages the details of the
    participants of the CTF and some other details like verification, etc.
    """

    class Sex(models.IntegerChoices):
        FEMALE = 0, _("Female")
        MALE = 1, _("Male")

        __empty__ = _("Non of the above")

    # The user this profile belongs to.
    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL, related_name="profile", on_delete=models.CASCADE
    )
    team = models.ForeignKey(
        to=Team,
        on_delete=models.SET_NULL,
        related_name="members",
        verbose_name="team",
        help_text="The Team of this participant.",
        default=None,
        blank=True,
        null=True,
    )

    # Information stuff
    country = models.CharField(
        verbose_name=_("country"), max_length=50, blank=True, null=False
    )
    institution = models.CharField(
        verbose_name=_("institution"), max_length=100, blank=True, null=False
    )
    sex = models.IntegerField(verbose_name=_("sex"), choices=Sex.choices, null=True)
    age = models.SmallIntegerField(_("age"), blank=True)

    # Account management
    is_banned = models.BooleanField(
        verbose_name=_("user ban status"),
        help_text=_("Is the user banned?"),
        null=False,
        default=False,
    )
    is_verified = models.BooleanField(
        verbose_name=_("user verification status"),
        help_text=_("Is the user verified?"),
        null=False,
        default=False,
    )

    def __str__(self):
        return _("Profile[") + self.user.username + "]"


class Category(models.Model):
    name = models.CharField(
        verbose_name=_("category name"),
        help_text=_("The name which names this category."),
        blank=False,
        max_length=50,
    )
    description = models.TextField(
        verbose_name=_("category description"),
        help_text=_("A brief description about the challenges in this category."),
        blank=True,
    )

    def __str__(self):
        return f"Category[{self.name}]"


class Challenge(models.Model):
    """A Challenge to solve."""

    class Difficulty(models.IntegerChoices):
        EASY = 0, _("Easy")
        MEDIUM = 1, _("Medium")
        HARD = 2, _("Hard")
        INSANE = 3, _("Insane")

    category = models.ForeignKey(
        Category,
        verbose_name=_("challenge category"),
        help_text=_("The category of this challenge"),
        on_delete=models.CASCADE,
        null=False,
    )

    diffculty = models.SmallIntegerField(
        verbose_name=_("difficulty"),
        help_text=_("How complicated is this challenge to solve."),
        choices=Difficulty.choices,
        null=False,
        blank=False,
    )

    name = models.CharField(
        verbose_name=_("challenge name"),
        help_text=_("The name of this challenge."),
        blank=False,
        max_length=100,
    )
    description = models.TextField(
        verbose_name=_("challenge description"),
        help_text=_("A description about this challenge. You can insert HTML content"),
        blank=True,
    )
    points = models.PositiveIntegerField(
        verbose_name=_("value of the challenge"),
        help_text=("The number of points this challenge gives to the team."),
    )
    flag = models.CharField(
        verbose_name=_("challenge's flag."),
        help_text=_("The flag of the challenge."),
        max_length=128,
        blank=False,
    )

    def __str__(self):
        return f"{self.name} : {self.category}"


class Submition(models.Model):
    challenge = models.ForeignKey(
        Challenge, related_name="submitions", on_delete=models.CASCADE
    )
    player = models.ForeignKey(
        Player, related_name="submitions", on_delete=models.CASCADE
    )
    team = models.ForeignKey(Team, related_name="submitions", on_delete=models.CASCADE)

    correct = models.BooleanField(
        verbose_name=_("submition_correct"),
        help_text=_("Whether this sumbition is correct or not."),
        null=False,
        default=False,
    )

    # Challenge stuff
    timestamp = models.DateTimeField(
        verbose_name=_("submition time"),
        help_text=_("The timestamp when this submition was made."),
        auto_now=True,
        null=False,
    )
    flag = models.CharField(
        _("flag used"),
        help_text=_(
            "Flag used in this submition. " "Encoded if correct, plaintext otherwise."
        ),
        blank=True,
        max_length=128,
    )
