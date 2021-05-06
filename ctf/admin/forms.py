from django import forms
from django.contrib.auth import forms as auth_forms

from django.core.exceptions import ValidationError
from django.contrib.auth.admin import (
    UserAdmin,
    UserCreationForm,
    UserChangeForm,
    AdminPasswordChangeForm,
)
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from django.contrib.auth import get_user_model, password_validation
from django.utils.translation import ugettext_lazy as _

from ..models import Team

User = get_user_model()


class CaseInsensitiveUsernameCleanMixin:
    def clean_username(self):
        data = self.cleaned_data["username"]

        if data and User.objects.filter(username__iexact=data).exists():
            raise ValidationError(_("A user with that username already exists."))

        return data


class CaseInsensitiveUserCreationForm(
    CaseInsensitiveUsernameCleanMixin, UserCreationForm
):
    pass


class CaseInsensitiveUserChangeForm(CaseInsensitiveUsernameCleanMixin, UserChangeForm):
    pass


class TeamnameField(auth_forms.UsernameField):
    pass


class TeamCreationForm(forms.ModelForm):
    """
    A form that creates a team.
    """

    error_messages = {
        "password_mismatch": _("The two password fields didn't match."),
    }
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = Team
        fields = ("teamname",)
        field_classes = {"teamname": TeamnameField}

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get("password2")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error("password2", error)


class TeamChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see this "
            "teams's password, but you can change the password using "
            '<a href="{}">this form</a>.'
        ),
    )

    class Meta:
        model = Team
        fields = "__all__"
        field_classes = {"username": TeamnameField}
