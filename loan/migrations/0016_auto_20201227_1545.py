# Generated by Django 3.1.4 on 2020-12-27 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0015_auto_20201223_2242'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanmaster',
            name='interest_rate',
            field=models.DecimalField(decimal_places=2, default='16.00', max_digits=5),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='loanasset',
            name='asset_no',
            field=models.CharField(max_length=15, primary_key=True, serialize=False),
        ),
    ]
