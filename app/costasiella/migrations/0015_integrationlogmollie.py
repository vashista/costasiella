# Generated by Django 2.2.10 on 2020-04-12 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('costasiella', '0014_auto_20200412_1422'),
    ]

    operations = [
        migrations.CreateModel(
            name='IntegrationLogMollie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mollie_payment_id', models.CharField(max_length=255)),
                ('recurring_type', models.CharField(max_length=255)),
                ('webhook_url', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('finance_invoice', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='costasiella.FinanceInvoice')),
                ('finance_order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='costasiella.FinanceOrder')),
            ],
        ),
    ]
