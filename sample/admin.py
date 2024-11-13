from django.contrib import admin
from .models import Faculty,Student,Company,FullTime,Rounds,Internship,Applicants

admin.site.register(Faculty)
admin.site.register(Student)
admin.site.register(Company)
admin.site.register(FullTime)
admin.site.register(Internship)
admin.site.register(Rounds)
admin.site.register(Applicants)