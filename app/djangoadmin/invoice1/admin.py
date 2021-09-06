from django.contrib import admin

import invoice1.models

admin.site.register(invoice1.models.Customer)
admin.site.register(invoice1.models.CustomerAddress)
admin.site.register(invoice1.models.Product)
admin.site.register(invoice1.models.Invoice)
admin.site.register(invoice1.models.InvoiceItem)