# Generated by Django 2.2.10 on 2020-04-17 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('costasiella', '0023_auto_20200415_1559'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemMailTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(editable=False, max_length=255)),
                ('subject', models.TextField()),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('content', models.TextField()),
            ],
        ),
    ]
