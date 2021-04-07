from django.urls import path

from .views import (
    TeamCreateView,
    TeamDetailView,
    TeamJoinView,
)

app_name = "ctf.users"

urlpatterns = [
    # Team details
    path("team/", TeamDetailView.as_view(), name="team_details"),
    # Team creation and joining
    path("newteam/", TeamCreateView.as_view(), name="signin"),
    path("jointeam/", JoinTeamView.as_view(), name="signin"),
]
