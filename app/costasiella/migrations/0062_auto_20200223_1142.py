# Generated by Django 2.2.8 on 2020-02-23 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('costasiella', '0061_auto_20200222_1110'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'permissions': [('view_insight', 'Can view insight menu'), ('view_insightclasspassescurrent', 'Can view insight classpasses current'), ('view_insightclasspassessold', 'Can view insight classpasses sold')]},
        ),
    ]