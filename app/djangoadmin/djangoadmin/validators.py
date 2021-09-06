from django.core.validators import RegexValidator
from django.utils.translation import ugettext as _


PhoneValidator = RegexValidator(regex=r'^\+\d{9,15}$', message=_("Merci de renseigner le numéro de téléphone avec un indicatif international. Format: +32xxxxxxxxx."))
VatValidator = RegexValidator(regex=r'^[A-Z]{2,4}(?=.{2,12}$)[-_\s0-9]*(?:[a-zA-Z][-_\s0-9]*){0,2}$', message=_("Merci de renseigner un numéro de TVA valide. Format: BExxxxxxxxx"))