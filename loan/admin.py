from django.contrib import admin

# Register your models here.

from .models import LoanMaster, LoanAsset, LoanTransactions

admin.site.register(LoanMaster)
admin.site.register(LoanAsset)
admin.site.register(LoanTransactions)
