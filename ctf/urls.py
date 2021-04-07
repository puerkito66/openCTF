from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView

app_name = "ctf"

urlpatterns = [
    # Authentication
    path("signin/", LoginView.as_view(), name="signin"),
    path("signout/", LogoutView.as_view(), name="signout"),
]
