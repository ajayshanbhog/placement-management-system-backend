# Generated by Django 5.1.1 on 2024-11-07 04:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0003_fulltime_cutoff_internship_company_internship_cutoff'),
    ]

    operations = [
        migrations.CreateModel(
            name='Applicants',
            fields=[
                ('applicant_id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('Internship', 'Internship'), ('FullTime', 'FullTime')], max_length=10)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sample.company')),
                ('internship', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sample.internship')),
                ('job', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sample.fulltime')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sample.student')),
            ],
            options={
                'unique_together': {('student', 'company', 'type', 'internship', 'job')},
            },
        ),
    ]
