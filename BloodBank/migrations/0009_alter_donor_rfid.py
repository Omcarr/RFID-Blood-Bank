# Generated by Django 5.0.1 on 2024-04-22 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BloodBank', '0008_rename_group_drivegroup_delete_bloodpacket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donor',
            name='RFID',
            field=models.CharField(max_length=30, null=True),
        ),
    ]