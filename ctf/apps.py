from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig


class CtfAdminConfig(AdminConfig):
    default_site = "openCTF.admin.OpenCtfAdminSite"


class CtfConfig(AppConfig):
    name = "ctf"
    verbose_name = "CTF"

    def ready(self):
        import ctf.signals  # noqa
