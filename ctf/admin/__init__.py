from django.contrib.admin import AdminSite, ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model as usermodel

from openCTF.admin import admin_site

from .forms import (
    CaseInsensitiveUserCreationForm,
    CaseInsensitiveUserChangeForm,
    TeamChangeForm,
    TeamCreationForm,
)

from ..models import (
    Player,
    Team,
    Category,
    Challenge,
    Submition,
)


class CaseInsensitiveUserAdmin(UserAdmin):
    model = usermodel()
    add_form = CaseInsensitiveUserCreationForm
    form = CaseInsensitiveUserChangeForm


class TeamAdmin(ModelAdmin):
    model = Team
    add_form = TeamCreationForm
    form = TeamChangeForm

    def get_urls(self):
        return super().get_urls()


class SubmitionAdmin(ModelAdmin):
    model = Submition
    readonly_fields = "__all__"


admin_site.register(usermodel(), CaseInsensitiveUserAdmin)
admin_site.register(Player, ModelAdmin)
admin_site.register(Team, TeamAdmin)
admin_site.register(Category, ModelAdmin)
admin_site.register(Challenge, ModelAdmin)
admin_site.register(Submition, ModelAdmin)
