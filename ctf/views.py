from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin


class UserCreateView(SuccessMessageMixin, CreateView):
    pass
