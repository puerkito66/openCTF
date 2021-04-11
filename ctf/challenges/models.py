"""The Challenges Models.

This defines some of the important challenge-related models.
The main models are:
    * The Category Model.
    * The Challenge Model.
    * The Submition Model.
    * The Solution Model.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from ctf.users.models import User
from ctf.teams.models import Team


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
        return self.name


class Challenge(models.Model):
    category = models.ForeignKey(
        Category,
        verbose_name=_("challenge category"),
        help_text=_("The category of this challenge"),
        on_delete=models.CASCADE,
        null=False,
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
    user = models.ForeignKey(User, related_name="submitions", on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name="submitions", on_delete=models.CASCADE)

    # Challenge stuff
    timestamp = models.DateTimeField(
        verbose_name=_("submition time"),
        help_text=_("The timestamp when this submition was made."),
        auto_now=True,
        null=False,
    )
    solved = models.BooleanField(
        verbose_name=_("correct submition"),
        help_text=_("Is this submition a correct challenge solution?"),
        null=False,
        default=False,
    )

    flag = models.CharField(
        _("encoded flag"),
    )
