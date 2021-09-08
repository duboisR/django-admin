from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Invoice2Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'invoice2'
    # STEP 18
    verbose_name = _("Module de facturation")
