# Generated by Django 3.1.4 on 2021-01-01 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0018_auto_20201230_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loantransactions',
            name='payment_mode',
            field=models.CharField(blank=True, choices=[('B', 'Bank Account Transfer'), ('C', 'CHEQUE'), ('D', 'Digital Payment'), ('E', 'ECS'), ('N', 'NACH'), ('S', 'CASH')], default='N', max_length=1, null=True),
        ),
    ]
