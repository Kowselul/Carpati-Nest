# Generated by Django 5.2.1 on 2025-05-28 14:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CarpatiNest_app', '0004_alter_refuge_options_booking'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='check_in_date',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='check_out_date',
        ),
        migrations.AddField(
            model_name='booking',
            name='booking_date',
            field=models.DateField(default=datetime.date.today, verbose_name='Data rezervării'),
        ),
    ]
