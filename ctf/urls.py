from django.urls import path
from django.contrib.auth import views

app_name = "ctf"

urlpatterns = [
    # Authentication
    path("signin/", views.LoginView.as_view(), name="signin"),
    path("signout/", views.LogoutView.as_view(), name="signout"),
    # Password reset
    path("password-reset/", views.PasswordResetView.as_view(), name="reset_passowrd"),
]
