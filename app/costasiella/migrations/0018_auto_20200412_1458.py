# Generated by Django 2.2.10 on 2020-04-12 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('costasiella', '0017_integrationlogmollie_log_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='integrationlogmollie',
            name='webhook_url',
            field=models.TextField(null=True),
        ),
    ]
