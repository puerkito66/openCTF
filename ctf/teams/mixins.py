from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.translation import ugettext as _


class IsNotInTeamMixin(UserPassesTestMixin):
    """Team Verification Mixin

    Checks if a user has not alreadey in a team.
    """

    permission_denied_message = _("You are already in a Team.")

    def test_func(self):
        return not self.request.user.team.all().exists()
