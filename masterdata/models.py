from django.db import models
from datetime import date
from django.utils.timezone import now

# Create your models here.

## Client Number Must be set for each Organization ##
class Client(models.Model):
    client_id = models.CharField(primary_key=True, max_length=6, null=False, blank=False )
    client_name = models.CharField(max_length=60, null=False, blank=False,  )
    
    def __str__(self):
        """String for representing the Model object."""
        return self.client_name
    
## Chart of Account must be unique for each Organiazation ##
## One Organization can have multiple COA e.g. parent and child company ##    
class ChartOfAccounts(models.Model):
    client_id = models.ForeignKey('Client', on_delete=models.SET_NULL, null=True)
    coa_id = models.CharField(primary_key=True, max_length=6, null=False, blank=False )
    coa_name = models.CharField(max_length=60, null=False, blank=False)
    
    class Meta:
        ordering = ['client_id', 'coa_id']
        
    def __str__(self):
        return f'{self.coa_id}, {self.coa_id}'

## Accounting Year Defines the accounting period ##
class AccountingYear(models.Model):
    client_id = models.ForeignKey('Client', on_delete=models.SET_NULL, null=True)
    accounting_year = models.CharField(primary_key=True, max_length=6, null=False, blank=False )
    acc_year_name = models.CharField(max_length=60, null=False, blank=False)
    
    class Meta:
        ordering = ['client_id', 'accounting_year']
        
    def __str__(self):
        return f'{self.accounting_year}, {self.acc_year_name}'   

## Currency Master ##
class Currency(models.Model):
    client_id = models.ForeignKey('Client', on_delete=models.SET_NULL, null=True)
    currency_key = models.CharField(primary_key=True, max_length=6, null=False, blank=False )
    currency_name = models.CharField(max_length=60, null=False, blank=False)
    decimal_places = models.IntegerField()
    
    class Meta:
        ordering = ['client_id', 'currency_key']
    
    def __str__(self):
        # return f'{self.currency_key}, {self.currency_name}' 
        return self.currency_name

## Controlling Area e.g. Region across globe ##
class ControllingArea(models.Model):
    client_id = models.ForeignKey('Client', on_delete=models.SET_NULL, null=True)
    controlling_area = models.CharField(primary_key=True, max_length=6, null=False, blank=False )
    ca_name = models.CharField(max_length=60, null=False, blank=False)
    currency_key = models.ForeignKey('Currency', on_delete=models.SET_NULL, null=True, blank=True)
    coa_id = models.ForeignKey('ChartOfAccounts', on_delete=models.SET_NULL, null=True)
    accounting_year = models.ForeignKey('AccountingYear', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['client_id', 'controlling_area']
    
    def __str__(self):
        # return f'{self.controlling_area}, {self.ca_name}' 
        return self.ca_name

## Compnay Code e.g. One Company Code per Balance Sheet
class CompanyCode(models.Model):
     client_id = models.ForeignKey('Client', on_delete=models.SET_NULL, null=True)
     company_code = models.CharField(primary_key=True, max_length=6, null=False, blank=False )
     company_name = models.CharField(max_length=60, null=False, blank=False)
     coa_id = models.ForeignKey('ChartOfAccounts', on_delete=models.SET_NULL, null=True)
     controlling_area = models.ForeignKey('ControllingArea', on_delete=models.SET_NULL, null=True)
     accounting_year = models.ForeignKey('AccountingYear', on_delete=models.SET_NULL, null=True)
     currency_key = models.ForeignKey('Currency', on_delete=models.SET_NULL, null=True)
     gstin = models.CharField(max_length=40, null=True, blank=True)
     unit_number = models.CharField(max_length=20, null=True, blank=True)
     building = models.CharField(max_length=80, null=True, blank=True)
     street_1 = models.CharField(max_length=80, null=True, blank=True)
     street_2 = models.CharField(max_length=80, null=True, blank=True)
     street_3 = models.CharField(max_length=80, null=True, blank=True)
     street_4 = models.CharField(max_length=80, null=True, blank=True) 
     city = models.CharField(max_length=40, null=False, blank=False)
     postal_code = models.CharField(max_length=20, null=False, blank=False)
     region = models.CharField(max_length=40, null=True, blank=True)
     country = models.CharField(max_length=40, null=True, blank=True)
     
     class Meta:
        ordering = ['client_id', 'company_code']
    
     def __str__(self):
        # return f'{self.company_code}, {self.company_name}'    
        return self.company_name

## Profit Centre e.g. One PC per responsibility
class ProfitCentre(models.Model):
    client_id = models.ForeignKey('Client', on_delete=models.SET_NULL, null=True)
    profit_centre = models.CharField(primary_key=True, max_length=6, null=False, blank=False )
    pc_name = models.CharField(max_length=60, null=False, blank=False)
    controlling_area = models.ForeignKey('ControllingArea', on_delete=models.SET_NULL, null=True)
    valid_from = models.DateField(default=date.today)
    valid_to = models.DateField()

    class Meta:
        ordering = ['client_id', 'profit_centre']
    
    def __str__(self):
        # return f'{self.profit_centre}, {self.pc_name}'  
        return self.pc_name

## Business Area e.g. Division    
class BusinessArea(models.Model):
    client_id = models.ForeignKey('Client', on_delete=models.SET_NULL, null=True)
    business_area = models.CharField(primary_key=True, max_length=12, null=False, blank=False )
    ba_name = models.CharField(max_length=60, null=False, blank=False)
    controlling_area = models.ForeignKey('ControllingArea', on_delete=models.SET_NULL, null=True)
    company_code = models.ForeignKey('CompanyCode', on_delete=models.SET_NULL, null=True)
    valid_from = models.DateField(default=date.today)
    valid_to = models.DateField()

    class Meta:
        ordering = ['client_id', 'business_area']
    
    def __str__(self):
        # return f'{self.business_area}, {self.ba_name}'  
        return self.ba_name

## Branch
class Branch(models.Model):
    client_id = models.ForeignKey('Client', on_delete=models.SET_NULL, null=True)
    branch = models.CharField(primary_key=True, max_length=12, null=False, blank=False )
    branch_name =  models.CharField(max_length=60, null=False, blank=False)
    controlling_area = models.ForeignKey('ControllingArea', on_delete=models.SET_NULL, null=True)
    company_code = models.ForeignKey('CompanyCode', on_delete=models.SET_NULL, null=True)
    business_area = models.ForeignKey('BusinessArea', on_delete=models.SET_NULL, null=True)
    valid_from = models.DateField(default=date.today)
    valid_to = models.DateField()
    
    class Meta:
        ordering = ['client_id', 'branch']
    
    def __str__(self):
        # return f'{self.branch}, {self.branch_name}' 
        return self.branch_name
    
## Cost Centre e.g. Department
class CostCentre(models.Model):
    client_id = models.ForeignKey('Client', on_delete=models.SET_NULL, null=True)
    cost_centre = models.CharField(primary_key=True, max_length=6, null=False, blank=False )
    cc_name = models.CharField(max_length=60, null=False, blank=False)
    controlling_area = models.ForeignKey('ControllingArea', on_delete=models.SET_NULL, null=True)
    company_code = models.ForeignKey('CompanyCode', on_delete=models.SET_NULL, null=True)
    valid_from = models.DateField(default=date.today)
    valid_to = models.DateField()
    # business_area = models.ForeignKey('BusinessArea', on_delete=models.SET_NULL, null=True)
    # profit_centre = models.ForeignKey('ProfitCentre', on_delete=models.SET_NULL, null=True)
    currency_key = models.ForeignKey('Currency', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['client_id', 'cost_centre']
    
    def __str__(self):
        # return f'{self.cost_centre}, {self.cc_name}'  
        return self.cc_name

## Bank Master
class BankMaster(models.Model):
    client_id = models.ForeignKey('Client', on_delete=models.SET_NULL, null=True)
    bank_id = models.CharField(primary_key=True, max_length=12, null=False, blank=False )
    bank_name = models.CharField(max_length=60, null=False, blank=False)
    bank_branch = models.CharField(max_length=60, null=False, blank=False)
    ifsc_code = models.CharField(max_length=20, null=False, blank=False )
    swift_code = models.CharField(max_length=20, null=True, blank=True )
    
    class Meta:
        ordering = ['client_id', 'bank_id']
    
    def __str__(self):
        return f'{self.bank_id}, {self.bank_name}, {self.bank_branch}'
    
class ProductCategory(models.Model):
    client_id        = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    product_category = models.CharField(primary_key=True, max_length=15, null=False,
                                        blank=False)
    category_name    = models.CharField(max_length=80, null=False, blank=False)
    company_code = models.ForeignKey('CompanyCode', on_delete=models.SET_NULL, null=True)
    valid_from       = models.DateField(default=date.today)
    valid_to         = models.DateField()
    
    class Meta:
        ordering = ['client_id', 'product_category']    
    
    def __str__(self):
        # return f'{self.product_category}, {self.category_name}'
        return self.category_name

class ProductSubCategory(models.Model):
    client_id            = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    product_sub_category = models.CharField(primary_key=True, max_length=15, null=False,
                                        blank=False)
    sub_category_name    = models.CharField(max_length=80, null=False, blank=False)
    product_category     = models.ForeignKey('ProductCategory',  
                                             on_delete=models.SET_NULL, null=True)
    valid_from           = models.DateField(default=date.today)
    valid_to             = models.DateField()
    
    class Meta:
        ordering = ['client_id', 'product_sub_category']    
    
    def __str__(self):
        # return f'{self.product_sub_category}, {self.sub_category_name}'
        return self.sub_category_name

class Product(models.Model):
    client_id            = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    product_id           = models.CharField(primary_key=True, max_length=15, null=False,
                                        blank=False)
    product_name         = models.CharField(max_length=80, null=False, blank=False)
    product_category     = models.ForeignKey('ProductCategory', 
                                             on_delete=models.SET_NULL, null=True)
    product_sub_category = models.ForeignKey('ProductSubCategory', 
                                             on_delete=models.SET_NULL, null=True)
    loan_no_prefix       = models.CharField(max_length=5, null=True, blank=True)
    interest_rate        = models.DecimalField(max_digits=5, decimal_places=2, 
                                              null=True, blank=True)
    valid_from           = models.DateField(default=date.today)
    valid_to             = models.DateField()
    
    class Meta:
        ordering = ['client_id', 'product_id']    
    
    def __str__(self):
        # return f'{self.product_id}, {self.product_name}'
        return self.product_name

    