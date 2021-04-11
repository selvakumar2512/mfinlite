# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 15:11:39 2020

@author: Abinesh
"""

from django import forms
from .models import LoanMaster, LoanAsset, LoanTransactions
from masterdata.models import Client, ProfitCentre, Branch, CostCentre, Product, Currency
from django.forms import DateInput
from datetime import date
from decimal import Decimal
import decimal
from django.shortcuts import get_object_or_404
from django.db.models import Q

class LoanForm(forms.Form):
## Loan Master    
    client_id   = forms.ModelChoiceField(queryset=Client.objects.all(), 
                                         initial={'client_id': Client.pk},
                                         widget=forms.Select(
                                          attrs={ 'class': 'form-select' } ))    
    loan_no     = forms.CharField( max_length=15, required=False, 
                                   widget=forms.TextInput( 
                                          attrs={ "class": "form-control", 
                                                  "readonly": "readonly" } ),)
    ext_loan_no = forms.CharField( max_length=30, required=False,
                                   widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    branch   = forms.ModelChoiceField(queryset=Branch.objects.all(), 
                                         initial={'branch': Branch.pk},
                                         widget=forms.Select(
                                          attrs={ 'class': 'form-select',
                                                  'float': 'right'} ))
    profitcentre   = forms.ModelChoiceField(queryset=ProfitCentre.objects.all(), 
                                         initial={'profitcentre': ProfitCentre.pk},
                                         widget=forms.Select(
                                          attrs={ 'class': 'form-select' } ))
    costcentre   = forms.ModelChoiceField(queryset=CostCentre.objects.all(), 
                                         initial={'costcentre': CostCentre.pk},
                                         widget=forms.Select(
                                          attrs={ 'class': 'form-select' } ))
    product   = forms.ModelChoiceField(queryset=Product.objects.all(), 
                                         initial={'product': Product.pk},
                                         widget=forms.Select(
                                          attrs={ 'class': 'form-select' } ))
    currency   = forms.ModelChoiceField(queryset=Currency.objects.all(), 
                                         initial={'currency': 'INR'},
                                         widget=forms.Select(
                                          attrs={ 'class': 'form-select' } ))
## Applicant Details    
    application_no    = forms.CharField(max_length=30, required=False,
                                   widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    application_date = forms.DateField(widget = DateInput(attrs={'type': 'date'}),
                                       initial=date.today())    
    customer    = forms.CharField( max_length=12, required=True,
                                   widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    customer_name = forms.CharField(max_length=80, required=False,
                                   widget=forms.TextInput( 
                                          attrs={ "class": "form-control",
                                                  "readonly": "readonly" } ),)
    bank_name    = forms.CharField(max_length=40, required=False,
                                   widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    bank_branch    = forms.CharField(max_length=40, required=False,
                                   widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    bank_ifsc    = forms.CharField(max_length=40, required=False,
                                   widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    bank_account    = forms.CharField(max_length=40, required=False,
                                   widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
## Amount and Charges
    amount_finance = forms.DecimalField(max_digits=15, decimal_places=2, required=False,
                                        widget=forms.NumberInput( 
                                          attrs={ "class": "form-control",
                                                  "type": "number" } ),)
    service_charges = forms.DecimalField(max_digits=15, decimal_places=2, required=False,
                                        widget=forms.NumberInput( 
                                          attrs={ "class": "form-control",
                                                  "type": "number" } ),)
    gst_charges = forms.DecimalField(max_digits=15, decimal_places=2, required=False,
                                        widget=forms.NumberInput( 
                                          attrs={ "class": "form-control",
                                                  "type": "number" } ),)
    vat_charges = forms.DecimalField(max_digits=15, decimal_places=2, required=False,
                                        widget=forms.NumberInput( 
                                          attrs={ "class": "form-control",
                                                  "type": "number" } ),)
    cess_charges = forms.DecimalField(max_digits=15, decimal_places=2, required=False,
                                        widget=forms.NumberInput( 
                                          attrs={ "class": "form-control",
                                                  "type": "number" } ),)
    other_charges = forms.DecimalField(max_digits=15, decimal_places=2, required=False,
                                        widget=forms.NumberInput( 
                                          attrs={ "class": "form-control",
                                                  "type": "number" } ),)
    amount_disburse = forms.DecimalField(max_digits=15, decimal_places=2, required=False,
                                        widget=forms.NumberInput( 
                                          attrs={ "class": "form-control",
                                                  "type": "number" } ),)
    principal_os = forms.DecimalField(max_digits=15, decimal_places=2, required=False,
                                        widget=forms.NumberInput( 
                                          attrs={ "class": "form-control",
                                                  "type": "number" } ),)
    latepayment_os = forms.DecimalField(max_digits=15, decimal_places=2, required=False,
                                        widget=forms.NumberInput( 
                                          attrs={ "class": "form-control",
                                                  "type": "number" } ),)
    cbc_os = forms.DecimalField(max_digits=15, decimal_places=2, required=False,
                                        widget=forms.NumberInput( 
                                          attrs={ "class": "form-control",
                                                  "type": "number" } ),)
    amount_first_instal = forms.DecimalField(max_digits=15, decimal_places=2, required=False,
                                        widget=forms.NumberInput( 
                                          attrs={ "class": "form-control",
                                                  "type": "number" } ),)
## Instalment Details
    disbursal_date = forms.DateField(widget = DateInput(attrs={'type': 'date'}),
                                  initial=date.today())
    interest_rate  = forms.DecimalField(max_digits=5, decimal_places=2, required=True,
                                        initial={'interest_date': '16.00'},
                                        widget=forms.NumberInput( 
                                          attrs={ "class": "form-control",
                                                  "type": "number" } ),)
    interest_start = forms.DateField(widget = DateInput(attrs={'type': 'date'}),
                                  initial=date.today())
    due_date = forms.IntegerField(widget=forms.NumberInput( 
                                          attrs={ "class": "form-control",
                                                  "type": "number" } ),)
    instalment_type = forms.ChoiceField(choices=LoanMaster.INSTAL_LIST, 
                                        widget=forms.Select(
                                          attrs={ 'class': 'form-select' } ))
    instalment_start = forms.DateField(widget = DateInput(attrs={'type': 'date'}),
                                  initial=date.today())
    instalment_end = forms.DateField(widget = DateInput(attrs={'type': 'date'}),)
    payment_mode = forms.ChoiceField(choices=LoanMaster.PAYMENT_LIST, 
                                        widget=forms.Select(
                                          attrs={ 'class': 'form-select' } ))
    first_payment = forms.ChoiceField(choices=LoanMaster.PAYMENT_LIST, 
                                        widget=forms.Select(
                                          attrs={ 'class': 'form-select' } ))
    total_instalments = forms.IntegerField(widget=forms.NumberInput( 
                                          attrs={ "class": "form-control",
                                                  "type": "number" } ),)
    advance_instalments = forms.IntegerField(required=False, widget=forms.NumberInput( 
                                          attrs={ "class": "form-control",
                                                  "type": "number" } ),)
    paid_instalments = forms.IntegerField(required=False, widget=forms.NumberInput( 
                                          attrs={ "class": "form-control",
                                                  "type": "number" } ),)
    overdue_instalments = forms.IntegerField(required=False, widget=forms.NumberInput( 
                                          attrs={ "class": "form-control",
                                                  "type": "number" } ),)
## Status
    loan_status = forms.ChoiceField(choices=LoanMaster.STATUS_LIST, 
                                        widget=forms.Select(
                                          attrs={ 'class': 'form-select' } ))
    disbursal_status = forms.ChoiceField(choices=LoanMaster.DISB_STATUS_LIST, 
                                        widget=forms.Select(
                                          attrs={ 'class': 'form-select' } ))

class AssetForm(forms.Form):
    loan                = forms.CharField( max_length=15, required=False, 
                                   widget=forms.TextInput( 
                                          attrs={ "class": "form-control", 
                                                  "readonly": "readonly" } ),)
    asset_no            = forms.CharField( max_length=15, required=True, 
                                    widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    asset_desc          = forms.CharField(max_length=80, required=False,
                                   widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    quantity            = forms.IntegerField(required=True, widget=forms.NumberInput( 
                                          attrs={ "class": "form-control",
                                                  "type": "number" } ),)
    invoice_no          = forms.CharField(max_length=40, required=False,
                                    widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    invoice_date        = forms.DateField(required=False, widget = DateInput(attrs={'type': 'date'}),)
    make                = forms.CharField(max_length=80, required=False,
                                    widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    model               = forms.CharField(max_length=80, required=False,
                                    widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    chasis_no           = forms.CharField(max_length=80, required=False,
                                    widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    engine_no           = forms.CharField(max_length=30, required=False,
                                    widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    color               = forms.CharField(max_length=30, required=False,
                                    widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    year                = forms.IntegerField(required=True, widget=forms.NumberInput( 
                                          attrs={ "class": "form-control",
                                                  "type": "number" } ),)
    registration_no     = forms.CharField(max_length=30, required=False,
                                    widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    rto                 = forms.CharField(max_length=30, required=False,
                                    widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    supplier            = forms.CharField(max_length=80, required=False,
                                    widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    category            = forms.CharField(max_length=30, required=False,
                                    widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    reposession_date    = forms.DateField(required=False, widget = DateInput(attrs={'type': 'date'}),)
    sales_date          = forms.DateField(required=False, widget = DateInput(attrs={'type': 'date'}),)
    imei1               = forms.CharField(max_length=30, required=False,
                                    widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    imei2               = forms.CharField(max_length=30, required=False,
                                    widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    invoice_remark      = forms.CharField(max_length=80, required=False,
                                    widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    asset_cost          = forms.DecimalField(max_digits=15, decimal_places=2, 
                                             required=False,
                                        widget=forms.NumberInput( 
                                          attrs={ "class": "form-control",
                                                  "type": "number" } ),)
    blue_book_value     = forms.DecimalField(max_digits=15, decimal_places=2, 
                                             required=False,
                                        widget=forms.NumberInput( 
                                          attrs={ "class": "form-control",
                                                  "type": "number" } ),)
    value               = forms.DecimalField(max_digits=15, decimal_places=2, 
                                             required=False,
                                        widget=forms.NumberInput( 
                                          attrs={ "class": "form-control",
                                                  "type": "number" } ),)
    sales_value         = forms.DecimalField(max_digits=15, decimal_places=2, 
                                             required=False,
                                        widget=forms.NumberInput( 
                                          attrs={ "class": "form-control",
                                                  "type": "number" } ),)
    rbi_code            = forms.CharField(max_length=30, required=False,
                                    widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    delivery_order      = forms.ChoiceField(choices=LoanAsset.DELIVERY_ORDER_LIST, 
                                        widget=forms.Select(
                                          attrs={ 'class': 'form-select' } ))
    do_date             = forms.DateField(required=False, widget = DateInput(attrs={'type': 'date'}),)
    first_inspect_date  = forms.DateField(required=False, widget = DateInput(attrs={'type': 'date'}),)
    regd_remark         = forms.CharField(max_length=80, required=False,
                                    widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    rc_status           = forms.CharField(max_length=20, required=False,
                                    widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    rcsu_date           = forms.DateField(required=False, widget = DateInput(attrs={'type': 'date'}),)
    
class TransactionsForm(forms.Form):
    loan               = forms.CharField( max_length=15, required=False, 
                                   widget=forms.TextInput( 
                                          attrs={ "class": "form-control", 
                                                  "readonly": "readonly" } ),)
    transaction_type    = forms.ChoiceField(choices=LoanTransactions.TRANSACTION_TYPE_LIST, 
                                        widget=forms.Select(
                                          attrs={ 'class': 'form-select' } ))
    due_date           = forms.DateField(widget = DateInput(attrs={'type': 'date'}),
                                  initial=date.today())
    debit_credit       = forms.ChoiceField(choices=LoanTransactions.DEBIT_LIST, 
                                        widget=forms.Select(
                                          attrs={ 'class': 'form-select' } ))
    total_amount       = forms.DecimalField(max_digits=15, decimal_places=2, 
                                             required=False,
                                        widget=forms.NumberInput( 
                                          attrs={ "class": "form-control",
                                                  "type": "number" } ),)
class SearchForm(forms.Form):
    customer    = forms.CharField( max_length=12, required=False,
                                   widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    full_name = forms.CharField( max_length=160, required=False,
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    village = forms.CharField( max_length=80, required=False,
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    taluk    = forms.CharField( max_length=80, required=False,
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    district = forms.CharField( max_length=80, required=False,
                                       widget=forms.TextInput( 
                                           attrs={ "class": "form-control" } ),)                                  
    city = forms.CharField( max_length=40,  required=False,
                                      widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    loan_no     = forms.CharField( max_length=15, required=False, 
                                   widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    ext_loan_no = forms.CharField( max_length=30, required=False,
                                   widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    branch   = forms.ModelChoiceField(queryset=Branch.objects.all(), 
                                         empty_label='NA',
                                         required=False,
                                         widget=forms.Select(
                                          attrs={ 'class': 'form-select',
                                                  'float': 'right'} ))
    profitcentre   = forms.ModelChoiceField(queryset=ProfitCentre.objects.all(), 
                                         empty_label='NA',
                                         required=False,
                                         widget=forms.Select(
                                          attrs={ 'class': 'form-select' } ))
    costcentre   = forms.ModelChoiceField(queryset=CostCentre.objects.all(), 
                                         empty_label='NA',
                                         required=False,
                                         widget=forms.Select(
                                          attrs={ 'class': 'form-select' } ))
    product   = forms.ModelChoiceField(queryset=Product.objects.all(), 
                                         empty_label='NA',
                                         required=False,
                                         widget=forms.Select(
                                          attrs={ 'class': 'form-select' } ))
    start_date           = forms.DateField(widget = DateInput(attrs={'type': 'date'}),
                                           required=False,
                                           initial=date.today())
    end_date           = forms.DateField(widget = DateInput(attrs={'type': 'date'}),
                                         required=False,
                                         initial=date.today())

class CollectionForm(forms.Form):
            
    loan_no           = forms.CharField( max_length=15, required=False, 
                                   widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    transaction_type  = forms.ChoiceField(choices=LoanTransactions.TRANSACTION_TYPE_LIST, 
                                          widget=forms.Select(
                                          attrs={ 'class': 'form-select' } ))
    transaction_no    = forms.ModelChoiceField(queryset=LoanTransactions.objects.none(),
                                               to_field_name='transaction_no',
                                               required=False,
                                               widget=forms.Select(
                                               attrs={ 'class': 'form-select' } ))
    payment_mode      = forms.ChoiceField(choices=LoanTransactions.PAYMENT_LIST, 
                                        widget=forms.Select(
                                          attrs={ 'class': 'form-select' } ))
    payment_no        = forms.CharField(max_length=20, required=False,
                                    widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    cheque_bank       = forms.CharField(max_length=40, required=False,
                                    widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    payment_date      = forms.DateField(widget = DateInput(attrs={'type': 'date'}),
                                        initial=date.today())
    total_amount      = forms.DecimalField(max_digits=15, decimal_places=2, 
                                             required=False,
                                        widget=forms.NumberInput( 
                                          attrs={ "class": "form-control",
                                                  "type": "number",
                                                  "readonly": "readonly" } ),)
    paid_amount       = forms.DecimalField(initial=Decimal('0.00'), max_digits=15, decimal_places=2, 
                                             required=False,
                                        widget=forms.NumberInput( 
                                          attrs={ "class": "form-control",
                                                  "type": "number" } ),)
    invoice_no        = forms.CharField(max_length=20, required=False,
                                    widget=forms.TextInput( 
                                          attrs={ "class": "form-control",
                                                 "readonly": "readonly" } ),)
    invoice_reference = forms.CharField(max_length=40, required=False,
                                    widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['transaction_no'].queryset = LoanTransactions.objects.none().only("transaction_no")
        
        if 'transaction_type' in self.data:
            try:
                trans_type = self.data.get("transaction_type")
                loan_no    = self.data.get("loan_no")
                loanobj = get_object_or_404(LoanMaster, loan_no=loan_no)
                self.fields['transaction_no'].queryset = LoanTransactions.objects.filter(
                                                                    Q(loan=loanobj) & Q(transaction_type=trans_type)
                                                                 & ~Q(transaction_status='F')).order_by().values_list("transaction_no", flat=True).distinct()
            except:
                pass

class ClosureForm(forms.Form):
            
    loan_no           = forms.CharField( max_length=15, required=False, 
                                   widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    os_amount         = forms.DecimalField(max_digits=15, decimal_places=2, 
                                             required=False,
                                        widget=forms.NumberInput( 
                                          attrs={ "class": "form-control",
                                                  "type": "number",
                                                  "readonly": "readonly" } ),)
    closure_charges   = forms.DecimalField(max_digits=15, decimal_places=2, 
                                             required=False,
                                        widget=forms.NumberInput( 
                                          attrs={ "class": "form-control",
                                                  "type": "number" } ),)
    total_amount      = forms.DecimalField(max_digits=15, decimal_places=2, 
                                             required=False,
                                        widget=forms.NumberInput( 
                                          attrs={ "class": "form-control",
                                                  "type": "number" } ),)
    payment_mode      = forms.ChoiceField(choices=LoanTransactions.PAYMENT_LIST,required=False,
                                        widget=forms.Select(
                                          attrs={ 'class': 'form-select' } ))
    payment_no        = forms.CharField(max_length=20, required=False,
                                    widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    cheque_bank       = forms.CharField(max_length=40, required=False,
                                    widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    payment_date      = forms.DateField(widget = DateInput(attrs={'type': 'date'}), required=False,
                                        initial=date.today())
    invoice_no        = forms.CharField(max_length=20, required=False,
                                    widget=forms.TextInput( 
                                          attrs={ "class": "form-control",
                                                 "readonly": "readonly" } ),)
    invoice_reference = forms.CharField(max_length=40, required=False,
                                    widget=forms.TextInput( 
                                          attrs={ "class": "form-control" } ),)
    