# Generated by Django 3.1.4 on 2020-12-18 07:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0002_auto_20201218_1224'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loanasset',
            old_name='deliver_order',
            new_name='delivery_order',
        ),
    ]
