# Generated by Django 2.1.5 on 2019-03-18 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('costasiella', '0012_financeglaccount_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='financeglaccount',
            name='code',
            field=models.CharField(default='', max_length=255),
        ),
    ]