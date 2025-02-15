# Generated by Django 5.1.1 on 2024-11-13 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0014_remove_company_package_remove_company_ph_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='designation_role',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='package',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='user_id',
            field=models.IntegerField(default=None, unique=True),
        ),
    ]
