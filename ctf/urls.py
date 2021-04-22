from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from .views import IndexView
from .views import (
    TeamCreateView,
    TeamDetailView,
    TeamJoinView,
)

app_name = "ctf"

urlpatterns = [
    # Main Views
    path("", Index.as_view(), name="index"),
    path("/", Index.as_view(), name="index"),
    # Authentication
    path("signin/", auth_views.LoginView.as_view(), name="signin"),
    path("signout/", auth_views.LogoutView.as_view(), name="signout"),
    # Password reset
    path(
        "password-reset/", auth_views.PasswordResetView.as_view(), name="reset_passowrd"
    ),
]


user_urlpatterns = [
    # User details
    path("details/<username:str>", UserDetailView.as_view(), name="user_details"),
    path("list/", UserListView.as_list(), name="list"),
    # Verification
    re_path(
        r"verify/(?P<uidb64>[0-9A-Za-z_\-]+)/"
        r"(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})",
        VerifyAccountView.as_view(),
        name="verify_account",
    ),
    # Password change
    path("change-password/", auth_views.PasswordChangeView.as_view()),
]


team_urlpatterns = [
    # Team details
    path("team/", TeamDetailView.as_view(), name="team_details"),
    # Team creation and joining
    path("newteam/", TeamCreateView.as_view(), name="signin"),
    path("jointeam/", JoinTeamView.as_view(), name="signin"),
]
