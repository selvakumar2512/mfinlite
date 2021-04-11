# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 10:11:36 2020

@author: Abinesh
"""

from django.urls import path
from .views import newloan_view, manageloan_view, loansearch_view, collection_view
from .views import get_total_amount, get_transaction_no, foreclosure_view, documents_view
from .views import welcome_view, receipt_view, soa_view, repayment_view, reports_view
from .views import overdue_view, forecast_view
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'loans'

urlpatterns = [
    path('loan/',                   newloan_view,       name="loans_new"),
    path('loan/search',             loansearch_view,    name="loans_search"),
    path('loan/manage',             manageloan_view,    name="loans_manage"),
    path('loan/collection',         collection_view,    name="loans_collection"),
    path('loan/foreclosure',        foreclosure_view,   name="loans_foreclosure"),
    path('loan/documents',          documents_view,     name="loans_documents"),
    path('loan/generate/receipt',   receipt_view,       name="loans_receipt"),
    path('loan/generate/welcome',   welcome_view,       name="loans_welcome"),
    path('loan/generate/soa',       soa_view,           name="loans_soa"),
    path('loan/generate/repayment', repayment_view,     name="loans_repay"),
    path('loan/reports/collection', reports_view,       name="collections"),
    path('loan/reports/overdue',    overdue_view,       name="overdue"),
    path('loan/reports/forecast',   forecast_view,      name="forecast"),
    
    path('get/ajax/getTransactionNo/', get_transaction_no, name="get_trans"),
    path('get/ajax/getTotalAmount/', get_total_amount, name="get_amount")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)