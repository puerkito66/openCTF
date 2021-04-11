from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class AccountVerificationTokenGenerator(PasswordResetTokenGenerator):
    """The Account Verification Token Generator class.

    Wrapper around the PasswordResetTokenGenerator class but for
    the Account verification process.
    """

    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk)
            + six.text_type(timestamp)
            + six.text_type(user.profile.is_active)
        )


account_verification_token = AccountActivationTokenGenerator()
