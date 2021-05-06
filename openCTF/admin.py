from django.contrib.admin import AdminSite

from django.utils.translation import ugettext_lazy as _


class OpenCtfAdminSite(AdminSite):
    site_header = _("openCTF Administration")
    site_title = _("The openCTF Administration Panel")


admin_site = OpenCtfAdminSite(name="openCtfAdmin")