# Generated by Django 4.2.4 on 2023-08-10 21:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_gearlog_checkout_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gearlog',
            name='checkout_date',
        ),
        migrations.RemoveField(
            model_name='gearlog',
            name='returned_date',
        ),
    ]
