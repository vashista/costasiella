# Generated by Django 2.1.5 on 2019-03-01 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('costasiella', '0004_auto_20190215_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoollocation',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]