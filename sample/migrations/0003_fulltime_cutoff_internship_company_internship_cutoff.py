# Generated by Django 5.1.1 on 2024-11-06 14:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0002_company_faculty_internship_fulltime_rounds_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='fulltime',
            name='cutoff',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Cutoff CGPA required', max_digits=4, null=True),
        ),
        migrations.AddField(
            model_name='internship',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sample.company'),
        ),
        migrations.AddField(
            model_name='internship',
            name='cutoff',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Cutoff CGPA required', max_digits=4, null=True),
        ),
    ]
