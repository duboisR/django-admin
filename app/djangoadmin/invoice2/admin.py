from django import forms
from django.contrib import admin
from django.shortcuts import reverse
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe

import invoice2.filters
import invoice2.models


# Customer
class CustomerAddressInline(admin.StackedInline):
    model = invoice2.models.CustomerAddress
    extra = 0
    min_num = 1
    classes = ['collapse']

    fields = (
        ('address_street', 'address_street_number', 'address_bp', ),
        ('address_zipcode', 'address_city', ),
    )


@admin.register(invoice2.models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'contact_email', 'contact_phone', 'get_invoice_link', )
    search_fields = ('company_name', 'company_vat', 'contact_first_name', 'contact_last_name', 'contact_email', 'contact_phone', )
    list_filter = (invoice2.filters.CustomerTypeFilter, )
    
    fieldsets = (
        (_("Société"), {'fields': (
            ('company_name', 'company_vat', ),
        )}),
        (_("Contact"), {'fields': (
            ('contact_first_name', 'contact_last_name', ),
            'contact_email', 'contact_phone',
        )}),
    )
    inlines = [CustomerAddressInline, ]

    def get_invoice_link(self, obj):
        url = reverse('admin:invoice2_invoice_changelist')
        return mark_safe("<a href='%s?customer__id__exact=%s'>Factures</a>" % (url, str(obj.pk)))
    get_invoice_link.short_description = _("Factures")


# Product
@admin.register(invoice2.models.Product)
class ProductAdmin(admin.ModelAdmin):
    model = invoice2.models.Product

    list_display = ('__str__', 'vat', 'price', )
    search_fields = ('description', )
    readonly_fields = ('vat', )


# Invoice
class InvoiceAdminForm(forms.ModelForm):
    ref_number_warning = forms.BooleanField(
        label=_("Vous êtes sur le point de modifier la numérotation de ce devis. Afin d’éviter toutes erreurs, veuillez valider votre choix"),
        initial=True, required=True)

    class Meta:
        model = invoice2.models.Invoice
        fields = '__all__'


class InvoiceItemInline(admin.TabularInline):
    model = invoice2.models.InvoiceItem
    verbose_name = _("Produit")
    verbose_name_plural = _("Produits")
    extra = 0
    autocomplete_fields = ['product', ]
    readonly_fields = ('product_vat', )


@admin.register(invoice2.models.Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    model = invoice2.models.Invoice

    list_display = ('invoice_number', 'invoice_date', 'get_customer', 'get_address', 'get_total', 'get_deadline_date', )
    search_fields = ('invoice_number', )
    date_hierarchy = 'invoice_date'
    list_filter = ('customer', )

    form = InvoiceAdminForm
    autocomplete_fields = ['customer', ]
    fieldsets = (
        (_("Client"), {'fields': (
            ('customer', ),
        )}),
        (_("Société"), {'fields': (
            ('company_name', 'company_vat', ),
        )}),
        (_("Contact"), {'fields': (
            ('contact_first_name', 'contact_last_name', ),
            'contact_email', 'contact_phone', 
        )}),
        (_("Adresse"), {'fields': (
            ('address_street', 'address_street_number', 'address_bp', ),
            ('address_zipcode', 'address_city', ),
        )}),
        (_("Facturation"), {'fields': (
            ('invoice_number', ),
            'ref_number_warning',  # cf. InvoiceAdminForm
            'invoice_date', 'terms_payment', 'discount', ),
        }),
    )
    inlines = [InvoiceItemInline, ]