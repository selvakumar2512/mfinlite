from django.contrib import admin
from .models import Client, ChartOfAccounts, AccountingYear, Currency, ControllingArea
from .models import CompanyCode, ProfitCentre, BusinessArea, CostCentre, BankMaster
from .models import Branch, ProductCategory, ProductSubCategory, Product

# Register your models here.
admin.site.register(Client)
admin.site.register(ChartOfAccounts)
admin.site.register(AccountingYear)
admin.site.register(Currency)
admin.site.register(ControllingArea)
admin.site.register(CompanyCode)
admin.site.register(ProfitCentre)
admin.site.register(BusinessArea)
admin.site.register(CostCentre)
admin.site.register(BankMaster)
admin.site.register(Branch)
admin.site.register(ProductCategory)
admin.site.register(ProductSubCategory)
admin.site.register(Product)