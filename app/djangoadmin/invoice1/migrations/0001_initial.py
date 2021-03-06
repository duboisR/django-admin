# Generated by Django 3.2.7 on 2021-09-05 19:42

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import invoice1.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(blank=True, max_length=255, null=True)),
                ('company_vat', models.CharField(blank=True, max_length=255, null=True, validators=[django.core.validators.RegexValidator(message='Merci de renseigner un numéro de TVA valide. Format: BExxxxxxxxx', regex='^[A-Z]{2,4}(?=.{2,12}$)[-_\\s0-9]*(?:[a-zA-Z][-_\\s0-9]*){0,2}$')])),
                ('contact_first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('contact_last_name', models.CharField(max_length=255)),
                ('contact_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('contact_phone', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(message='Merci de renseigner le numéro de téléphone avec un indicatif international. Format: +32xxxxxxxxx.', regex='^\\+\\d{9,15}$')])),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(default=invoice1.models.generate_invoice_number, max_length=255, unique=True)),
                ('invoice_date', models.DateField(default=django.utils.timezone.now)),
                ('terms_payment', models.CharField(choices=[('15', '15 jours'), ('15_end', '15 jours fin de mois'), ('30', '30 jours'), ('30_end', '30 jours fin de mois'), ('60', '60 jours'), ('60_end', '60 jours fin de mois'), ('90', '90 jours'), ('90_end', '90 jours fin de mois'), ('cash', 'Au comptant')], default='15', max_length=25)),
                ('discount', models.DecimalField(decimal_places=2, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0.00')), django.core.validators.MaxValueValidator(Decimal('100'))])),
                ('company_name', models.CharField(blank=True, max_length=255, null=True)),
                ('company_vat', models.CharField(blank=True, max_length=255, null=True, validators=[django.core.validators.RegexValidator(message='Merci de renseigner un numéro de TVA valide. Format: BExxxxxxxxx', regex='^[A-Z]{2,4}(?=.{2,12}$)[-_\\s0-9]*(?:[a-zA-Z][-_\\s0-9]*){0,2}$')])),
                ('contact_first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('contact_last_name', models.CharField(max_length=255)),
                ('contact_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('contact_phone', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(message='Merci de renseigner le numéro de téléphone avec un indicatif international. Format: +32xxxxxxxxx.', regex='^\\+\\d{9,15}$')])),
                ('address_street', models.CharField(max_length=255)),
                ('address_street_number', models.CharField(blank=True, max_length=255, null=True)),
                ('address_bp', models.CharField(blank=True, max_length=255, null=True)),
                ('address_zipcode', models.CharField(max_length=5)),
                ('address_city', models.CharField(max_length=255)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='invoice1.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('vat', models.PositiveIntegerField(default=21)),
                ('price', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=15)),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_description', models.TextField()),
                ('product_quantity', models.PositiveIntegerField(default=1)),
                ('product_vat', models.PositiveIntegerField(default=21)),
                ('product_price', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=15)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice1.invoice')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='invoice1.product')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_street', models.CharField(max_length=255)),
                ('address_street_number', models.CharField(blank=True, max_length=255, null=True)),
                ('address_bp', models.CharField(blank=True, max_length=255, null=True)),
                ('address_zipcode', models.CharField(max_length=5)),
                ('address_city', models.CharField(max_length=255)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='invoice1.customer')),
            ],
        ),
    ]
