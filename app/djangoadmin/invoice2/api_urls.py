from django.urls import path

import invoice2.api_views

urlpatterns = [
    # Customer views
    path('customer/infos/', invoice2.api_views.customer_infos),

    # Product views
    path('product/infos/', invoice2.api_views.product_infos),
]
