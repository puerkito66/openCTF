from django.views.generic import CreateView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import UserCreationForm


"""############ GENERAL VIEWS ############"""


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = UserCreationForm
    template_name = "users/new_user.html"


class IndexView(TemplateView):
    template_name = "index.html"


"""############ PLAYER VIEWS ############"""


class PlayerDetailView(DetailView):
    model = Player
    template_name = "profile_check.html"

    def get_object(self):
        return get_object_or_404(UserProfile, user__username=self.kwargs["username"])


class PlayerListView(ListView):
    pass


class VerifyAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
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
    detal


class TeamListView(ListView):
    pass


class TeamCreateView(LoginRequiredMixin, IsVerifiedMixin, IsNotInTeamMixin, CreateView):
    pass


class TeamJoinView(LoginRequiredMixin, IsVerifiedMixin, IsNotInTeamMixin, FormView):
    pass
