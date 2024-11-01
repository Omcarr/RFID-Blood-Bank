# Generated by Django 5.0.1 on 2024-04-17 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BloodBank', '0002_donationdrive_donor_sex_donor_unit_status_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='donationdrive',
            old_name='Date',
            new_name='date_created',
        ),
        migrations.AlterField(
            model_name='donor',
            name='Sex',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Transgender', 'Transgender')], max_length=20, null=True),
        ),
    ]
