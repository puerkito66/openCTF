from django.shortcuts import render
from django.shortcuts import render
from django.views import View
from django.views.generic import (
    CreateView,
    DetailView,
    FormView,
    ListView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext as _

from ctf.users.mixins import IsVerifiedMixin

from .mixins import IsNotInTeamMixin


class TeamDetailView(DetailView):
    pass


class TeamListView(ListView):
    pass


class TeamCreateView(LoginRequiredMixin, IsVerifiedMixin, IsNotInTeamMixin, CreateView):
    pass


class TeamJoinView(LoginRequiredMixin, IsVerifiedMixin, IsNotInTeamMixin, FormView):
    pass
