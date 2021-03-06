# Generated by Django 3.1.4 on 2021-03-10 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0024_auto_20210124_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanasset',
            name='created_on',
            field=models.DateTimeField(verbose_name='Created On'),
        ),
        migrations.AlterField(
            model_name='loanmaster',
            name='created_on',
            field=models.DateTimeField(verbose_name='Created On'),
        ),
        migrations.AlterField(
            model_name='loantransactions',
            name='created_on',
            field=models.DateTimeField(verbose_name='Created On'),
        ),
        migrations.AlterField(
            model_name='loantransactions',
            name='payment_mode',
            field=models.CharField(blank=True, choices=[('B', 'Bank A/c Trans.'), ('C', 'CHEQUE'), ('D', 'Digital Payment'), ('E', 'ECS'), ('N', 'NACH'), ('S', 'Cash')], default='N', max_length=1, null=True),
        ),
    ]
