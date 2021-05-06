from django.views.generic import CreateView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import DetailView, ListView, FormView, TemplateView, View
from django.views.generic.edit import CreateView

from django.shortcuts import get_object_or_404
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .tokens import account_verifier

from .models import User, Player, Team, Challenge, Category, Submition
from .mixins import IsNotInTeamMixin, IsInTeamMixin, IsVerifiedMixin


"""############ GENERAL VIEWS ############"""


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = UserCreationForm
    template_name = "user_new.html"


class IndexView(TemplateView):
    template_name = "index.html"


"""############ PLAYER VIEWS ############"""


class PlayerDetailView(DetailView):
    """Get access to the details of a Player."""

    model = Player
    template_name = "player_profile.html"

    def get_object(self):
        return get_object_or_404(Player, user__username=self.kwargs["username"])


class PlayerProfileView(TemplateView):
    """Get access to the details of the CURRENT player."""

    template_name = "player_detail.html"


class PlayerListView(ListView):
    model = Player
    template_name = "player_list.html"


class PlayerVerifyAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_verifier.check_token(user, token):
            user.profile.email_confirmed = True
            user.save()

            messages.success(
                request=request,
                message=_("Your account has been verified successfuly!"),
            )
            return render(
                request=request,
                template_name="users/activation_success.html",
                status=200,
            )
        else:
            # invalid link
            return render(
                request=request, template_name="users/invalid_token.html", status=409
            )


############ TEAM VIEWS ############


class TeamDetailView(DetailView):
    model = Team
    tempate_name = "team_details.html"


class TeamListView(ListView):
    model = Team
    template_name = "team_list.html"


class TeamCreateView(LoginRequiredMixin, IsVerifiedMixin, IsNotInTeamMixin, CreateView):
    model = Team
    template_name = "team_new.html"


class TeamJoinView(LoginRequiredMixin, IsVerifiedMixin, IsNotInTeamMixin, FormView):
    pass


############ CHALLENGE VIEWS ############


class ChallengeListView(LoginRequiredMixin, IsVerifiedMixin, IsInTeamMixin):
    # Althoug we mention here `Challenge`, we're meaning actually the `Category`.
    model = Category
    template_name = "challenge_list.html"


class ChallengeSubmitionView(LoginRequiredMixin, IsVerifiedMixin, IsInTeamMixin, View):
    pass
