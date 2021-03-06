# Generated by Django 2.2.10 on 2020-04-10 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('costasiella', '0008_auto_20200410_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='financeorderitem',
            name='attendance_type',
            field=models.CharField(choices=[['TRIAL', 'Trial'], ['DROPIN', 'Drop in'], ['CLASSPASS', 'Classpass'], ['SUBSCRIPTION', 'Subscription'], ['COMPLEMENTARY', 'Complementary'], ['REVIEW', 'To be reviewed'], ['RECONCILE_LATER', 'Reconcile later']], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='financeorderitem',
            name='date',
            field=models.DateField(null=True),
        ),
    ]
