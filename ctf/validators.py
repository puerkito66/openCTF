from django.contrib.auth.validators import UnicodeUsernameValidator

from django.utils.translation import ugettext_lazy as _


class TeamnameValidator(UnicodeUsernameValidator):
    message = _(
        "Enter a valid teamname. This value may contain only letters, "
        "numbers, and @/./+/-/_ characters."
    )
