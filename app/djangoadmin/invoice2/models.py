from decimal import Decimal
from dateutil.relativedelta import relativedelta

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

import djangoadmin.validators


# Customer Models
class Customer(models.Model):
    # Company informations
    company_name = models.CharField(verbose_name=_("Nom"), max_length=255, blank=True, null=True)
    company_vat = models.CharField(verbose_name=_("TVA"), validators=[djangoadmin.validators.VatValidator], max_length=255, blank=True, null=True)

    # Contact informations
    contact_first_name = models.CharField(verbose_name=_("Prénom"), max_length=255, blank=True, null=True)
    contact_last_name = models.CharField(verbose_name=_("Nom"), max_length=255)
    contact_email = models.EmailField(verbose_name=_("Adresse e-mail"), blank=True, null=True)
    contact_phone = models.CharField(verbose_name=_("Téléphone"), validators=[djangoadmin.validators.PhoneValidator], max_length=255)

    # STEP 2
    class Meta:
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")

    # STEP 3
    def __str__(self):
        if self.company_vat:
            return "Société: %s (TVA: %s)" % (self.company_name, self.company_vat)
        return "Particulier: %s" % self.contact_last_name


class CustomerAddress(models.Model):
    # Main information
    customer = models.ForeignKey('Customer', verbose_name=_("Client"),
        on_delete=models.CASCADE, blank=True, null=True)

    # Address informations
    address_street = models.CharField(verbose_name=_("Rue"), max_length=255)
    address_street_number = models.CharField(verbose_name=_("Numéro"), max_length=255, blank=True, null=True)
    address_bp = models.CharField(verbose_name=_("BP"), max_length=255, blank=True, null=True)
    address_zipcode = models.CharField(verbose_name=_("Code postal"), max_length=5)
    address_city = models.CharField(verbose_name=_("Ville"), max_length=255)

    # STEP 2
    class Meta:
        verbose_name = _("Adresse")
        verbose_name_plural = _("Addresses")

    # STEP 3
    def __str__(self):
        return self.get_address()

    # STEP 4
    def get_address(self):
        address = self.address_street
        if self.address_street_number:
            address += " %s" % self.address_street_number
        if self.address_bp:
            address += " / BP %s" % self.address_bp
        address += " - %s %s" % (self.address_zipcode, self.address_city)
        return address
    get_address.short_description = _("Adresse")


# Product Model
class Product(models.Model):
    # Detail informations
    description = models.TextField(verbose_name=_("Description"))
    vat = models.PositiveIntegerField(verbose_name=_("TVA (%)"), default=21)
    price = models.DecimalField(verbose_name=_("Prix (HTVA)"), max_digits=15, decimal_places=2, default=Decimal("0.00"))

    # STEP 2
    class Meta:
        verbose_name = _("Produit")
        verbose_name_plural = _("Produits")

    # STEP 3
    def __str__(self):
        if (len(self.description) > 25):
            return "%s..." % self.description[:25]
        return self.description


# Invoice Models
def generate_invoice_number(country_prefix=1):
    """
    Generate invoice_number for the Invoice. The number should follow each other.
    """
    code_prefix = timezone.now().strftime("%Y%m")
    last_invoices = Invoice.objects.filter(invoice_number__startswith=code_prefix).values_list('invoice_number', flat=True)
    if len(last_invoices) == 0:
        return "{code_prefix}{code}".format(code_prefix=code_prefix, code=format(1, '04d'))
    else:
        next_code = max(map(int, [i[-4:] for i in last_invoices])) + 1
        return "{code_prefix}{code}".format(code_prefix=code_prefix, code=format(next_code, '04d'))


class Invoice(models.Model):
    TERMS_CHOICES = (
        ('15', _("15 jours")),
        ('15_end', _("15 jours fin de mois")),
        ('30', _("30 jours")),
        ('30_end', _("30 jours fin de mois")),
        ('60', _("60 jours")),
        ('60_end', _("60 jours fin de mois")),
        ('90', _("90 jours")),
        ('90_end', _("90 jours fin de mois")),
        ('cash', _("Au comptant")),
    )

    # Invoice informations
    invoice_number = models.CharField(verbose_name=_("Numéro"), max_length=255, unique=True, default=generate_invoice_number)
    invoice_date = models.DateField(verbose_name=_("Date de facturation"), default=timezone.now)
    terms_payment = models.CharField(verbose_name=_("Conditions de payement"), max_length=25, choices=TERMS_CHOICES, default='15')
    discount = models.DecimalField(verbose_name=_("Réduction (en %)"), decimal_places=2, max_digits=5, default=0,
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('100'))])

    # Customer informations
    customer = models.ForeignKey('Customer', verbose_name=_("Client"),
        on_delete=models.SET_NULL, blank=True, null=True)
    
    # Company informations
    company_name = models.CharField(verbose_name=_("Nom"), max_length=255, blank=True, null=True)
    company_vat = models.CharField(verbose_name=_("TVA"), validators=[djangoadmin.validators.VatValidator], max_length=255, blank=True, null=True)

    # Contact informations
    contact_first_name = models.CharField(verbose_name=_("Prénom"), max_length=255, blank=True, null=True)
    contact_last_name = models.CharField(verbose_name=_("Nom"), max_length=255)
    contact_email = models.EmailField(verbose_name=_("Adresse e-mail"), blank=True, null=True)
    contact_phone = models.CharField(verbose_name=_("Téléphone"), validators=[djangoadmin.validators.PhoneValidator], max_length=255)

    # Address informations
    address_street = models.CharField(verbose_name=_("Rue"), max_length=255)
    address_street_number = models.CharField(verbose_name=_("Numéro"), max_length=255, blank=True, null=True)
    address_bp = models.CharField(verbose_name=_("BP"), max_length=255, blank=True, null=True)
    address_zipcode = models.CharField(verbose_name=_("Code postal"), max_length=5)
    address_city = models.CharField(verbose_name=_("Ville"), max_length=255)

    # STEP 2
    class Meta:
        verbose_name = _("Facture")
        verbose_name_plural = _("Factures")

    # STEP 3
    def __str__(self):
        return self.invoice_number

    # STEP 4
    def get_customer(self):
        if self.company_vat:
            return "Société: %s (TVA: %s)" % (self.company_name, self.company_vat)
        return "Particulier: %s" % self.contact_last_name
    get_customer.short_description = _("Client")

    # STEP 4
    def get_address(self):
        address = self.address_street
        if self.address_street_number:
            address += " %s" % self.address_street_number
        if self.address_bp:
            address += " / BP %s" % self.address_bp
        address += " - %s" % self.address_zipcode
        return address
    get_address.short_description = _("Adresse")

    # STEP 4
    def get_deadline_date(self):
        deadline_date = self.invoice_date
        if self.terms_payment:
            if '15' in self.terms_payment:
                deadline_date = deadline_date + relativedelta(days=14)
            if '30' in self.terms_payment:
                deadline_date = deadline_date + relativedelta(months=1)
            elif '60' in self.terms_payment:
                deadline_date = deadline_date + relativedelta(months=2)
            elif '90' in self.terms_payment:
                deadline_date = deadline_date + relativedelta(months=3)
            if 'end' in self.terms_payment:
                deadline_date = timezone(deadline_date.year, deadline_date.month, 1) + relativedelta(months=1, days=-1)
        return deadline_date
    get_deadline_date.short_description = _("Date butoire")

    # STEP 4
    def get_prices(self):
        excl_tax_vat = {}  # calculate excl_tax foreach vat
        for invoiceitem_instance in self.invoiceitem_set.all():
            # Vat
            vat_key = str(invoiceitem_instance.product_vat)
            if vat_key not in excl_tax_vat:
                excl_tax_vat[vat_key] = Decimal('0.00')
            # Price
            excl_tax_vat[vat_key] += invoiceitem_instance.product_price * invoiceitem_instance.product_quantity
        excl_tax = round(sum(excl_tax_vat.values()), 2)

        discount = {}
        if self.discount:
            discount[str(self.discount)] = round(excl_tax * self.discount / 100, 2)
            excl_tax_discount = round(excl_tax - discount[str(self.discount)], 2)
        else:
            excl_tax_discount = excl_tax
        
        vat_val = {}
        for vat, val in excl_tax_vat.items():
            vat_val[vat] = round(val * Decimal(vat) / 100, 2)

        return {
            'excl_tax': excl_tax,
            'discount': discount,
            'excl_tax_discount': excl_tax_discount,
            'vat': vat_val,
            'incl_tax': excl_tax_discount + round(sum(vat_val.values()), 2),
        }

    # STEP 4
    def get_total(self):
        return self.get_prices().get('excl_tax_discount')
    get_total.short_description = _("Montant (HTVA)")


class InvoiceItem(models.Model):
    # Main information
    invoice = models.ForeignKey('Invoice', verbose_name=_("Facture"), on_delete=models.CASCADE)

    # Detail informations
    product = models.ForeignKey('Product', verbose_name=_("Produit"),
        on_delete=models.SET_NULL, blank=True, null=True)
    product_description = models.TextField(verbose_name=_("Description"))
    product_quantity = models.PositiveIntegerField(verbose_name=_("Quantité"), default=1)
    product_vat = models.PositiveIntegerField(verbose_name=_("TVA (%)"), default=21)
    product_price = models.DecimalField(verbose_name=_("Prix (HTVA)"), max_digits=15, decimal_places=2, default=Decimal("0.00"))

    # STEP 2
    class Meta:
        verbose_name = _("Facture (Produit)")
        verbose_name_plural = _("Facture (Produits)")

    # STEP 3
    def __str__(self):
        return "%s - %s" % (self.invoice, self.product_description)