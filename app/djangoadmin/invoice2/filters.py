from django.contrib import admin
from django.utils.translation import ugettext as _


class CustomerTypeFilter(admin.SimpleListFilter):
    """ Admin filter which allows us to only show in company / physical personal customer. """
    title = _("Type de client")
    parameter_name = 'customer_type'

    COMPANY = 'company'
    PERSONAL = 'personal'

    def lookups(self, request, model_admin):
        return [
            (self.COMPANY, _("Société")),
            (self.PERSONAL, _("Particulier")),
        ]

    def queryset(self, request, queryset):
        if self.value() == self.COMPANY:
            return queryset.filter(company_vat__isnull=False)
        if self.value() == self.PERSONAL:
            return queryset.filter(company_vat__isnull=True)
        return queryset