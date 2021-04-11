"""General User Informative Views.

This module only displays info about the participants of the CTF.
Since everybody can see all participants in the contest, there's no point asking for
sign up.
"""


from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext as _

from .models import User, Profile, Team


class UserDetailView(DetailView):
    pass


class UserListView(ListView):
    pass
