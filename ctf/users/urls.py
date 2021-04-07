from django.urls import path

from .views import (
    UserCreateView,
    UserDetailView,
    JoinTeamView,
)

app_name = "ctf.users"

urlpatterns = [
    # User details
    path("details/", UserDetailView.as_view(), name="user_details"),
    path("list/", UserListView.as_list(), name="list"),
]
