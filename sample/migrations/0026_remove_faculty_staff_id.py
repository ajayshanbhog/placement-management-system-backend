# Generated by Django 5.1.1 on 2024-11-13 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0025_company_ph_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='faculty',
            name='staff_id',
        ),
    ]
