# Generated by Django 3.1.4 on 2020-12-14 15:11

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0005_auto_20201214_2311'),
        ('masterdata', '0003_productcategory_company_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoanMaster',
            fields=[
                ('loan_no', models.CharField(auto_created=True, editable=False, max_length=15, primary_key=True, serialize=False)),
                ('application_no', models.CharField(blank=True, max_length=30, null=True)),
                ('application_date', models.DateField(default=datetime.date.today)),
                ('amount_finance', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('service_charges', models.DecimalField(blank=True, decimal_places=2, default='0.00', max_digits=15, null=True)),
                ('gst_charges', models.DecimalField(blank=True, decimal_places=2, default='0.00', max_digits=15, null=True)),
                ('vat_charges', models.DecimalField(blank=True, decimal_places=2, default='0.00', max_digits=15, null=True)),
                ('cess_charges', models.DecimalField(blank=True, decimal_places=2, default='0.00', max_digits=15, null=True)),
                ('other_charges', models.DecimalField(blank=True, decimal_places=2, default='0.00', max_digits=15, null=True)),
                ('amount_disburse', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('disbursal_date', models.DateField(default=datetime.date.today)),
                ('interest_start', models.DateField(default=datetime.date.today)),
                ('emi_start', models.DateField(default=datetime.date.today)),
                ('emi_end', models.DateField(default=datetime.date.today)),
                ('principal_os', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('latepayment_os', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('cbc_os', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('first_emi', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('first_payment', models.CharField(choices=[('B', 'Bank Account Transfer'), ('C', 'CHEQUE'), ('D', 'Digital Payment'), ('E', 'ECS'), ('N', 'NACH'), ('S', 'CASH')], default='S', max_length=1)),
                ('payment_mode', models.CharField(choices=[('B', 'Bank Account Transfer'), ('C', 'CHEQUE'), ('D', 'Digital Payment'), ('E', 'ECS'), ('N', 'NACH'), ('S', 'CASH')], default='N', max_length=1)),
                ('instalment_type', models.CharField(choices=[('W', 'Weekly'), ('B', 'Bi-Weekly'), ('M', 'Monthly'), ('Q', 'Quarterly')], default='W', max_length=1)),
                ('total_instalments', models.IntegerField(blank=True, null=True)),
                ('advance_instalments', models.IntegerField(blank=True, null=True)),
                ('paid_instalments', models.IntegerField(blank=True, null=True)),
                ('overdue_instalments', models.IntegerField(blank=True, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=40, null=True)),
                ('bank_branch', models.CharField(blank=True, max_length=40, null=True)),
                ('bank_ifsc', models.CharField(blank=True, max_length=20, null=True)),
                ('bank_account', models.CharField(blank=True, max_length=30, null=True)),
                ('status', models.CharField(blank=True, choices=[('A', 'Active'), ('I', 'Inactive'), ('C', 'Closed')], default='A', max_length=1)),
                ('created_on', models.DateTimeField(auto_now=True, verbose_name='Created On')),
                ('created_by', models.CharField(blank=True, default='', max_length=20)),
                ('changed_on', models.DateTimeField(auto_now_add=True, verbose_name='Changed On')),
                ('changed_by', models.CharField(blank=True, default='', max_length=20)),
                ('branch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='masterdata.branch')),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='masterdata.client')),
                ('costcentre', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='masterdata.costcentre')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='customer.customer')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='masterdata.product')),
                ('profitcentre', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='masterdata.profitcentre')),
            ],
        ),
    ]
