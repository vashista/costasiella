# Generated by Django 2.2.10 on 2020-04-12 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('costasiella', '0018_auto_20200412_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='integrationlogmollie',
            name='payment_data',
            field=models.TextField(null=True),
        ),
    ]