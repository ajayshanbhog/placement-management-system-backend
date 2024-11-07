from django.contrib import admin
from .models import Faculty,Sample,Student,Company,FullTime,Rounds,Internship

admin.site.register(Sample)
admin.site.register(Faculty)
admin.site.register(Student)
admin.site.register(Company)
admin.site.register(FullTime)
admin.site.register(Internship)
admin.site.register(Rounds)