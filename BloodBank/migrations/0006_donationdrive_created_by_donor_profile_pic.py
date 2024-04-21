# Generated by Django 5.0.1 on 2024-04-20 14:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BloodBank', '0005_donor_groups'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='donationdrive',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='donor',
            name='profile_pic',
            field=models.ImageField(blank=True, default='default_pfp.png', null=True, upload_to=''),
        ),
    ]