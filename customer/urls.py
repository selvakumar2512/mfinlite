# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 17:47:30 2020

@author: Abinesh
"""

from django.urls import path
from .views import customer_view, custsearch_view, custmanage_view
from django.conf import settings
from django.conf.urls.static import static
#from django.contrib.auth.views import LogoutView
# from . import views

# app_name = 'customer'
app_name = 'customers'

urlpatterns = [
    # path('customers/', customer_view, name="customers_main"),
    path('customer/', customer_view, name="customers_main"),
    path('customer/search', custsearch_view, name="customers_search"),
    path('customer/manage', custmanage_view, name="customers_manage"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)