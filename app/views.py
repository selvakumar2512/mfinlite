# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
# from django.db.models import Q
from loan.models import LoanTransactions, LoanMaster 
import datetime 
import decimal
import calendar
from django.db.models import Q, Sum, F, DecimalField, Func, Count, Case, When
# from django.db.models import F
from django.db.models import FloatField
from django.db.models.functions import Cast
# from django.db.models import Func
# Func = ''

# class SumDecimal(Func):
#     function = 'SUM'
#     name = 'sum'
#     contains_aggregate = True
#     output_field = DecimalField()
#     template = '%(function)s(%(expressions)s)'

#     def __init__(self, *args, **kwargs):
#         self.decimal_places = kwargs.pop('decimal_places', None)
#         super(SumDecimal, self).__init__(*args, **kwargs)

#     def as_sql(self, compiler, connection, function=None, template=None):
#         sql = super(SumDecimal, self).as_sql(
#             compiler=compiler,
#             connection=connection,
#             function=function,
#             template=template)

#         if self.decimal_places:
#             sql, params = sql
#             sql = 'CAST(%s AS DECIMAL(16, %d))' % (sql, self.decimal_places)
#             return sql, params

#         return sql
    
@login_required(login_url="/login/")
def index(request):
    context = {}
    
    this_month = datetime.datetime.now().month
    td         = datetime.date.today()
    first_day  = td.replace(day=1)
    last_day   = datetime.date(td.year, td.month, calendar.monthrange(td.year, td.month)[-1])
    # context['segment'] = 'index'
    
    summary = []
    fin_amount = decimal.Decimal('0.00')
    rev_amount = decimal.Decimal('0.00')
    ovr_amount = decimal.Decimal('0.00')
    out_amount = decimal.Decimal('0.00')
    chg_amount = decimal.Decimal('0.00')
    col_amount = decimal.Decimal('0.00')
    amount     = decimal.Decimal('0.00')
#### Number Of Loans Issued    
    no_of_loans = LoanMaster.objects.filter(Q(created_on__month=this_month)).count()
#### Total Active Loans
    total_loans =  LoanMaster.objects.filter(Q(loan_status='A')).count()
#### Amount Disbursed    
    loans = LoanMaster.objects.filter(Q(created_on__month=this_month) &
                                            ( Q(disbursal_status='F') | Q(disbursal_status='P') ) &
                                            Q(loan_status='A'))
    for loan in loans:
        fin_amount = fin_amount + loan.amount_finance
#### Revenue
    trans = LoanTransactions.objects.filter(Q(debit_credit='C') & 
                                            ~Q(transaction_status='O') &
                                            Q(payment_date__month=this_month))
    for tran in trans:
        if tran.transaction_status=='F':
            rev_amount = rev_amount + tran.total_amount
        else:
            if tran.paid_amount is not None:
                rev_amount = rev_amount + tran.paid_amount
#### Overdue
    # pending = LoanTransactions.objects.filter(~Q(transaction_status='F') &
    #                                           ~Q(transaction_type='D') &
    #                                           Q(due_date__lt=datetime.date.today()))
    # for pen in pending:
    #     if pen.transaction_status=='P':
    #         if pen.paid_amount is not None:
    #             ovr_amount = ovr_amount + pen.paid_amount
    #         else:
    #             ovr_amount = ovr_amount + pen.total_amount
    #     else:
    #         ovr_amount = ovr_amount + pen.total_amount
    pending = LoanTransactions.objects.filter(~Q(transaction_status='F') &
                                              ~Q(transaction_type='D') )
    for pen in pending:
## Get the amount based on the status
        if pen.transaction_status=='P':
            if pen.paid_amount is not None:
                amount = pen.total_amount - pen.paid_amount
            else:
                amount = pen.total_amount
        else:
            amount = pen.total_amount
## Overdue Amount        
        if pen.due_date < datetime.date.today():
            ovr_amount = ovr_amount + amount
## Collection This Month
        if first_day <= pen.due_date <= last_day:
            col_amount = col_amount + amount
## Outstanding Principal
        if pen.transaction_type == 'I':
            out_amount = out_amount + amount
        else:
            chg_amount = chg_amount + amount
            
### Overdue Loans
    # outloans = LoanTransactions.objects.filter(~Q(transaction_status='F') &
    #                                           ~Q(transaction_type='D') &
    #                                           Q(due_date__lt=datetime.date.today())).values(
    #                                               loan_no=F('loan__loan_no'), 
    #                                               name=F('loan__customer__full_name'),
    #                                               product=F('loan__product__product_name')).order_by(
    #                                                   'loan__loan_no', 
    #                                               'loan__customer__full_name',
    #                                               'loan__product').annotate(
    #                                               total=Sum('total_amount'))
### Outstanding Principal Per Product
    oploans = LoanTransactions.objects.filter(~Q(transaction_status='F') &
                                              ~Q(transaction_type='D') ).values(
                                                    branch=F('loan__branch__branch_name'),
                                                    product=F('loan__product__product_name')).order_by(
                                                        'loan__branch__branch_name',
                                                        'loan__product__product_name' ).annotate(
                                                  # total=Sum(Case(When(transaction_type='I', then=F('total_amount')), default=0)),
                                                  # charges=Sum(Case(When(~Q(transaction_type='I'), then=F('total_amount')), default=0)),
                                                  # overdue=Sum(Case(When(due_date__lt=datetime.date.today(), then=F('total_amount')), default=0)),
                                                  loans=Count(Case(When(Q(loan__loan_status='A'), then=F('loan__loan_no')), default=0), distinct=True),
                                                  prin_not_due=Sum(Case(When(Q(transaction_type='I') & Q(due_date__gte=datetime.date.today()),
                                                      then=F('total_amount')), default=0)),
                                                  chrg_not_due=Sum(Case(When(~Q(transaction_type='I') & Q(due_date__gte=datetime.date.today()),
                                                      then=F('total_amount')), default=0)),
                                                  prin_due=Sum(Case(When(Q(transaction_type='I') & Q(due_date__lt=datetime.date.today()),
                                                      then=F('total_amount')), default=0)),
                                                  chrg_due=Sum(Case(When(~Q(transaction_type='I') & Q(due_date__lt=datetime.date.today()),
                                                      then=F('total_amount')), default=0))
                                                  )

    context = {
        'segment'    : 'index',
        'month'      : this_month,
        'loans'      : no_of_loans,
        'total_loans': total_loans,
        'disbursed'  : fin_amount,
        'revenue'    : rev_amount,
        'out_amount' : out_amount,
        'chg_amount' : chg_amount,
        'col_amount' : col_amount,
        'overdue'    : ovr_amount,
        # 'outloans'   : outloans,
        'oploans'    : oploans
        }
    
    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        if request.path == 'customer:customers_main':
            return render(request,'customer:customers_main', context)
        elif request.path == 'customer:customers_manage':
            context['segment'] = 'customer-manage'
            return render(request,'customer:customers_manage', context)
        else:
            load_template      = request.path.split('/')[-1]
            context['segment'] = load_template

            html_template = loader.get_template( load_template )
            return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))
