# Generated by Django 3.1.4 on 2020-12-19 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0005_auto_20201218_2127'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='product_id_start',
            new_name='loan_no_prefix',
        ),
    ]
