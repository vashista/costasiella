# Generated by Django 2.2.2 on 2019-07-26 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('costasiella', '0012_financeinvoice_accounts'),
    ]

    operations = [
        migrations.AddField(
            model_name='financeinvoice',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='financeinvoice',
            name='paid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='financeinvoice',
            name='sub_total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='financeinvoice',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='financeinvoice',
            name='vat',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.DeleteModel(
            name='FinanceInvoiceAmount',
        ),
    ]