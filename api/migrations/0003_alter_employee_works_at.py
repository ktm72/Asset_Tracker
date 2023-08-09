# Generated by Django 4.2.4 on 2023-08-09 20:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='works_at',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='works_at', to='api.company'),
        ),
    ]
