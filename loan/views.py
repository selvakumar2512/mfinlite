from django.shortcuts import render

# Create your views here.

from django.contrib.auth.decorators import login_required
from .forms import LoanForm, AssetForm, TransactionsForm, SearchForm, CollectionForm, ClosureForm
from .models import LoanMaster, LoanAsset, LoanTransactions
from customer.models import Customer
from django.db.models import Q
from django.shortcuts import get_object_or_404
from datetime import datetime #, date
from dateutil.relativedelta import relativedelta
import decimal
from .loanmodule import *
from .pdf import *
import json
from django.http import HttpResponse
import locale
import operator
from functools import reduce

def is_valid(param):
    return param != '' and param is not None
   
@login_required(login_url="/login/")
def newloan_view(request):
    
    msg      = ''
    new_loan = 0
    
    if request.method == "POST":
        loanform  = LoanForm(request.POST)
        assetform = AssetForm(request.POST)
        if loanform.is_valid():
            customer_id = loanform.cleaned_data.get("customer")
            if customer_id:
                try:
                    customer_obj = Customer.objects.get(customer_id=customer_id)
                    loan = LoanMaster(
                        client              = loanform.cleaned_data.get("client_id"),
                        loan_no             = loanform.cleaned_data.get("loan_no"),
                        ext_loan_no         = loanform.cleaned_data.get("ext_loan_no"),
                        branch              = loanform.cleaned_data.get("branch"),
                        profitcentre        = loanform.cleaned_data.get("profitcentre"),                
                        costcentre          = loanform.cleaned_data.get("costcentre"),
                        product             = loanform.cleaned_data.get("product"),
                        currency            = loanform.cleaned_data.get("currency"),
                        application_no      = loanform.cleaned_data.get("application_no"),
                        application_date    = loanform.cleaned_data.get("application_date"),
                        customer            = customer_obj,
                        bank_name           = loanform.cleaned_data.get("bank_name"),
                        bank_branch         = loanform.cleaned_data.get("bank_branch"),
                        bank_ifsc           = loanform.cleaned_data.get("bank_ifsc"),
                        bank_account        = loanform.cleaned_data.get("bank_account"),
                        amount_finance      = loanform.cleaned_data.get("amount_finance"),
                        service_charges     = loanform.cleaned_data.get("service_charges"),
                        gst_charges         = loanform.cleaned_data.get("gst_charges"),
                        vat_charges         = loanform.cleaned_data.get("vat_charges"),
                        cess_charges        = loanform.cleaned_data.get("cess_charges"),
                        other_charges       = loanform.cleaned_data.get("other_charges"),
                        amount_disburse     = loanform.cleaned_data.get("amount_disburse"),
                        principal_os        = loanform.cleaned_data.get("principal_os"),
                        latepayment_os      = loanform.cleaned_data.get("latepayment_os"),
                        cbc_os              = loanform.cleaned_data.get("cbc_os"),
                        amount_first_instal = loanform.cleaned_data.get("amount_first_instal"),
                        disbursal_date      = loanform.cleaned_data.get("disbursal_date"),
                        interest_rate       = loanform.cleaned_data.get("interest_rate"),
                        interest_start      = loanform.cleaned_data.get("interest_start"),
                        due_date            = loanform.cleaned_data.get("due_date"),
                        instalment_type     = loanform.cleaned_data.get("instalment_type"),
                        instalment_start    = loanform.cleaned_data.get("instalment_start"),
                        instalment_end      = loanform.cleaned_data.get("instalment_end"),
                        payment_mode        = loanform.cleaned_data.get("payment_mode"),
                        first_payment       = loanform.cleaned_data.get("first_payment"),
                        total_instalments   = loanform.cleaned_data.get("total_instalments"),
                        advance_instalments = loanform.cleaned_data.get("advance_instalments"),
                        paid_instalments    = loanform.cleaned_data.get("paid_instalments"),
                        overdue_instalments = loanform.cleaned_data.get("overdue_instalments"),
                        loan_status         = loanform.cleaned_data.get("loan_status"),
                        disbursal_status    = loanform.cleaned_data.get("disbursal_status"),
                        created_on          = datetime.now(),
                        created_by          = str(request.user),
                        changed_on          = datetime.now(),
                        changed_by          = str(request.user),                
                        )
                    new_loan = loan.save()
                    msg      = 'Loan ' + str(new_loan) + ' Created Successfully'
                    loanform.cleaned_data['loan_no'] = new_loan
                    loanform.cleaned_data['customer_name'] = customer_obj.full_name                                        
                except:
                    msg = 'Invalid Customer Number. Please enter correctrect Customer Number'

            if new_loan:
##### Update Loan Asset #####
                if assetform.is_valid():
                    asset = LoanAsset(
                        client              = loanform.cleaned_data.get("client_id"),
                        loan                = LoanMaster.objects.get(loan_no=new_loan),
                        asset_no            = assetform.cleaned_data.get("asset_no"),
                        asset_desc          = assetform.cleaned_data.get("asset_desc"),
                        quantity            = assetform.cleaned_data.get("quantity"),
                        invoice_no          = assetform.cleaned_data.get("invoice_no"),
                        invoice_date        = assetform.cleaned_data.get("invoice_date"),
                        make                = assetform.cleaned_data.get("make"),
                        model               = assetform.cleaned_data.get("model"),
                        chasis_no           = assetform.cleaned_data.get("chasis_no"),
                        engine_no           = assetform.cleaned_data.get("engine_no"),
                        color               = assetform.cleaned_data.get("color"),
                        year                = assetform.cleaned_data.get("year"),
                        registration_no     = assetform.cleaned_data.get("registration_no"),
                        rto                 = assetform.cleaned_data.get("rto"),
                        supplier            = assetform.cleaned_data.get("supplier"),
                        category            = assetform.cleaned_data.get("category"),
                        reposession_date    = assetform.cleaned_data.get("reposession_date"),
                        sales_date          = assetform.cleaned_data.get("sales_date"),
                        imei1               = assetform.cleaned_data.get("imei1"),
                        imei2               = assetform.cleaned_data.get("imei2"),
                        invoice_remark      = assetform.cleaned_data.get("invoice_remark"),
                        asset_cost          = assetform.cleaned_data.get("asset_cost"),
                        blue_book_value     = assetform.cleaned_data.get("blue_book_value"),
                        value               = assetform.cleaned_data.get("value"),
                        sales_value         = assetform.cleaned_data.get("sales_value"),
                        rbi_code            = assetform.cleaned_data.get("rbi_code"),
                        delivery_order      = assetform.cleaned_data.get("delivery_order"),
                        do_date             = assetform.cleaned_data.get("do_date"),
                        first_inspect_date  = assetform.cleaned_data.get("first_inspect_date"),
                        regd_remark         = assetform.cleaned_data.get("regd_remark"),
                        rc_status           = assetform.cleaned_data.get("rc_status"),
                        rcsu_date           = assetform.cleaned_data.get("rcsu_date"),
                        created_on          = datetime.now(),
                        created_by          = str(request.user),
                        changed_on          = datetime.now(),
                        changed_by          = str(request.user), 
                    )
                asset.save()
##### Generate Loan Transactions #####
#### Update Amount Disbursed and Charges
                loanobj = LoanMaster.objects.get(loan_no=new_loan)
### Amount Finance
                if loanobj.amount_finance:
                    add_transactions(loanobj, 
                                     'D', 
                                     'F', 
                                     'D', 
                                     loanobj.disbursal_date, 
                                     loanobj.amount_finance, 
                                     request)
### Service Charges
                if loanobj.service_charges:
                    add_transactions(loanobj, 
                                     'S', 
                                     'F', 
                                     'C', 
                                     loanobj.disbursal_date, 
                                     loanobj.service_charges, 
                                     request)
### GST Charges
                if loanobj.gst_charges:
                    add_transactions(loanobj, 
                                     'G', 
                                     'F', 
                                     'C', 
                                     loanobj.disbursal_date, 
                                     loanobj.gst_charges, 
                                     request)
### VAT Charges
                if loanobj.vat_charges:
                    add_transactions(loanobj, 
                                     'V', 
                                     'F', 
                                     'C', 
                                     loanobj.disbursal_date, 
                                     loanobj.vat_charges, 
                                     request)
### CESS Charges
                if loanobj.cess_charges:
                    add_transactions(loanobj, 
                                     'E', 
                                     'F', 
                                     'C', 
                                     loanobj.disbursal_date, 
                                     loanobj.cess_charges, 
                                     request)
### Other Charges
                if loanobj.other_charges:
                    add_transactions(loanobj, 
                                     'T', 
                                     'F', 
                                     'C', 
                                     loanobj.disbursal_date, 
                                     loanobj.other_charges, 
                                     request)
#### Calculat Instlament Amount
                annual_interest = decimal.Decimal(float(loanform.cleaned_data.get("interest_rate")))
                total_inst      = decimal.Decimal(float(loanform.cleaned_data.get("total_instalments")))
                principal       = decimal.Decimal(float(loanform.cleaned_data.get("amount_finance")))
                instal_type     = loanform.cleaned_data.get("instalment_type")
                instal_annual   = 1
                        
                if instal_type == 'W':
                    instal_annual = 52
                    add_days      = relativedelta(days=7)
                elif instal_type == 'B':
                    instal_annual = 26
                    add_days      = relativedelta(days=14)
                elif instal_type == 'M':
                    instal_annual = 12
                    add_days      = relativedelta(months=1)
                elif instal_type == 'Q':
                    instal_annual = 4
                    add_days      = relativedelta(months=3)
                    
                freq_rate = ( annual_interest / total_inst / 100 ) * ( total_inst / instal_annual )
                rate = (1 + freq_rate) ** total_inst
                instal_amount = ( principal * freq_rate * rate ) / (rate - 1)
                total_amount  = round(instal_amount * total_inst,0)
                instal_amount = round(instal_amount,0)

                ins_start = loanform.cleaned_data.get("instalment_start")
                ins_end   = loanform.cleaned_data.get("instalment_end")
                    
                due_date  = ins_start

                while due_date <= ins_end:
## Save Loan Transactions
                    if due_date == ins_end: #new
                        instal_amount = total_amount
                        
                    add_transactions(loanobj, 
                                     'I', 
                                     'O', 
                                     'C', 
                                     due_date, 
                                     instal_amount, 
                                     request)
## Generate Due Date
                    due_date+=add_days   
                    total_amount = total_amount - instal_amount 
        else:
            msg = loanform.errors
    else:
        loanform = LoanForm()
        assetform = AssetForm()
        
    context = {
                'segment':      'loan-new',
                'msg':          msg,
                'new_loan':     new_loan,
                'loanform':     loanform,
                'assetform':    assetform 
              }
    return render(request, 'loans/loan-new.html', context)

### Loan Manage
@login_required(login_url="/login/")
def manageloan_view(request):
    
    loanform         = LoanForm()
    assetform        = AssetForm()
    transform        = TransactionsForm()
    loantransactions = LoanTransactions.objects.none()
    asset            = LoanAsset.objects.none()
    tab              = 'tab_master'
    action           = None
    msg              = None
    
    loan_no = request.GET.get("loan_no")
    
## Set Active Tab
    if 'get_loan' in request.GET:
        tab = 'tab_master'
        action = 'get_loan'
    elif 'get_asset' in request.GET:
        tab = 'tab_asset'
        action = 'get_asset'
    elif 'get_trans' in request.GET:
        tab = 'tab_transactions'
        action = 'get_trans'
    elif 'new_trans' in request.GET:
        tab = 'tab_transactions'
        action = 'new_trans'
    # elif 'preview' in request.GET:
    #     tab = 'tab_documents'
    #     action = 'preview'
    # elif 'generate' in request.GET:
    #     tab = 'tab_documents'
    #     action = 'generate'
        
    if request.method == "GET":
        loanform  = LoanForm(request.GET)
        assetform = AssetForm(request.GET)
        transform = TransactionsForm(request.GET)
        if is_valid(loan_no):
            try:
                loanobj = get_object_or_404(LoanMaster, loan_no=loan_no)
            except:
                loanobj = LoanMaster.objects.none()
            if loanobj:
                if action == 'get_trans':
                    try:
                        loantransactions = LoanTransactions.objects.filter(loan=loanobj)
                    except:
                        loantransactions = LoanTransactions.objects.none()
                elif action == 'get_loan':
                    try:
                        loantransactions = LoanTransactions.objects.filter(loan=loanobj)
                    except:
                        loantransactions = LoanTransactions.objects.none()
### Get Loan Master                      
                    loanform = fill_loanform(loantransactions,loanobj)
### Get Asset Details
                elif action == 'get_asset':
                    try:
                        asset = LoanAsset.objects.get(loan=loanobj)
                    except:
                        asset = LoanAsset.objects.none()
                    if asset:
                        assetform = fill_assetform(loanobj,asset)
                elif action == 'new_trans':
                    transform = TransactionsForm(initial={
                        'loan':     loanobj.loan_no,
                        })
    else:
        loanform  = LoanForm(request.POST)
        assetform = AssetForm(request.POST)
        transform = TransactionsForm(request.POST)
### Get Action
        if 'update_loan' in request.POST:
            action = 'update_loan'
        elif 'update_asset' in request.POST:
            action = 'update_asset'
        elif 'add_trans' in request.POST:
            action = 'add_trans'
            
### Save Loan            
        loan_no = request.POST.get('loan_no')
        
        if is_valid(loan_no):
            loanobj = get_object_or_404(LoanMaster, loan_no=loan_no)
### Update LoanMaster
            if action == 'update_loan': 
                customer_id = request.POST.get("customer")
                customer_obj = Customer.objects.get(customer_id=customer_id)
                if loanform.is_valid():
                    update_loan(loanobj,customer_obj,loanform,request)               
                    msg = 'Loan ' + str(loan_no) + 'Updated Successfully'
### Update Loan Asset       
        asset_no = request.POST.get('asset_no')
        if is_valid(asset_no):
            if action == 'update_asset':
                if assetform.is_valid():
                    asset = LoanAsset.objects.get(asset_no=asset_no)
                    if asset:
                        loanobj = get_object_or_404(LoanMaster, loan_no=asset.loan.loan_no)
                        update_asset(asset,loanobj,assetform,request)                     
                        msg = 'Asset ' + str(asset.asset_no) + 'Updated Successfully'
                else:
                    msg = assetform.errors

### Add Loan Transactions
        loan = request.POST.get('loan')
        if is_valid(loan):
            if action == 'add_trans':
                if transform.is_valid():
                    loanobj = get_object_or_404(LoanMaster, loan_no=loan)
                    add_transactions(loanobj, 
                                     transform.cleaned_data.get("transaction_type"), 
                                     'O', 
                                     transform.cleaned_data.get("debit_credit"), 
                                     transform.cleaned_data.get("due_date"), 
                                     transform.cleaned_data.get("total_amount"), 
                                     request)
                    msg = 'Loan Transactions Added Successfully'
                else:
                    msg = assetform.errors
                    
    context = {
        'loanform':         loanform,
        'assetform':        assetform,
        'transform':        transform,
        'segment':          'loan-manage',
        'loantransactions': loantransactions,
        'tab':              tab,
        'msg':              msg,
        'action':           action,
        }

    return render(request, 'loans/loan-manage.html', context)

@login_required(login_url="/login/")
def loansearch_view(request):

    searchform = SearchForm()
    loans      = LoanMaster.objects.none()
    queries    = {
                  'customer'    : 'customer__customer_id__icontains',
                  'full_name'   : 'customer__full_name__icontains',
                  'village'     : 'customer__perm_village__icontains',
                  'taluk'       : 'customer__perm_taluk__icontains',
                  'district'    : 'customer__perm_district__icontains',
                  'city'        : 'customer__perm_city__icontains',
                  'loan_no'     : 'loan_no__icontains',
                  'ext_loan_no' : 'ext_loan_no__icontains',
                  'branch'      : 'branch__branch',
                  'profitcentre': 'profitcentre__profit_centre',
                  'costcentre'  : 'costcentre__cost_centre',
                  'product'     : 'product__product_id',
                 }
    predicates = []
      
    if request.method == "GET":
       searchform = SearchForm(request.GET)
       if searchform.is_valid():
           for field, value in searchform.cleaned_data.items():
               if value and field in queries:
                   if field == 'product':
                       predicates.append((queries[field], value.product_id))
                   elif field == 'branch':
                       predicates.append((queries[field], value.branch))
                   elif field == 'profitcentre':
                       predicates.append((queries[field], value.profit_centre))
                   elif field == 'costcentre':
                       predicates.append((queries[field], value.cost_centre))
                   else:
                       predicates.append((queries[field], value))
           if predicates:      
               q_list = [Q(x) for x in predicates]
               loans = LoanMaster.objects.filter(reduce(operator.and_, q_list))            
               
    context = {
        'segment'   : 'loan-search',
        'searchform': searchform,
        'loans'     : loans,
        # 'msg': msg,
        }
    return render(request, 'loans/loan-search.html', context)

@login_required(login_url="/login/")
def collection_view(request):
    
    form    = CollectionForm()
    loan_no = request.GET.get("loan_no")
    msg     = None
    action  = None
    receipt = {}

         
    if request.method == "GET":
       form = CollectionForm(request.GET)

    if request.method == 'POST':
        
        form = CollectionForm(request.POST)
        if form.is_valid():
            loan_no        = form.cleaned_data.get("loan_no")
            trans_type     = form.cleaned_data.get("transaction_type")
            trans_no       = form.cleaned_data.get("transaction_no")
            total_amount   = form.cleaned_data.get("total_amount")
            paid_amount    = form.cleaned_data.get("paid_amount")
            
            
            if not paid_amount:
                msg = 'Please enter payment amount'
            else:
                if paid_amount > total_amount:
                    msg = "Payment Amount Cannot be more than than Total Amount"
            
            if not msg:
                 if loan_no:
                     loanobj = get_object_or_404(LoanMaster, loan_no=loan_no)
                     if loanobj:
                         trans = get_object_or_404(LoanTransactions, loan=loanobj, transaction_type=trans_type, transaction_no=trans_no)
                         if trans:
                                 update_trans(trans,loanobj,form,request)                     
                                 msg = 'Transactions ' + str(trans_type) + str(trans_no) + 'Receipted Successfully'
        else:
             msg = form.errors
            
    context = {
        'segment': 'collection',
        'form':     form,
        'msg':      msg,
        }

    return render(request, 'loans/loan-collection.html', context)

@login_required(login_url="/login/")
def foreclosure_view(request):
    
    form  = ClosureForm()
    
    loan_no = request.GET.get("loan_no")
    msg = None
    os_amount = decimal.Decimal('0.00')
    total_amount = decimal.Decimal('0.00')
    if request.method == 'GET':
        
       form = ClosureForm(request.GET)
       
       try:
           loanobj = get_object_or_404(LoanMaster, loan_no=loan_no)
           trans = LoanTransactions.objects.filter(Q(loan=loanobj) & ~Q(transaction_status='F'))
           for tran in trans:
               os_amount = os_amount + tran.total_amount
       except:
           loanobj = LoanMaster.objects.none()
       
       total_amount = request.GET.get("total_amount")
       if total_amount != 0.00:
           total_amount = os_amount
           
       form = ClosureForm(initial={ 'loan_no'           : request.GET.get("loan_no"),
                                    'os_amount'         : os_amount,
                                    'closure_charges'   : request.GET.get("closure_charges"),
                                    'total_amount'      : total_amount,
                                    'payment_mode'      : request.GET.get("payment_mode"),
                                    'payment_no'        : request.GET.get("payment_no"),
                                    'cheque_bank'       : request.GET.get("cheque_bank"),
                                    'payment_date'      : request.GET.get("payment_date"),
                                    'invoice_no'        : request.GET.get("invoice_no"),
                                    'invoice_reference' : request.GET.get("invoice_reference"),
                                })
    else:
         form = ClosureForm(request.POST)   
         if form.is_valid():
             loan_no            = form.cleaned_data.get("loan_no")
             total_amount       = form.cleaned_data.get("total_amount")
             closure_charges    = form.cleaned_data.get("closure_charges")
             invoice_number = None
             if loan_no:
                 loanobj = get_object_or_404(LoanMaster, loan_no=loan_no)
                 if loanobj:
                     trans = LoanTransactions.objects.filter(Q(loan=loanobj) & ~Q(transaction_status='F'))
### Update All Transactions
                     for tran in trans:
                         tran.paid_amount        = tran.total_amount
                         tran.payment_date       = form.cleaned_data.get("payment_date")
                         tran.payment_no         = form.cleaned_data.get("payment_no")
                         tran.payment_mode       = form.cleaned_data.get("payment_mode")
                         tran.cheque_bank        = form.cleaned_data.get("cheque_bank")
                         tran.invoice_reference  = form.cleaned_data.get("invoice_reference")
                         tran.changed_on         = datetime.now()
                         tran.transaction_status = 'F'
                         if invoice_number is not None:
                             tran.invoice_no = invoice_number
                             tran.save()
                         else:
                             tran.save()
                             prev_tran = get_object_or_404(LoanTransactions, transaction_id=tran.transaction_id)
                             invoice_number = prev_tran.invoice_no
### Add New Transactions for Foreclosure
                     add_transactions(loanobj, 
                                     'X', 
                                     'F', 
                                     'C', 
                                     date.today(), 
                                     closure_charges, 
                                     request)
### Close Loan
                     loanobj.loan_status    = 'C'
                     loanobj.latepayment_os = decimal.Decimal('0.00')
                     loanobj.cbc_os         = decimal.Decimal('0.00')
                     loanobj.principal_os   = decimal.Decimal('0.00')
                     loanobj.save()
                     msg = 'Loan Closed Successfully'
         else:
             msg = form.errors
             
    context = {
        'segment': 'foreclosure',
        'form':     form,
        'msg':      msg,
        'os_amount': os_amount,
        }
    return render(request, 'loans/loan-foreclosure.html', context)

def get_transaction_no(request):
    loan_no      = request.GET.get("loan_no")
    trans_type   = request.GET.get("transaction_type")
    if not trans_type:
        trans_type = 'I'
    data = []
    if loan_no:
        loanobj = get_object_or_404(LoanMaster, loan_no=loan_no)
        if loanobj:
            result = LoanTransactions.objects.filter(Q(loan=loanobj) & Q(transaction_type=trans_type)
                                                           & ~Q(transaction_status='F'))
            for res in result:
                data.append({'id':res.transaction_no, 'name':res.transaction_no})
    else:
        data.append({'id':loan_no, 'name':trans_type})
    result = { 'trans': data }
    return HttpResponse(json.dumps(result), content_type="application/json")

def get_total_amount(request):
    loan_no    = request.GET.get("loan_no")
    trans_type = request.GET.get("transaction_type")
    trans_no   = request.GET.get("transaction_no")
    net        = decimal.Decimal('0.00')
    if trans_no:
        if loan_no:
            loanobj = get_object_or_404(LoanMaster, loan_no=loan_no)
            if loanobj:
                loantrans = get_object_or_404(LoanTransactions, loan=loanobj, transaction_type=trans_type, transaction_no=trans_no)
                if loantrans:
                    total = loantrans.total_amount
                    if loantrans.paid_amount is not None:
                        paid  = loantrans.paid_amount
                    else:
                        paid = decimal.Decimal('0.00')
                    net   = total - paid
                    result = str(net)
    else:
        result = str(0.00)
    return HttpResponse(json.dumps(result), content_type="application/json")

@login_required(login_url="/login/")
def documents_view(request):
    
    loan_no   = request.GET.get("loan_no")
    doc_type  = request.GET.get("document_type")
    loantrans = LoanTransactions.objects.none()
    loanobj   = LoanMaster.objects.none()
    action    = None
    
    if 'preview' in request.GET:
        action = 'Preview'
    elif 'generate' in request.GET:
        action = 'Generate'
    
    if is_valid(loan_no):
        try:
            loanobj = get_object_or_404(LoanMaster, loan_no=loan_no)
        except:
            loanobj = LoanMaster.objects.none()
        
        if loanobj:
            loantrans = LoanTransactions.objects.filter(Q(loan=loanobj) & ~Q(transaction_status='O'))
            
    context = {
        'segment'  : 'documents',
        'loantrans': loantrans,
        'doc_type' : doc_type,
        'action'   : action,
        'loanobj'  : loanobj,
        }
    
    return render(request, 'loans/loan-documents.html', context)

@login_required(login_url="/login/")
def receipt_view(request):
    
    loan_no = 'Test'
    
    invoice = request.GET.get("invoice")
    
    if invoice:
        loantrans = LoanTransactions.objects.filter(invoice_no=invoice)
        invoice_master = loantrans[0]
        
    receipt = {
        'invoice': invoice,
        'master': invoice_master,
        'transactions': loantrans,
        'total': invoice_master.total_amount,
        }
    pdf = generate_pdf('loans/loan-receipt.html', receipt)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        content = "inline; filename=%s.pdf" % invoice
        response['Content-Disposition'] = content
        return response

@login_required(login_url="/login/")
def welcome_view(request):
    
    loanobj = LoanMaster.objects.none()
    inst_amount = decimal.Decimal('0.00')
    today = date.today()
    
    loan_no = request.GET.get("loan")
    
    if loan_no:
        loanobj = get_object_or_404(LoanMaster, loan_no=loan_no)
        if loanobj:
            loantrans   = LoanTransactions.objects.filter(Q(loan=loanobj) & Q(transaction_type='I')).first()
            inst_amount = loantrans.total_amount
    welcome = {
        'loanobj'     : loanobj,
        'loan'        : loan_no,
        'inst_amount' : inst_amount,
        'today'       : today,
        }
    
    pdf = generate_pdf('loans/loan-welcome.html', welcome)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        content = "inline; filename=%s.pdf" % loan_no
        response['Content-Disposition'] = content
        return response

@login_required(login_url="/login/")
def repayment_view(request):
    
    locale.setlocale(locale.LC_MONETARY, 'en_IN')
    loanobj = LoanMaster.objects.none()
    asset = LoanAsset.objects.none()
    inst_amount = decimal.Decimal('0.00')
    
    loan_no = request.GET.get("loan")
    today = date.today()
    repayment = []
    
    if loan_no:
        loanobj = get_object_or_404(LoanMaster, loan_no=loan_no)
        if loanobj:
            loantrans   = LoanTransactions.objects.filter(Q(loan=loanobj) & Q(transaction_type='I')).first()
            asset       = LoanAsset.objects.filter(Q(loan=loanobj)).first()
            inst_amount = loantrans
## Calculate Total Interest
        annual_interest = decimal.Decimal(float(loanobj.interest_rate))
        total_inst      = decimal.Decimal(float(loanobj.total_instalments))
        principal       = decimal.Decimal(float(loanobj.amount_finance))
        
        freq_rate = ( annual_interest / total_inst / 100 ) * ( total_inst / 12 )
        rate = (1 + freq_rate) ** total_inst
        instal_amount  = ( principal * freq_rate * rate ) / (rate - 1)
        total_interest = round(( instal_amount * total_inst ) - principal,0)
        orig_amount    = round(total_interest + principal,0)
        
        # outstand_ins = alltrans.count()
### Format Currency
        loanobj.amount_finance = locale.currency(loanobj.amount_finance, symbol=False, grouping=True)
        total_interest         = locale.currency(total_interest, symbol=False, grouping=True)
        orig_amount            = locale.currency(orig_amount, symbol=False, grouping=True)
        
### Get Repayment Schedule
        repayment = repayment_schedule(loan_no)
        
    repay = {
        'loanobj'     : loanobj,
        'asset'       : asset,
        'today'       : today,
        'interest'    : total_interest,
        'total'       : orig_amount,
        'repayment'   : repayment,
        }
    
    pdf = generate_pdf('loans/loan-repayment.html', repay)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        content = "inline; filename=%s_Repayment.pdf" % loan_no
        response['Content-Disposition'] = content
        return response
    
@login_required(login_url="/login/")
def soa_view(request):
    
    locale.setlocale(locale.LC_MONETARY, 'en_IN')
    loanobj     = LoanMaster.objects.none()
    asset       = LoanAsset.objects.none()
    inst_amount = decimal.Decimal('0.00')
    total       = decimal.Decimal('0.00')
    
    loan_no = request.GET.get("loan")
    today = date.today()
    # today = today.strftime('%d/%m/%Y')
    
    if loan_no:
        loanobj = get_object_or_404(LoanMaster, loan_no=loan_no)
        if loanobj:
            # loantrans   = LoanTransactions.objects.filter(Q(loan=loanobj))
            asset       = LoanAsset.objects.filter(Q(loan=loanobj)).first()
            # inst_amount = loantrans
### Calculate Total Interest
        annual_interest = decimal.Decimal(float(loanobj.interest_rate))
        total_inst      = decimal.Decimal(float(loanobj.total_instalments))
        principal       = decimal.Decimal(float(loanobj.amount_finance))
        
        freq_rate = ( annual_interest / total_inst / 100 ) * ( total_inst / 12 )
        rate = (1 + freq_rate) ** total_inst
        instal_amount  = ( principal * freq_rate * rate ) / (rate - 1)
        total_interest = round(( instal_amount * total_inst ) - principal,0)
        orig_amount    = round(total_interest + principal,0)
        
        principal_os, paid_instal, unpaid_instal, charges_os, overdue_instal, paidtrans, total = trans_summary(loan_no)
        if total >= 0:
            total_type = 'DR'
        else:
            total_type = 'CR'
            
### Format Currency
        loanobj.amount_finance = locale.currency(loanobj.amount_finance, symbol=False, grouping=True)
        total_interest         = locale.currency(total_interest, symbol=False, grouping=True)
        orig_amount            = locale.currency(orig_amount, symbol=False, grouping=True)
        charges_os             = locale.currency(charges_os, symbol=False, grouping=True)
        principal_os           = locale.currency(principal_os, symbol=False, grouping=True)
        total                  = locale.currency(total, symbol=False, grouping=True)
        
        for ptrans in paidtrans:
            ptrans.total_amount = locale.currency(ptrans.total_amount, symbol=False, grouping=True)
            
    soa = {
        'loanobj'        : loanobj,
        'asset'          : asset,
        'today'          : today,
        'interest'       : total_interest,
        'total'          : orig_amount,
        'principal_os'   : principal_os,
        'paid_instal'    : paid_instal,
        'unpaid_instal'  : unpaid_instal,
        'charges_os'     : charges_os,
        'overdue_instal' : overdue_instal,
        'paidtrans'      : paidtrans,
        'total_paid'     : total,
        'total_type'     : total_type
        }
    
    pdf = generate_pdf('loans/loan-soa.html', soa)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        content = "inline; filename=%s_SOA.pdf" % loan_no
        response['Content-Disposition'] = content
        return response

@login_required(login_url="/login/")
def reports_view(request):
    
    searchform = SearchForm()
    loantrans  = LoanTransactions.objects.none()
    queries    = {
                  'branch'      : 'loan__branch__branch',
                  'profitcentre': 'loan__profitcentre__profit_centre',
                  'costcentre'  : 'loan__costcentre__cost_centre',
                  'product'     : 'loan__product__product_id',
                  'start_date'  : 'payment_date__gte',
                  'end_date'    : 'payment_date__lte',
                 }
    predicates = []
      
    if request.method == "GET":
       searchform = SearchForm(request.GET)
       if searchform.is_valid():
           for field, value in searchform.cleaned_data.items():
               if value and field in queries:
                   if field == 'product':
                       predicates.append((queries[field], value.product_id))
                   elif field == 'branch':
                       predicates.append((queries[field], value.branch))
                   elif field == 'profitcentre':
                       predicates.append((queries[field], value.profit_centre))
                   elif field == 'costcentre':
                       predicates.append((queries[field], value.cost_centre))
                   else:
                       predicates.append((queries[field], value))
           if predicates:       
               q_list = [Q(x) for x in predicates]
               loantrans = LoanTransactions.objects.filter(reduce(operator.and_, q_list))  
        
    context = {
        'segment'    : 'rptcol',
        'searchform' : searchform,
        'loantrans'  : loantrans,
        }
    
    return render(request, 'loans/reports-collections.html', context)

@login_required(login_url="/login/")
def overdue_view(request):
    
    searchform = SearchForm()
    loantrans  = LoanTransactions.objects.none()
    queries    = {
                  'branch'      : 'loan__branch__branch',
                  'profitcentre': 'loan__profitcentre__profit_centre',
                  'costcentre'  : 'loan__costcentre__cost_centre',
                  'product'     : 'loan__product__product_id',
                  'start_date'  : 'due_date__lt',
                 }
    predicates = []
    if request.method == "GET":
       searchform = SearchForm(request.GET)
       if searchform.is_valid():
           for field, value in searchform.cleaned_data.items():
               if value and field in queries:
                   if field == 'product':
                       predicates.append((queries[field], value.product_id))
                   elif field == 'branch':
                       predicates.append((queries[field], value.branch))
                   elif field == 'profitcentre':
                       predicates.append((queries[field], value.profit_centre))
                   elif field == 'costcentre':
                       predicates.append((queries[field], value.cost_centre))
                   else:
                       predicates.append((queries[field], value))
           if predicates:  
               q_list = [Q(x) for x in predicates]
               q_list.append(~Q(('transaction_status', 'F')))
               loantrans = LoanTransactions.objects.filter(reduce(operator.and_, q_list))  
    
    
    context = {
        'segment'    : 'rptover',
        'searchform' : searchform,
        'loantrans'  : loantrans,
        }
    
    return render(request, 'loans/reports-overdue.html', context)

@login_required(login_url="/login/")
def forecast_view(request):
    
    searchform = SearchForm()
    loantrans  = LoanTransactions.objects.none()
    queries    = {
                  'branch'      : 'loan__branch__branch',
                  'profitcentre': 'loan__profitcentre__profit_centre',
                  'costcentre'  : 'loan__costcentre__cost_centre',
                  'product'     : 'loan__product__product_id',
                  'start_date'  : 'due_date__gte',
                  'end_date'    : 'due_date__lte',
                 }
    predicates = []
    if request.method == "GET":
       searchform = SearchForm(request.GET)
       if searchform.is_valid():
           for field, value in searchform.cleaned_data.items():
               if value and field in queries:
                   if field == 'product':
                       predicates.append((queries[field], value.product_id))
                   elif field == 'branch':
                       predicates.append((queries[field], value.branch))
                   elif field == 'profitcentre':
                       predicates.append((queries[field], value.profit_centre))
                   elif field == 'costcentre':
                       predicates.append((queries[field], value.cost_centre))
                   else:
                       predicates.append((queries[field], value))
           if predicates:  
               q_list = [Q(x) for x in predicates]
               q_list.append(~Q(('transaction_status', 'F')))
               loantrans = LoanTransactions.objects.filter(reduce(operator.and_, q_list))  
    
    
    context = {
        'segment'    : 'rptfore',
        'searchform' : searchform,
        'loantrans'  : loantrans,
        }
    
    return render(request, 'loans/reports-forecast.html', context)