# Generated by Django 2.2 on 2019-06-05 01:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('costasiella', '0017_schedule'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Schedule',
            new_name='ScheduleItem',
        ),
    ]