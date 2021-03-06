# Generated by Django 3.1.4 on 2020-12-18 07:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0003_productcategory_company_code'),
        ('loan', '0003_auto_20201218_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanmaster',
            name='ext_loan_no',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='loanmaster',
            name='currency',
            field=models.ForeignKey(default='INR', null=True, on_delete=django.db.models.deletion.SET_NULL, to='masterdata.currency'),
        ),
    ]
