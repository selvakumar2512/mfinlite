# Generated by Django 3.1.4 on 2020-12-19 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0006_auto_20201219_1908'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='interest_rate',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
