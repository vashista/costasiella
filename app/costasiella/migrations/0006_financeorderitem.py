# Generated by Django 2.2.10 on 2020-04-09 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('costasiella', '0005_auto_20200409_1550'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinanceOrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance_type', models.CharField(choices=[['TRIAL', 'Trial'], ['DROPIN', 'Drop in'], ['CLASSPASS', 'Classpass'], ['SUBSCRIPTION', 'Subscription'], ['COMPLEMENTARY', 'Complementary'], ['REVIEW', 'To be reviewed'], ['RECONCILE_LATER', 'Reconcile later']], max_length=255)),
                ('date', models.DateField()),
                ('product_name', models.CharField(max_length=255)),
                ('description', models.TextField(default='')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=20)),
                ('price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('tax', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('finance_costcenter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='costasiella.FinanceCostCenter')),
                ('finance_glaccount', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='costasiella.FinanceGLAccount')),
                ('finance_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='costasiella.FinanceOrder')),
                ('finance_tax_rate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='costasiella.FinanceTaxRate')),
                ('schedule_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='costasiella.ScheduleItem')),
            ],
        ),
    ]
