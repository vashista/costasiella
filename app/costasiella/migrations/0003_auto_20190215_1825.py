# Generated by Django 2.1.5 on 2019-02-15 18:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('costasiella', '0002_auto_20190215_1821'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schoollocation',
            old_name='public_item',
            new_name='public_display',
        ),
    ]