"""
URL configuration for sample project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
    path('admin/', admin.site.urls),
    # Api for Login
    path('login/faculty', views.login_faculty, name='login_faculty'),
    path('login/company', views.login_company, name='login_company'),
    path('login/student', views.login_student, name='login_student'),

    # Api for Register
    path('register/student/', views.register_student, name='register_student'),
    path('register/company/', views.register_company, name='register_company'),
    path('register/faculty/', views.register_faculty, name='register_faculty'),

     # Internship URLs
    path('api/internship/', views.InternshipListCreateView.as_view(), name='internship-list-create'),
    #path('api/internship/<int:pk>/', views.InternshipRetrieveUpdateDestroyView.as_view(), name='internship-detail'),

    # FullTime Job URLs
    path('api/fulltime/', views.FullTimeListCreateView.as_view(), name='fulltime-list-create'),
    #path('api/fulltime/<int:pk>/', views.FullTimeRetrieveUpdateDestroyView.as_view(), name='fulltime-detail'),

    path('api/students/<int:faculty_user_id>/', views.get_students_by_faculty, name='get_students_by_faculty'),

    #path('api/internships/<str:cgpa>/', views.internship_list, name='internship-list'),
    #path('api/fulltimes/<str:cgpa>/', views.fulltime_list, name='fulltime-list'),

    path('api/internships/<str:srn>/', views.internship_list_by_srn, name='internship-list-by-srn'),
    path('api/fulltimes/<str:srn>/', views.fulltime_list_by_srn, name='fulltime-list-by-srn'),


    path('api/apply/', views.apply, name="apply"),
    path('api/check_application_status/', views.check_application_status, name='check-application-status'),
    path('api/applicants/company/<int:company_id>/', views.get_applicants_for_company),
    path('api/applicants/toggle-status/<int:applicant_id>/', views.toggle_applicant_status, name='toggle_applicant_status'),

    # Api for Profile 
    path('get/faculty/<int:user_id>/', views.get_faculty_profile, name='get_faculty_profile'),
    path('get/student/<int:user_id>/', views.get_student_profile, name='get_student_profile'),
    path('get/company/<int:user_id>/', views.get_company_profile, name='get_company_profile'),    
    path('update/faculty/<int:faculty_id>/', views.update_faculty_profile, name='update_faculty'),
    path('update/student/<int:student_id>/', views.update_student_profile, name='update_student'),
    path('update/company/<int:company_id>/', views.update_company_profile, name='update_company'),



    path('api/create/round/', views.create_round, name='create_round'),

    path('api/internship_rounds/<int:student_id>/', views.internship_rounds, name='internship-rounds'),
    path('api/fulltime_rounds/<int:student_id>/', views.job_rounds, name='job-rounds'),

    path('api/fulltime-operation/<int:pk>/', views.fulltime_detail, name='fulltime-detail'),
    path('api/internship-operation/<int:pk>/', views.internship_detail, name='internship-detail'),

    path('api/<int:company_id>/rounds/<int:id>/', views.get_rounds_company_internship_fulltime, name='get_rounds'),
    path('api/rounds/delete/<int:round_id>/', views.delete_round, name='delete_round'),

    path('api/students-result/faculty/<int:faculty_id>/', views.get_students_results_by_faculty, name='get_students_by_faculty'),

    path('api/check_selected_status/<int:student_id>/', views.check_selected_status, name='check_selected_status'),
    path('api/rounds/toggle-status/<int:round_id>/', views.toggle_round_status, name='toggle_round_status'),    
]


