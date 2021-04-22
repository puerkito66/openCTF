from django.contrib.auth.models import UserManager


class CaseInsensitiveUserManager(UserManager):
    """Case-Insensitive Manager for User.

    By default, Django checks the username field (whatever it is defined)
    case-sensitive. This is has no sense, so this aproach avoids this problem, even if
    the username field is changed to be the email or something like that.

        see: https://gist.github.com/tuatara/2c388845c28fe1985908
        see: https://simpleisbetterthancomplex.com/tutorial/2017/02/06/how-to-implement-case-insensitive-username.html
    """

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD + "__iexact": username})
