from django import forms
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from .models import Submition


User = get_user_model()


class SubmitionForm(forms.ModelForm):
    class Meta:
        model = Submition
        fields = ("flag",)


class TeamJoinForm(forms.Form):
    teamcode = forms.CharField(
        max_length=50,
        help_text=_("Teamname you want to join."),
        validators=[UnicodeUsernameValidator()],
        required=True,
    )
    password = forms.CharField(
        max_length=128,
        help_text=_("The Team password to join."),
        widget=forms.PasswordInput(),
    )
