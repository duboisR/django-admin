from django.http import JsonResponse

import invoice2.models


# Customer views
def customer_infos(request):
    customer_pk = request.GET.get('pk', None)
    if request.user.is_authenticated and customer_pk:
        customer_instance = invoice2.models.Customer.objects.filter(pk=customer_pk).first()
        if customer_instance:
            address_instance = customer_instance.customeraddress_set.first()
            return JsonResponse({
                'company_name': customer_instance.company_name,
                'company_vat': customer_instance.company_vat,
                'contact_first_name': customer_instance.contact_first_name,
                'contact_last_name': customer_instance.contact_last_name,
                'contact_email': customer_instance.contact_email,
                'contact_phone': customer_instance.contact_phone,
                'address_street': address_instance.address_street if address_instance else None,
                'address_street_number': address_instance.address_street_number if address_instance else None,
                'address_bp': address_instance.address_bp if address_instance else None,
                'address_zipcode': address_instance.address_zipcode if address_instance else None,
                'address_city': address_instance.address_city if address_instance else None,
            })
    return JsonResponse({})


# Product views
def product_infos(request):
    product_pk = request.GET.get('pk', None)
    if product_pk:
        product_instance = invoice2.models.Product.objects.filter(pk=product_pk).first()
        return JsonResponse({
            'product_description': product_instance.description,
            'product_vat': product_instance.vat,
            'product_price': product_instance.price,
        })
    return JsonResponse({})