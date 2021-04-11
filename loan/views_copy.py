from django.shortcuts import render

# Create your views here.

from django.contrib.auth.decorators import login_required
from .forms import LoanForm, AssetForm, TransactionsForm, SearchForm
from .models import LoanMaster, LoanAsset, LoanTransactions
from customer.models import Customer
from django.db.models import Q
from django.shortcuts import get_object_or_404
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import decimal
from .loanmodule import *

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
                instal_amount = round(instal_amount,0)

                ins_start = loanform.cleaned_data.get("instalment_start")
                ins_end   = loanform.cleaned_data.get("instalment_end")
                    
                due_date  = ins_start

                while due_date <= ins_end:
## Save Loan Transactions
                    add_transactions(loanobj, 
                                     'I', 
                                     'O', 
                                     'C', 
                                     due_date, 
                                     instal_amount, 
                                     request)
## Generate Due Date
                    due_date+=add_days                     
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
    elif 'preview' in request.GET:
        tab = 'tab_documents'
        action = 'preview'
    elif 'generate' in request.GET:
        tab = 'tab_documents'
        action = 'generate'
        
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
### Calculate Paid, Overdue and Advance Instalments
                    overdue = loantransactions.filter(Q(due_date__lt=datetime.today()) & ~Q(transaction_status='F')).count()
                    paid    = loantransactions.filter(Q(transaction_status='F')).count()
                    advance = loantransactions.filter(Q(due_date__gt=datetime.today()) & Q(transaction_status='F')).count()
## Initialize Loan Masster
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
### Get Asset Details
                elif action == 'get_asset':
                    try:
                        asset = LoanAsset.objects.get(loan=loanobj)
                    except:
                        asset = LoanAsset.objects.none()
                    if asset:
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
### Show Transactions Form
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
    
    loans = LoanMaster.objects.none()
    searchform = SearchForm()
    
    customer     = request.GET.get("customer")
    full_name    = request.GET.get("full_name")
    village      = request.GET.get("village")
    taluk        = request.GET.get("taluk")
    district     = request.GET.get("district")
    city         = request.GET.get("city")
    loan_no      = request.GET.get("loan_no")
    ext_loan_no  = request.GET.get("ext_loan_no")
    branch       = request.GET.get("branch")
    profitcentre = request.GET.get("profitcentre")
    costcentre   = request.GET.get("costcentre")
    product      = request.GET.get("product")
    
    msg = customer
    
    if request.method == "GET":
       searchform = SearchForm(request.GET)
    
    if ( is_valid(customer)    | is_valid(full_name)    |
         is_valid(village)     | is_valid(taluk)        |
         is_valid(district)    | is_valid(city)         |
         is_valid(loan_no)     | is_valid(ext_loan_no)  |
         is_valid(branch)      | is_valid(profitcentre) |
         is_valid(costcentre)  | is_valid(product) ):
        loans = LoanMaster.objects.all()
    
    if is_valid(customer):
        loans = loans.filter(Q(customer__customer_id__icontains=customer)).distinct()
    
    if is_valid(full_name):
        loans = loans.filter(Q(customer__full_name__icontains=full_name)).distinct()
    
    if is_valid(village):
        loans = loans.filter(Q(customer__perm_village__icontains=village) | Q(customer__cont_village__icontains=village)).distinct()
    
    if is_valid(city):
        loans = loans.filter(Q(customer__perm_city__icontains=city) | Q(customer__cont_city__icontains=city)).distinct()
    
    if is_valid(taluk):
        loans = loans.filter(Q(customer__perm_taluk__icontains=taluk) | Q(customer__cont_taluk__icontains=taluk)).distinct()
    
    if is_valid(district):
        loans = loans.filter(Q(customer__perm_district__icontains=district) | Q(customer__cont_district__icontains=district)).distinct()
    
    if is_valid(loan_no):
        loans = loans.filter(Q(loan_no__icontains=loan_no)).distinct()
    
    if is_valid(ext_loan_no):
        loans = loans.filter(Q(ext_loan_no__icontains=ext_loan_no)).distinct()
    
    if is_valid(branch):
        loans = loans.filter(Q(branch__branch__icontains=branch)).distinct()

    if is_valid(profitcentre):
        loans = loans.filter(Q(profitcentre__profit_centre__icontains=profitcentre)).distinct()
        
    if is_valid(costcentre):
        loans = loans.filter(Q(costcentre__cost_centre__icontains=costcentre)).distinct()
        
    if is_valid(product):
        loans = loans.filter(Q(product__product_id__icontains=product)).distinct()
        
    context = {
        'segment': 'loan-search',
        'searchform': searchform,
        'loans': loans,
        'msg': msg,
        }
    return render(request, 'loans/loan-search.html', context)