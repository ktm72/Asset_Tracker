# Generated by Django 4.2.4 on 2023-08-10 21:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_gearlog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gearlog',
            name='checkout_date',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='gearlog',
            name='returned_condition',
            field=models.TextField(blank=True, null=True),
        ),
    ]
