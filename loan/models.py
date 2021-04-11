from django.db import models

# Create your models here.

from django.utils.translation import ugettext as _
from masterdata.models import Client, ProfitCentre, Branch, CostCentre, Product, Currency
from customer.models import Customer
from datetime import date
import datetime
# import string
from django.core.validators import MinValueValidator, MaxValueValidator

class LoanMaster(models.Model):
    client              = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    loan_no             = models.CharField(primary_key=True, max_length=12, null=False, 
                                           blank=False, editable=False, auto_created=True)
    ext_loan_no         = models.CharField(max_length=30, null=True, blank=True )
    customer            = models.ForeignKey(Customer, on_delete=models.SET_NULL, 
                                            null=True)
    branch              = models.ForeignKey(Branch, on_delete=models.SET_NULL, 
                                            null=True)
    profitcentre        = models.ForeignKey(ProfitCentre, on_delete=models.SET_NULL, 
                                            null=True)
    costcentre          = models.ForeignKey(CostCentre, on_delete=models.SET_NULL, 
                                            null=True)
    product             = models.ForeignKey(Product, on_delete=models.SET_NULL, 
                                            null=True)
    currency            = models.ForeignKey(Currency, on_delete=models.SET_NULL, 
                                            null=True)    
    application_no      = models.CharField(max_length=30, null=True, blank=True )
    application_date    = models.DateField(default=date.today, null=True, blank=True)
    amount_finance      = models.DecimalField(max_digits=15, decimal_places=2, 
                                              null=True, blank=True)
    service_charges     = models.DecimalField(max_digits=15, decimal_places=2, 
                                              null=True, blank=True)
    gst_charges         = models.DecimalField(max_digits=15, decimal_places=2, 
                                              null=True, blank=True)
    vat_charges         = models.DecimalField(max_digits=15, decimal_places=2, 
                                              null=True, blank=True)
    cess_charges        = models.DecimalField(max_digits=15, decimal_places=2, 
                                              null=True, blank=True)
    other_charges       = models.DecimalField(max_digits=15, decimal_places=2, 
                                              null=True, blank=True)
    amount_disburse     = models.DecimalField(max_digits=15, decimal_places=2, 
                                              null=True, blank=True)
    principal_os        = models.DecimalField(max_digits=15, decimal_places=2, 
                                              null=True, blank=True)
    latepayment_os      = models.DecimalField(max_digits=15, decimal_places=2, 
                                              null=True, blank=True)
    cbc_os              = models.DecimalField(max_digits=15, decimal_places=2, 
                                              null=True, blank=True)
    amount_first_instal = models.DecimalField(max_digits=15, decimal_places=2, 
                                              null=True, blank=True)
    disbursal_date      = models.DateField(default=date.today, null=True, blank=True)
    interest_rate       = models.DecimalField(max_digits=5, decimal_places=2, 
                                              null=False, blank=False)
    interest_start      = models.DateField(default=date.today, null=True, blank=True)
    due_date            = models.IntegerField(null=True, blank=True,
                                              validators=[MinValueValidator(1),
                                                          MaxValueValidator(31)])
    instalment_start    = models.DateField(default=date.today, null=True, blank=True)
    instalment_end      = models.DateField(default=date.today, null=True, blank=True)
    
    PAYMENT_LIST = (
        ('B', 'Bank Account Transfer'),  
        ('C', 'CHEQUE'),   
        ('D', 'Digital Payment'),
        ('E', 'ECS'),
        ('N', 'NACH'),
        ('S', 'CASH'),        
        )
    
    first_payment       = models.CharField(max_length=1, choices=PAYMENT_LIST, 
                                           blank=False, default='S' )
    payment_mode        = models.CharField(max_length=1, choices=PAYMENT_LIST, 
                                           blank=False, default='N' )
    
    INSTAL_LIST = (
        ('W', 'Weekly'),
        ('B', 'Bi-Weekly'),
        ('M', 'Monthly'),
        ('Q', 'Quarterly'),
        )
    
    instalment_type     = models.CharField(max_length=1, choices=INSTAL_LIST, 
                                           blank=False, default='W' )
    total_instalments   = models.IntegerField(null=True, blank=True)
    advance_instalments = models.IntegerField(null=True, blank=True)
    paid_instalments    = models.IntegerField(null=True, blank=True)
    overdue_instalments = models.IntegerField(null=True, blank=True)
    
    bank_name           = models.CharField(max_length=40, null=True, blank=True )
    bank_branch         = models.CharField(max_length=40, null=True, blank=True )
    bank_ifsc           = models.CharField(max_length=20, null=True, blank=True )
    bank_account        = models.CharField(max_length=30, null=True, blank=True )
    
    STATUS_LIST = (
        ('A', 'Active'),
        ('I', 'Inactive'),
        ('C', 'Closed'),
        )
    
    loan_status         = models.CharField(max_length=1, choices=STATUS_LIST, 
                                           blank=True, default='A' )
    
    DISB_STATUS_LIST = (
        ('N', 'Not Disbursed'),
        ('P', 'Partially Disbursed'),
        ('F', 'Fully Disbursed'),
        )
    
    disbursal_status    = models.CharField(max_length=1, choices=DISB_STATUS_LIST, 
                                           blank=True, default='F' )
    
    created_on          = models.DateTimeField(verbose_name=_("Created On"), 
                                               auto_now=False)
    created_by          = models.CharField(max_length=20, blank=True, default='' )
    changed_on          = models.DateTimeField(verbose_name=_("Changed On"), 
                                               auto_now_add=True)
    changed_by          = models.CharField(max_length=20, blank=True, default='' ) 
    
    class Meta:
        ordering = ['client_id', 'loan_no']    
    
    def __str__(self):
        return self.loan_no
    
    def save(self):
        if not self.loan_no:
            last_loan = LoanMaster.objects.filter(product=self.product).order_by('loan_no').last()
            if last_loan:
                loan_no = int(''.join(i for i in last_loan.loan_no if i.isdigit()))
                loan_no = loan_no + 1
                zero_filled_loan = str(loan_no).zfill(9)
                self.loan_no = self.product.loan_no_prefix + str(zero_filled_loan)
            else:
                self.loan_no = self.product.loan_no_prefix + '000000001'
        
        super(LoanMaster,self).save()
        return self.loan_no
            
    def update(self):
        super(LoanMaster,self).save()
        
class LoanAsset(models.Model):
    client             = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    loan               = models.ForeignKey(LoanMaster, on_delete=models.SET_NULL, 
                                           null=True)
    asset_no           = models.CharField(primary_key=True, max_length=15, null=False, 
                                          blank=False,)
    asset_desc         = models.CharField(max_length=80, null=True, blank=True )
    quantity           = models.IntegerField(null=True, blank=True, default=1)
    invoice_no         = models.CharField(max_length=40, null=True, blank=True )
    invoice_date       = models.DateField(default=date.today, null=True, blank=True)
    make               = models.CharField(max_length=80, null=True, blank=True )
    model              = models.CharField(max_length=80, null=True, blank=True )
    chasis_no          = models.CharField(max_length=80, null=True, blank=True )
    engine_no          = models.CharField(max_length=30, null=True, blank=True )
    color              = models.CharField(max_length=30, null=True, blank=True )
    year               = models.IntegerField(null=True, blank=True)
    registration_no    = models.CharField(max_length=30, null=True, blank=True )
    rto                = models.CharField(max_length=30, null=True, blank=True )
    supplier           = models.CharField(max_length=80, null=True, blank=True )
    category           = models.CharField(max_length=30, null=True, blank=True )
    reposession_date   = models.DateField(default=date.today, null=True, blank=True)
    sales_date         = models.DateField(default=date.today, null=True, blank=True)
    imei1              = models.CharField(max_length=30, null=True, blank=True )
    imei2              = models.CharField(max_length=30, null=True, blank=True )
    invoice_remark     = models.CharField(max_length=80, null=True, blank=True )
    asset_cost         = models.DecimalField(max_digits=15, decimal_places=2, 
                                             null=True, blank=True)
    blue_book_value    = models.DecimalField(max_digits=15, decimal_places=2, 
                                             null=True, blank=True)
    value              = models.DecimalField(max_digits=15, decimal_places=2, 
                                             null=True, blank=True)
    sales_value        = models.DecimalField(max_digits=15, decimal_places=2, 
                                             null=True, blank=True)    
    rbi_code           = models.CharField(max_length=30, null=True, blank=True )
    
    DELIVERY_ORDER_LIST = (
        ('Y', 'Yes'),
        ('N', 'No'),
        )
    
    delivery_order     = models.CharField(max_length=1, choices=DELIVERY_ORDER_LIST, 
                                        blank=True, default='Y' )
    do_date            = models.DateField(default=date.today, null=True, blank=True)
    first_inspect_date = models.DateField(default=date.today, null=True, blank=True)
    regd_remark        = models.CharField(max_length=80, null=True, blank=True )
    rc_status          = models.CharField(max_length=20, null=True, blank=True )
    rcsu_date          = models.DateField(default=date.today, null=True, blank=True)
    created_on         = models.DateTimeField(verbose_name=_("Created On"), auto_now=False)
    created_by         = models.CharField(max_length=20, blank=True, default='' )
    changed_on         = models.DateTimeField(verbose_name=_("Changed On"), auto_now_add=True)
    changed_by         = models.CharField(max_length=20, blank=True, default='' ) 
    
    class Meta:
        ordering = ['client_id', 'loan', 'asset_no']    
    
    def __str__(self):
        return f'{self.loan}, {self.asset_no}'
    
    def update(self):
        super(LoanAsset,self).save()
    
    def save(self):
        super(LoanAsset,self).save()
    
    
class LoanTransactions(models.Model):
    client            = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    transaction_id    = models.CharField(primary_key=True, max_length=20,  
                                            blank=False, editable=False, 
                                            null=False, auto_created=True)
    loan              = models.ForeignKey(LoanMaster, on_delete=models.SET_NULL, 
                                           null=True)
    transaction_no    = models.IntegerField(null=False, blank=False, 
                                            editable=False, auto_created=True)
                                            
    TRANSACTION_TYPE_LIST = (
        ('I', 'Instalment Payment'),
        ('D', 'Disbursal'),
        ('F', 'First Payment'),
        ('C', 'CBC Charges'),
        ('L', 'LP Charges'),
        ('O', 'Overdue Charges'),
        ('P', 'Part Payment'),
        ('X', 'Fore Closure'),
        ('M', 'Other Payments'),
        ('S', 'Service Charges'),
        ('G', 'GST Charges'),
        ('V', 'VAT Charges'),
        ('E', 'CESS Charges'),
        ('T', 'Other Charges'),
        )
    
    transaction_type   = models.CharField(max_length=1, choices=TRANSACTION_TYPE_LIST, 
                                         blank=True, default='I' ) 
    STATUS_LIST = (
        ('O', 'Not Paid'),
        ('F', 'Fully Paid'),
        ('P', 'Partially Paid'),
        )
    transaction_status = models.CharField(max_length=1, choices=STATUS_LIST, 
                                         blank=True, default='O' )

    posting_date      = models.DateField(default=date.today, null=False, blank=False)
    due_date          = models.DateField(default=date.today, null=False, blank=False)
    
    PAYMENT_LIST = (
        ('B', 'Bank A/c Trans.'),  
        ('C', 'CHEQUE'),   
        ('D', 'Digital Payment'),
        ('E', 'ECS'),
        ('N', 'NACH'),
        ('S', 'Cash'),        
        )
    
    payment_mode      = models.CharField(max_length=1, choices=PAYMENT_LIST, 
                                           blank=True, null=True, default='N' )
    payment_no        = models.CharField(max_length=20, null=True, blank=True, default='' )
    payment_date      = models.DateField(null=True, blank=True)
    cheque_bank       = models.CharField(max_length=40, null=True, blank=True, default='' )
    
    DEBIT_LIST = (
        ('D', 'DR'),  
        ('C', 'CR'),          
        )
    
    debit_credit      = models.CharField(max_length=1, choices=DEBIT_LIST, 
                                           blank=False, default='D' )
    total_amount      = models.DecimalField(max_digits=15, decimal_places=2, 
                                             null=True, blank=True)
    paid_amount       = models.DecimalField(max_digits=15, decimal_places=2, 
                                             null=True, blank=True, default='0.00')
    invoice_no        = models.CharField(max_length=20, null=True, blank=True,
                                         auto_created=True)
    invoice_reference = models.CharField(max_length=40, null=True, blank=True )
    created_on        = models.DateTimeField(verbose_name=_("Created On"), auto_now=False)
    created_by        = models.CharField(max_length=20, blank=True, default='' )
    changed_on        = models.DateTimeField(verbose_name=_("Changed On"), auto_now_add=True)
    changed_by        = models.CharField(max_length=20, blank=True, default='' ) 
    
    class Meta:
        ordering = ['client_id', 'loan', 'transaction_no']
        
    def __str__(self):
        return f'{self.loan}, {self.get_transaction_type_display()}, {self.transaction_no}'
    
    def save(self):   
## Generate Transaction No      
        if not self.transaction_no:
            last_trans = LoanTransactions.objects.filter(loan=self.loan,transaction_type=self.transaction_type).order_by('transaction_no').last()
            if last_trans:
                self.transaction_no = last_trans.transaction_no + 1
            else:
                self.transaction_no = 1
## Generate Transaction ID                
        if not self.transaction_id:
            self.transaction_id = self.loan.loan_no + self.transaction_type + str(self.transaction_no)
## Update Invoice Number            
        if ((self.transaction_status == 'F') or (self.transaction_status == 'P')):
            if not self.invoice_no:
                last_inv = LoanTransactions.objects.filter(payment_date=self.payment_date).order_by('invoice_no').last()
                curr_date = str(datetime.datetime.today().strftime('%d%m%y'))
                branch = self.loan.branch.branch[-4:]
                if last_inv:
                    if last_inv.invoice_no:
                        inv_list = last_inv.invoice_no.split("/")
                        last_no = int(inv_list[-1])
                        last_no+=1
                    else:
                       last_no = 1 
                else:
                    last_no = 1
            
                length = len(str(last_no))
                zeros = 6 - length
                zero_filled_inv = str(last_no).zfill(zeros)
                
                self.invoice_no = branch + '/' + curr_date + self.transaction_type + '/' + zero_filled_inv           
        else:
            self.payment_mode = ''
        self.invoice_reference = self.get_transaction_type_display() 
        super(LoanTransactions,self).save()
        # return self.transaction_no, self.invoice_no
            
    def update(self):
        super(LoanTransactions,self).save()
    
    
    
    
    
    
    
    
    
    
    