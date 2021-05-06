from django.urls import path, re_path

from .views import *

app_name = "ctf"

urlpatterns = [
    # Main Views
    path("", IndexView.as_view(), name="index"),
    path("index", IndexView.as_view(), name="index"),
    # User details
    path("details/<str:username>", PlayerDetailView.as_view(), name="user_details"),
    path("list/", PlayerListView.as_view(), name="list"),
    # Verification
    re_path(
        r"verify/(?P<uidb64>[0-9A-Za-z_\-]+)/"
        r"(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})",
        PlayerVerifyAccountView.as_view(),
        name="verify_account",
    ),
    # Team details
    path("team/", TeamDetailView.as_view(), name="team_details"),
    # Team creation and joining
    path("team/new/", TeamCreateView.as_view(), name="team_new"),
    path("team/join/", TeamJoinView.as_view(), name="team_enroll"),
]
