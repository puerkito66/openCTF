from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.translation import ugettext as _


class IsVerifiedMixin(UserPassesTestMixin):
    """Profile verification mixin

    Checks if a user has verified the registered email, so some actions can be enabled.
    """

    permission_denied_message = _(
        "Please verify your email first before you can create a Team."
    )

    def test_func(self):
        return self.request.user.profile.is_verified


class IsNotInTeamMixin(UserPassesTestMixin):
    """Team Verification Mixin

    Checks if a user has not alreadey in a team.
    """

    permission_denied_message = _("You are already in a Team.")

    def test_func(self):
        return not self.request.user.team.all().exists()
