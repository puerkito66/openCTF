from django.db import models

from ctf.users.models import User


class Team(models.Model):
    """
    Team Model.

    This model manages the Team Profile for the participants.
    """

    name = models.CharField(_("team name"), max_length=50, blank=False)
    password = models.CharField(_("password"), max_length=100, blank=False)

    captain = models.OneToOneField(
        User,
        verbose_name=_("team captain"),
        help_text=_("The Team Captain. By default is the team creator."),
        null=False,
    )
    members = models.ForeignKey(
        User,
        related_name="team",
        verbose_name="members",
        on_delete=models.DO_NOTHING,
        help_text=_("The members of the Team."),
    )

    is_banned = models.BooleanField(
        verbose_name=_("team ban status"),
        help_text=_("Is the team banned?"),
        default=False,
    )
