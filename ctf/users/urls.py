from django.urls import path
from django.contrib.auth import views as auth_views

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
    # Password change
    path("change-password/", auth_views.PasswordChangeView.as_view()),
]
