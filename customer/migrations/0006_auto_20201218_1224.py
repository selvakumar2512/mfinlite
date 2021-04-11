# Generated by Django 3.1.4 on 2020-12-18 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_auto_20201214_2311'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='gua_first_name',
            field=models.CharField(default='test', max_length=80),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='gua_full_name',
            field=models.CharField(blank=True, max_length=160, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='gua_last_name',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='gua_middle_name',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='gua_mobile',
            field=models.CharField(default='345354', max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='gua_title',
            field=models.CharField(blank=True, choices=[('MR', 'Mr.'), ('MS', 'Ms.'), ('MRS', 'Mrs.'), ('DR', 'Dr.')], default='MR', max_length=3, verbose_name='title'),
        ),
    ]