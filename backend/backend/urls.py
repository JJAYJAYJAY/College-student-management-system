"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.urls import path
from .views import *

urlpatterns = [
    path('api/login', Login.as_view(), name='login'),
    path('api/student/get_student_info', GetStudentInfo.as_view(), name='student'),
    path('api/student/get_student_grade', GetStudentGrade.as_view(), name='student_grade'),
    path('api/student/get_student_course', GetStudentCourse.as_view(), name='student_course'),
    path('api/student/get_course_offering', GetCourseOffering.as_view(), name='course_offering'),
    path('api/teacher/get_teacher_info', GetTeacherInfo.as_view(), name='teacher'),
    path('api/teacher/get_teacher_course', GetTeacherCourse.as_view(), name='teacher_course'),
    path('api/teacher/teacher_get_student_grade', TeacherGetStudentGrade.as_view(), name='teacher_student_grade'),
    path('api/teacher/update_student_grade', UpdateStudentGrade.as_view(), name='update_student_grade'),
    path('api/teacher/update_student_from_excel', UpdateStudentFromExcel.as_view(), name='update_student_from_excel'),
    path('api/admin/get_admin_info', GetAdminInfo.as_view(), name='admin'),
    path('api/admin/admin_get_student_info', AdminGetStudentInfo.as_view(), name='admin_student'),
    path('api/admin/admin_get_teacher_info', AdminGetTeacherInfo.as_view(), name='admin_teacher'),
    path('api/admin/admin_get_student_change_info', AdminGetStudentChangeInfo.as_view(), name='admin_student_change'),
    path('api/admin/update_student_info', UpdateStudentInfo.as_view(), name='update_student_info'),
    path('api/admin/delete_student_info', DeleteStudentInfo.as_view(), name='delete_student_info'),
    path('api/admin/update_student_info_from_excel', UpdateStudentInfoFromExcel.as_view(), name='update_student_info_from_excel'),
    path('api/admin/admin_get_teacher_change_info', AdminGetTeacherChangeInfo.as_view(), name='admin_teacher_change'),
    path('api/admin/update_teacher_info', UpdateTeacherInfo.as_view(), name='update_teacher_info'),
    path('api/admin/delete_teacher_info', DeleteTeacherInfo.as_view(), name='delete_teacher_info'),
    path('api/admin/update_teacher_info_from_excel', UpdateTeacherInfoFromExcel.as_view(), name='update_teacher_info_from_excel'),
    path('api/admin/admin_get_course_info', AdminGetCourseInfo.as_view(), name='admin_course'),
    path('api/admin/delete_course_info', DeleteCourseInfo.as_view(), name='delete_course_info'),
    path('api/admin/update_course_info_from_excel', UpdateCourseInfoFromExcel.as_view(), name='update_course_from_excel'),
]

