from django.db import models
from datetime import date, time

class Faculty(models.Model):
    faculty_id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    ph_number = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]

    student_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    SRN = models.CharField(max_length=15, unique=True)
    branch = models.CharField(max_length=50, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    email = models.EmailField(unique=True)
    ph_number = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='Other')
    cgpa = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    faculty_advisor = models.CharField(max_length=50, blank=True, null=True)
    user_id = models.ForeignKey(Faculty, null=True, on_delete=models.SET_NULL)
    password = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name


class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, blank=True, null=True)
    ph_number = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True,default=None)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class FullTime(models.Model):
    job_id = models.AutoField(primary_key=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    package = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cutoff = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True, help_text='Cutoff CGPA required')
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.job_title or "Full-Time Job"


class Internship(models.Model):
    internship_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True, null=True)
    stipend = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    ppo = models.BooleanField(default=False)
    type = models.CharField(max_length=50, blank=True, null=True)
    duration = models.IntegerField(null=True, blank=True, help_text='Duration in months')
    cutoff = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True, help_text='Cutoff CGPA required')
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Rounds(models.Model):
   
    # Constants for 'Status' field
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    ]

    TYPE_CHOICES = [
        ('Internship', 'Internship'),
        ('FullTime', 'FullTime')
    ]
    # Fields
    round_id = models.AutoField(primary_key=True)
    round_no = models.IntegerField(default=-1)
    round_name = models.CharField(max_length=100,default='Not Mentioned')  # New field for Round Name
    date = models.DateField(default=date.today)  # Date in YYYYMMDD format
    time_scheduled = models.TimeField(default=time(9, 0))  # Separate field for time
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Scheduled')
    company = models.ForeignKey(Company, on_delete=models.CASCADE,default=None)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=None)
    internship = models.ForeignKey(Internship, null=True, blank=True, on_delete=models.CASCADE,default=None)
    job = models.ForeignKey(FullTime, null=True, blank=True, on_delete=models.CASCADE,default=None)

    def __str__(self):
        return f"Round {self.round_no} - {self.round_name} - {self.get_status_display()}"



class Applicants(models.Model):
    APPLICATION_TYPE_CHOICES = [
        ('Internship', 'Internship'),
        ('FullTime', 'FullTime')
    ]
    
    STATUS_CHOICES = [
        ('selected', 'Selected'),
        ('notselected', 'Not Selected')
    ]

    applicant_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=APPLICATION_TYPE_CHOICES)
    internship = models.ForeignKey(Internship, null=True, blank=True, on_delete=models.CASCADE)
    job = models.ForeignKey(FullTime, null=True, blank=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default='notselected')

    def __str__(self):
        return f"{self.student.name} - {self.type} - {self.company.name} - {self.status}"

    class Meta:
        unique_together = ('student', 'company', 'type', 'internship', 'job')
