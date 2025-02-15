# Generated by Django 5.1.1 on 2024-11-11 11:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0008_alter_rounds_internship_alter_rounds_job'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicants',
            name='internship',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sample.internship'),
        ),
        migrations.AlterField(
            model_name='applicants',
            name='job',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sample.fulltime'),
        ),
    ]
