# Generated by Django 3.1.4 on 2020-12-23 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0014_auto_20201223_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loantransactions',
            name='invoice_no',
            field=models.CharField(auto_created=True, blank=True, max_length=20, null=True),
        ),
    ]