from django.forms import ModelForm

from .models import Submition


class SubmitionForm(forms.ModelForm):
    class Meta:
        model = Submition
        fields = ("flag",)
