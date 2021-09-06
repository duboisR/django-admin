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
    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_vat = models.CharField(validators=[djangoadmin.validators.VatValidator], max_length=255, blank=True, null=True)

    # Contact informations
    contact_first_name = models.CharField(max_length=255, blank=True, null=True)
    contact_last_name = models.CharField(max_length=255)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(validators=[djangoadmin.validators.PhoneValidator], max_length=255)


class CustomerAddress(models.Model):
    # Main information
    customer = models.ForeignKey('Customer',
        on_delete=models.CASCADE, blank=True, null=True)

    # Address informations
    address_street = models.CharField(max_length=255)
    address_street_number = models.CharField(max_length=255, blank=True, null=True)
    address_bp = models.CharField(max_length=255, blank=True, null=True)
    address_zipcode = models.CharField(max_length=5)
    address_city = models.CharField(max_length=255)


# Product Model
class Product(models.Model):
    # Detail informations
    description = models.TextField()
    vat = models.PositiveIntegerField(default=21)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal("0.00"))


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
    invoice_number = models.CharField(max_length=255, unique=True, default=generate_invoice_number)
    invoice_date = models.DateField(default=timezone.now)
    terms_payment = models.CharField(max_length=25, choices=TERMS_CHOICES, default='15')
    discount = models.DecimalField(decimal_places=2, max_digits=5, default=0,
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('100'))])

    # Customer informations
    customer = models.ForeignKey('Customer',
        on_delete=models.SET_NULL, blank=True, null=True)
    
    # Company informations
    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_vat = models.CharField(validators=[djangoadmin.validators.VatValidator], max_length=255, blank=True, null=True)

    # Contact informations
    contact_first_name = models.CharField(max_length=255, blank=True, null=True)
    contact_last_name = models.CharField(max_length=255)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(validators=[djangoadmin.validators.PhoneValidator], max_length=255)

    # Address informations
    address_street = models.CharField(max_length=255)
    address_street_number = models.CharField(max_length=255, blank=True, null=True)
    address_bp = models.CharField(max_length=255, blank=True, null=True)
    address_zipcode = models.CharField(max_length=5)
    address_city = models.CharField(max_length=255)


class InvoiceItem(models.Model):
    # Main information
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE)

    # Detail informations
    product = models.ForeignKey('Product',
        on_delete=models.SET_NULL, blank=True, null=True)
    product_description = models.TextField()
    product_quantity = models.PositiveIntegerField(default=1)
    product_vat = models.PositiveIntegerField(default=21)
    product_price = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal("0.00"))