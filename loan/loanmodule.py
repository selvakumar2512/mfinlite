# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 21:34:04 2021

@author: Abinesh
"""

from django.contrib.auth.decorators import login_required
from .forms import LoanForm, AssetForm, TransactionsForm
from .models import LoanMaster, LoanAsset, LoanTransactions
from customer.models import Customer
from django.db.models import Q
from django.shortcuts import get_object_or_404
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import decimal
from django.db.models import Q, Sum, F, DecimalField, Func, Count, Case, When

def is_valid(param):
    return param != '' and param is not None

def add_transactions(loanobj,trans_type,trans_status,deb_crd,due_date,amount,request):
    payment_mode = ''
    payment_date = None
    if trans_type == 'I':
        payment_mode = loanobj.payment_mode
    else:
        payment_mode = loanobj.first_payment
        if trans_status == 'F':
            payment_date = loanobj.disbursal_date
    loantrans = LoanTransactions(
                        client              = loanobj.client,
                        loan                = loanobj,
                        transaction_type    = trans_type,
                        transaction_status  = trans_status,
                        posting_date        = date.today(),
                        due_date            = due_date,
                        payment_mode        = payment_mode,
                        debit_credit        = deb_crd,
                        total_amount        = amount,
                        payment_date        = payment_date,
                        created_on          = datetime.now(),
                        created_by          = str(request.user),
                        changed_on          = datetime.now(),
                        changed_by          = str(request.user),
                            )
    loantrans.save()

def fill_loanform(trans,loanobj):
### Calculate Paid, Overdue and Advance Instalments    
    overdue = trans.filter(Q(due_date__lt=datetime.today()) & ~Q(transaction_status='F')).count()
    paid    = trans.filter(Q(transaction_status='F') & Q(transaction_type='I')).count()
    advance = trans.filter(Q(due_date__gt=datetime.today()) & Q(transaction_status='F')).count()
## Initialize Loan Master
    loanform = LoanForm(initial={
                        'client':              loanobj.client,
                        'loan_no':             loanobj.loan_no,
                        'ext_loan_no':         loanobj.ext_loan_no,
                        'branch':              loanobj.branch,
                        'profitcentre':        loanobj.profitcentre,
                        'costcentre':          loanobj.costcentre,
                        'product':             loanobj.product,
                        'currency':            loanobj.currency,
                        'application_no':      loanobj.application_no,
                        'application_date':    loanobj.application_date,
                        'customer':            loanobj.customer.customer_id,
                        'customer_name':       loanobj.customer.full_name,
                        'bank_name':           loanobj.bank_name,
                        'bank_branch':         loanobj.bank_branch,
                        'bank_ifsc':           loanobj.bank_ifsc,
                        'bank_account':        loanobj.bank_account,
                        'amount_finance':      loanobj.amount_finance,
                        'service_charges':     loanobj.service_charges,
                        'gst_charges':         loanobj.gst_charges,
                        'vat_charges':         loanobj.vat_charges,
                        'cess_charges':        loanobj.cess_charges,
                        'other_charges':       loanobj.other_charges,
                        'amount_disburse':     loanobj.amount_disburse,
                        'principal_os':        loanobj.principal_os,
                        'latepayment_os':      loanobj.latepayment_os,
                        'cbc_os':              loanobj.cbc_os,
                        'amount_first_instal': loanobj.amount_first_instal,
                        'disbursal_date':      loanobj.disbursal_date,
                        'interest_rate':       loanobj.interest_rate,
                        'interest_start':      loanobj.interest_start,
                        'due_date':            loanobj.due_date,
                        'instalment_type':     loanobj.instalment_type,
                        'instalment_start':    loanobj.instalment_start,
                        'instalment_end':      loanobj.instalment_end,
                        'payment_mode':        loanobj.payment_mode,
                        'first_payment':       loanobj.first_payment,
                        'total_instalments':   loanobj.total_instalments,
                        'advance_instalments': advance,
                        'paid_instalments':    paid,
                        'overdue_instalments': overdue,
                        'loan_status':         loanobj.loan_status,
                        'disbursal_status':    loanobj.disbursal_status,
                        })
    return loanform
    
def update_loan(loanobj,customer_obj,loanform,request):
    loanobj.client_id           = loanform.cleaned_data.get("client_id")
    loanobj.loan_no             = loanform.cleaned_data.get("loan_no")
    loanobj.ext_loan_no         = loanform.cleaned_data.get("ext_loan_no")
    loanobj.branch              = loanform.cleaned_data.get("branch")
    loanobj.profitcentre        = loanform.cleaned_data.get("profitcentre")                
    loanobj.costcentre          = loanform.cleaned_data.get("costcentre")
    loanobj.product             = loanform.cleaned_data.get("product")
    loanobj.currency            = loanform.cleaned_data.get("currency")
    loanobj.application_no      = loanform.cleaned_data.get("application_no")
    loanobj.application_date    = loanform.cleaned_data.get("application_date")
    loanobj.customer            = customer_obj
    loanobj.bank_name           = loanform.cleaned_data.get("bank_name")
    loanobj.bank_branch         = loanform.cleaned_data.get("bank_branch")
    loanobj.bank_ifsc           = loanform.cleaned_data.get("bank_ifsc")
    loanobj.bank_account        = loanform.cleaned_data.get("bank_account")
    loanobj.amount_finance      = loanform.cleaned_data.get("amount_finance")
    loanobj.service_charges     = loanform.cleaned_data.get("service_charges")
    loanobj.gst_charges         = loanform.cleaned_data.get("gst_charges")
    loanobj.vat_charges         = loanform.cleaned_data.get("vat_charges")
    loanobj.cess_charges        = loanform.cleaned_data.get("cess_charges")
    loanobj.other_charges       = loanform.cleaned_data.get("other_charges")
    loanobj.amount_disburse     = loanform.cleaned_data.get("amount_disburse")
    loanobj.principal_os        = loanform.cleaned_data.get("principal_os")
    loanobj.latepayment_os      = loanform.cleaned_data.get("latepayment_os")
    loanobj.cbc_os              = loanform.cleaned_data.get("cbc_os")
    loanobj.amount_first_instal = loanform.cleaned_data.get("amount_first_instal")
    loanobj.disbursal_date      = loanform.cleaned_data.get("disbursal_date")
    loanobj.interest_rate       = loanform.cleaned_data.get("interest_rate")
    loanobj.interest_start      = loanform.cleaned_data.get("interest_start")
    loanobj.due_date            = loanform.cleaned_data.get("due_date")
    loanobj.instalment_type     = loanform.cleaned_data.get("instalment_type")
    loanobj.instalment_start    = loanform.cleaned_data.get("instalment_start")
    loanobj.instalment_end      = loanform.cleaned_data.get("instalment_end")
    loanobj.payment_mode        = loanform.cleaned_data.get("payment_mode")
    loanobj.first_payment       = loanform.cleaned_data.get("first_payment")
    loanobj.total_instalments   = loanform.cleaned_data.get("total_instalments")
    loanobj.advance_instalments = loanform.cleaned_data.get("advance_instalments")
    loanobj.paid_instalments    = loanform.cleaned_data.get("paid_instalments")
    loanobj.overdue_instalments = loanform.cleaned_data.get("overdue_instalments")
    loanobj.loan_status         = loanform.cleaned_data.get("loan_status")
    loanobj.disbursal_status    = loanform.cleaned_data.get("disbursal_status")
    loanobj.changed_on          = datetime.now()
    loanobj.changed_by          = str(request.user)
    loanobj.update()

def fill_assetform(loanobj,asset):
    assetform = AssetForm(initial={
                                    'loan':                 loanobj.loan_no,
                                    'asset_no':             asset.asset_no,
                                    'asset_desc':           asset.asset_desc,
                                    'quantity':             asset.quantity,
                                    'invoice_no':           asset.invoice_no,
                                    'invoice_date':         asset.invoice_date,
                                    'make':                 asset.make,
                                    'model':                asset.model,
                                    'chasis_no':            asset.chasis_no,
                                    'engine_no':            asset.engine_no,
                                    'color':                asset.color,
                                    'year':                 asset.year,
                                    'registration_no':      asset.registration_no,
                                    'rto':                  asset.rto,
                                    'supplier':             asset.supplier,
                                    'category':             asset.category,
                                    'reposession_date':     asset.reposession_date,
                                    'sales_date':           asset.sales_date,
                                    'imei1':                asset.imei1,
                                    'imei2':                asset.imei2,
                                    'invoice_remark':       asset.invoice_remark,
                                    'asset_cost':           asset.asset_cost,
                                    'blue_book_value':      asset.blue_book_value,
                                    'value':                asset.value,
                                    'sales_value':          asset.sales_value,
                                    'rbi_code':             asset.rbi_code,
                                    'delivery_order':       asset.delivery_order,
                                    'do_date':              asset.do_date,
                                    'first_inspect_date':   asset.first_inspect_date,
                                    'regd_remark':          asset.regd_remark,
                                    'rc_status':            asset.rc_status,
                                    'rcsu_date':            asset.rcsu_date,
                                        })      
    return assetform
       
def update_asset(asset,loanobj,assetform,request):
    asset.client              = loanobj.client
    asset.loan                = loanobj
    asset.asset_no            = assetform.cleaned_data.get("asset_no")
    asset.asset_desc          = assetform.cleaned_data.get("asset_desc")
    asset.quantity            = assetform.cleaned_data.get("quantity")
    asset.invoice_no          = assetform.cleaned_data.get("invoice_no")
    asset.invoice_date        = assetform.cleaned_data.get("invoice_date")
    asset.make                = assetform.cleaned_data.get("make")
    asset.model               = assetform.cleaned_data.get("model")
    asset.chasis_no           = assetform.cleaned_data.get("chasis_no")
    asset.engine_no           = assetform.cleaned_data.get("engine_no")
    asset.color               = assetform.cleaned_data.get("color")
    asset.year                = assetform.cleaned_data.get("year")
    asset.registration_no     = assetform.cleaned_data.get("registration_no")
    asset.rto                 = assetform.cleaned_data.get("rto")
    asset.supplier            = assetform.cleaned_data.get("supplier")
    asset.category            = assetform.cleaned_data.get("category")
    asset.reposession_date    = assetform.cleaned_data.get("reposession_date")
    asset.sales_date          = assetform.cleaned_data.get("sales_date")
    asset.imei1               = assetform.cleaned_data.get("imei1")
    asset.imei2               = assetform.cleaned_data.get("imei2")
    asset.invoice_remark      = assetform.cleaned_data.get("invoice_remark")
    asset.asset_cost          = assetform.cleaned_data.get("asset_cost")
    asset.blue_book_value     = assetform.cleaned_data.get("blue_book_value")
    asset.value               = assetform.cleaned_data.get("value")
    asset.sales_value         = assetform.cleaned_data.get("sales_value")
    asset.rbi_code            = assetform.cleaned_data.get("rbi_code")
    asset.delivery_order      = assetform.cleaned_data.get("delivery_order")
    asset.do_date             = assetform.cleaned_data.get("do_date")
    asset.first_inspect_date  = assetform.cleaned_data.get("first_inspect_date")
    asset.regd_remark         = assetform.cleaned_data.get("regd_remark")
    asset.rc_status           = assetform.cleaned_data.get("rc_status")
    asset.rcsu_date           = assetform.cleaned_data.get("rcsu_date")
    asset.changed_on          = datetime.now()
    asset.changed_by          = str(request.user) 
    asset.update()

def update_trans(trans,loanobj,transform,request):
    trans.client            = loanobj.client
    trans.loan              = loanobj
    trans.paid_amount       = transform.cleaned_data.get("paid_amount")
    trans.payment_date      = transform.cleaned_data.get("payment_date")
    trans.payment_no        = transform.cleaned_data.get("payment_no")
    trans.payment_mode      = transform.cleaned_data.get("payment_mode")
    trans.cheque_bank       = transform.cleaned_data.get("cheque_bank")
    trans.invoice_reference = transform.cleaned_data.get("invoice_reference")
    trans.changed_on        = datetime.now()
    trans.changed_by        = str(request.user) 
    if trans.paid_amount == trans.total_amount:
        trans.transaction_status = 'F'
    else:
        trans.transaction_status = 'P'
    trans.save()
    
def PMT(rate, nper, pv):
    freq_rate = ( rate / nper ) * ( nper / 12 )
    int_rate = (1 + freq_rate) ** nper
    pmt = ( pv * freq_rate * int_rate ) / (int_rate - 1)
    return(pmt)

def repayment_schedule(loan_no):
    
    loanobj = LoanMaster.objects.none()
    repayment = []
 
### Get Loan Master
    if is_valid(loan_no):
        loanobj = get_object_or_404(LoanMaster, loan_no=loan_no)
    
    if loanobj:
### Get Number of Instalments per annum
        if loanobj.instalment_type == 'W':
           instal_annual = 52
           add_days      = relativedelta(days=7)
        elif loanobj.instalment_type == 'B':
           instal_annual = 26
           add_days      = relativedelta(days=14)
        elif loanobj.instalment_type == 'M':
           instal_annual = 12
           add_days      = relativedelta(months=1)
        elif loanobj.instalment_type == 'Q':
           instal_annual = 4
           add_days      = relativedelta(months=3)
### Principal Amount, Instalment Start and Balance
        principal       = decimal.Decimal(float(loanobj.amount_finance))
        balance         = decimal.Decimal(float(loanobj.amount_finance))
        due_date        = loanobj.instalment_start
        total_inst      = decimal.Decimal(float(loanobj.total_instalments))
        annual_interest = decimal.Decimal(float(loanobj.interest_rate))
        payment         = 1

### Generate Schedule
        while payment <= total_inst:
            pmt = PMT(annual_interest/100, total_inst, principal)
            ipmt = ((annual_interest/100)*balance/instal_annual)
            ppmt = pmt - ipmt
            balance-=ppmt
            pmt  = round(pmt,0)
            ipmt = round(ipmt,0)
            ppmt = round(ppmt,0)

            repayment.append({'number': payment, 'due_date':due_date, 'instalment': pmt, 'principal': ppmt, 'interest': ipmt, 'balance': round(balance,0)})
            due_date+=add_days
            payment+=1
            
        return(repayment)
    
def trans_summary(loan_no):
    loanobj         = LoanMaster.objects.none()
    instal_annual   = 1
    paid_instal     = 0
    unpaid_instal   = 0
    overdue_instal  = 0
    charges_os      = decimal.Decimal('0.00')
    principal_os    = decimal.Decimal('0.00')
    total           = decimal.Decimal('0.00')
    
### Get Loan Master
    if is_valid(loan_no):
        loanobj = get_object_or_404(LoanMaster, loan_no=loan_no)
    
    
    if loanobj:
        annual_interest = decimal.Decimal(float(loanobj.interest_rate))
        total_inst      = decimal.Decimal(float(loanobj.total_instalments))
        principal       = decimal.Decimal(float(loanobj.amount_finance))
        instal_type     = loanobj.instalment_type
        
        if instal_type == 'W':
           instal_annual = 52
        elif instal_type == 'B':
           instal_annual = 26
        elif instal_type == 'M':
           instal_annual = 12
        elif instal_type == 'Q':
           instal_annual = 4
           
        loantrans = LoanTransactions.objects.filter(Q(loan=loanobj))
        paidtrans = LoanTransactions.objects.filter(Q(loan=loanobj) & ~Q(transaction_status='O'))
        if loantrans:
            for trans in loantrans:
                if trans.transaction_type == 'I':
                    if trans.transaction_status == 'F':
                        paid_instal+=1
                    else:
                        unpaid_instal+=1
                        if trans.due_date < date.today():
                            overdue_instal+=1
                elif ( trans.transaction_type == 'C' or
                       trans.transaction_type == 'L' or 
                       trans.transaction_type == 'O' or
                       trans.transaction_type == 'S' or
                       trans.transaction_type == 'V' or
                       trans.transaction_type == 'G' or
                       trans.transaction_type == 'E' or
                       trans.transaction_type == 'T'
                       ):
                    charges_os+=trans.total_amount
                
                if trans.transaction_status == 'F':
                    if trans.debit_credit == 'D':
                        total+=trans.total_amount
                    else:
                        total-=trans.total_amount
                elif trans.transaction_status == 'P':
                    if trans.debit_credit == 'D':
                        total+=trans.paid_amount
                    else:
                        total-=trans.paid_amount 
### Principal O/S
            inst_amount = PMT(annual_interest/100, total_inst, principal)
            period_interest = annual_interest/100/instal_annual
            rem_interest = 1 / ( (1 + period_interest)**unpaid_instal )
            principal_os = inst_amount * ( (1 - rem_interest) / period_interest )
            principal_os = round(principal_os,0)
        
    return principal_os, paid_instal, unpaid_instal, charges_os, overdue_instal, paidtrans, total
        