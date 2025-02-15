# Generated by Django 5.1.1 on 2024-11-04 02:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('company_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(blank=True, max_length=50, null=True)),
                ('designation_role', models.CharField(blank=True, max_length=50, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('package', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('user_id', models.IntegerField(unique=True)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('faculty_id', models.AutoField(primary_key=True, serialize=False)),
                ('role', models.CharField(max_length=50)),
                ('staff_id', models.CharField(max_length=10, unique=True)),
                ('user_id', models.IntegerField(unique=True)),
                ('password', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('ph_number', models.CharField(blank=True, max_length=15, null=True)),
                ('department', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Internship',
            fields=[
                ('internship_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('stipend', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('ppo', models.BooleanField(default=False)),
                ('type', models.CharField(blank=True, max_length=50, null=True)),
                ('duration', models.IntegerField(blank=True, help_text='Duration in months', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FullTime',
            fields=[
                ('job_id', models.AutoField(primary_key=True, serialize=False)),
                ('job_title', models.CharField(blank=True, max_length=100, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('package', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sample.company')),
            ],
        ),
        migrations.CreateModel(
            name='Rounds',
            fields=[
                ('round_id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=50)),
                ('round_no', models.IntegerField()),
                ('no_of_students', models.IntegerField(blank=True, null=True)),
                ('datetime', models.DateTimeField(blank=True, null=True)),
                ('company_name', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(choices=[('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Scheduled', max_length=10)),
                ('comp_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comp_id_rounds', to='sample.company')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company_rounds', to='sample.company')),
                ('fulltime', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sample.fulltime')),
                ('internship', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sample.internship')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('SRN', models.CharField(max_length=15, unique=True)),
                ('branch', models.CharField(blank=True, max_length=50, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('ph_number', models.CharField(blank=True, max_length=15, null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='Other', max_length=6)),
                ('cgpa', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('faculty_advisor', models.CharField(blank=True, max_length=50, null=True)),
                ('password', models.CharField(max_length=255)),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sample.faculty')),
            ],
        ),
    ]
