# Generated by Django 3.1.4 on 2020-12-27 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0016_auto_20201227_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loantransactions',
            name='payment_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]