from pprint import pprint

import pandas as pd
from django.http import JsonResponse
from rest_framework.views import APIView

from .service import LoginService, StudentService, TeacherService, AdminService
from uitls.response import Response
from uitls.tools import *


class Login(APIView):
    def post(self, request):
        account = request.data.get('username')
        password = request.data.get('password')
        response = LoginService.login(account, password)
        if response:
            return Response().ok(response, status=200)
        else:
            return Response().fail('登录失败', status=400)


class GetStudentInfo(APIView):
    def post(self, request):
        # 请求头获得token
        token = get_token_from_request(request)
        response = StudentService.get_student_info(token)
        if response:
            return Response().ok(response, status=200)
        else:
            return Response().fail('获取学生信息失败', status=400)


class GetStudentGrade(APIView):
    def post(self, request):
        # 请求头获得token
        token = get_token_from_request(request)
        response = StudentService.get_student_grade(token)
        if response:
            return Response().ok(response, status=200)
        else:
            return Response().fail('获取学生成绩失败', status=400)


class GetStudentCourse(APIView):
    def post(self, request):
        # 请求头获得token
        token = get_token_from_request(request)
        term = request.data.get('term')
        classId = request.data.get('classId')
        response = StudentService.get_student_course(token, term, classId)
        if response:
            return Response().ok(response, status=200)
        else:
            return Response().fail('获取学生课程失败', status=400)


class GetCourseOffering(APIView):
    def post(self, request):
        # 请求头获得token
        token = get_token_from_request(request)
        classId = request.data.get('classId')
        response = StudentService.get_course_offering(token, classId)
        if response:
            return Response().ok(response, status=200)
        else:
            return Response().fail('获取课程信息失败', status=400)


class GetTeacherInfo(APIView):
    def post(self, request):
        # 请求头获得token
        token = get_token_from_request(request)
        response = TeacherService.get_teacher_info(token)
        if response:
            return Response().ok(response, status=200)
        else:
            return Response().fail('获取教师信息失败', status=400)


class GetTeacherCourse(APIView):
    def post(self, request):
        # 请求头获得token
        token = get_token_from_request(request)
        response = TeacherService.get_teacher_course(token)
        if response:
            return Response().ok(response, status=200)
        else:
            return Response().fail('获取教师课程失败', status=400)


class TeacherGetStudentGrade(APIView):
    def post(self, request):
        # 请求头获得token
        token = get_token_from_request(request)
        classId = request.data.get('classId')
        courseId = request.data.get('courseId')
        response = TeacherService.teacher_get_student_grade(token, classId, courseId)
        if response:
            return Response().ok(response, status=200)
        else:
            return Response().fail('获取学生成绩失败', status=400)


class UpdateStudentGrade(APIView):
    def post(self, request):
        # 请求头获得token
        token = get_token_from_request(request)
        updateData = request.data.get('data')
        response = TeacherService.update_student_grade(token, updateData)
        if response:
            return Response().ok(response, status=200)
        else:
            return Response().fail('升级学生成绩失败', status=400)


class UpdateStudentFromExcel(APIView):
    def post(self, request):
        # 请求头获得token
        token = get_token_from_request(request)
        # 读取excel文件
        excelFile = request.FILES.get('file')
        updateData = pd.read_excel(excelFile)
        response = TeacherService.update_student_from_excel(token, updateData)
        if response:
            return Response().ok(response, status=200)
        else:
            return Response().fail('升级学生成绩失败', status=400)


class GetAdminInfo(APIView):
    def post(self, request):
        # 请求头获得token
        token = get_token_from_request(request)
        response = AdminService.get_admin_info(token)
        if response:
            return Response().ok(response, status=200)
        else:
            return Response().fail('获取管理员信息失败', status=400)


class AdminGetStudentInfo(APIView):
    def post(self, request):
        # 请求头获得token
        token = get_token_from_request(request)
        response = AdminService.admin_get_student_info(token)
        if response:
            return Response().ok(response, status=200)
        else:
            return Response().fail('获取学生信息失败', status=400)


class AdminGetTeacherInfo(APIView):
    def post(self, request):
        # 请求头获得token
        token = get_token_from_request(request)
        response = AdminService.admin_get_teacher_info(token)
        if response:
            return Response().ok(response, status=200)
        else:
            return Response().fail('获取教师信息失败', status=400)


class AdminGetStudentChangeInfo(APIView):
    def post(self, request):
        # 请求头获得token
        token = get_token_from_request(request)
        response = AdminService.admin_get_student_change_info(token)
        if response:
            return Response().ok(response, status=200)
        else:
            return Response().fail('获取学生信息失败', status=400)


class UpdateStudentInfo(APIView):
    def post(self, request):
        # 请求头获得token
        token = get_token_from_request(request)
        updateData = request.data.get('data')
        response = AdminService.update_student_info(token, updateData)
        if response:
            return Response().ok(response, status=200)
        else:
            return Response().fail('更新学生信息失败', status=400)


class DeleteStudentInfo(APIView):
    def post(self, request):
        # 请求头获得token
        token = get_token_from_request(request)
        studentId = request.data.get('studentId')
        response = AdminService.delete_student_info(token, studentId)
        if response:
            return Response().ok(response, status=200)
        else:
            return Response().fail('删除学生信息失败', status=400)


class UpdateStudentInfoFromExcel(APIView):
    def post(self, request):
        # 请求头获得token
        token = get_token_from_request(request)
        # 读取excel文件
        excelFile = request.FILES.get('file')
        updateData = pd.read_excel(excelFile)
        response = AdminService.update_student_info_from_excel(token, updateData)
        if response:
            return Response().ok(response, status=200)
        else:
            return Response().fail('更新学生信息失败', status=400)


class AdminGetTeacherChangeInfo(APIView):
    def post(self, request):
        # 请求头获得token
        token = get_token_from_request(request)
        response = AdminService.admin_get_teacher_change_info(token)
        if response:
            return Response().ok(response, status=200)
        else:
            return Response().fail('获取教师信息失败', status=400)


class UpdateTeacherInfo(APIView):
    def post(self, request):
        # 请求头获得token
        token = get_token_from_request(request)
        updateData = request.data.get('data')
        response = AdminService.update_teacher_info(token, updateData)
        if response:
            return Response().ok(response, status=200)
        else:
            return Response().fail('更新教师信息失败', status=400)


class DeleteTeacherInfo(APIView):
    def post(self, request):
        # 请求头获得token
        token = get_token_from_request(request)
        teacherId = request.data.get('teacherId')
        response = AdminService.delete_teacher_info(token, teacherId)
        if response:
            return Response().ok(response, status=200)
        else:
            return Response().fail('删除教师信息失败', status=400)


class UpdateTeacherInfoFromExcel(APIView):
    def post(self, request):
        # 请求头获得token
        token = get_token_from_request(request)
        # 读取excel文件
        excelFile = request.FILES.get('file')
        updateData = pd.read_excel(excelFile)
        response = AdminService.update_teacher_info_from_excel(token, updateData)
        if response:
            return Response().ok(response, status=200)
        else:
            return Response().fail('更新教师信息失败', status=400)


class AdminGetCourseInfo(APIView):
    def post(self, request):
        # 请求头获得token
        token = get_token_from_request(request)
        classId = request.data.get('classId')
        response = AdminService.admin_get_course_info(token, classId)
        if response:
            return Response().ok(response, status=200)
        else:
            return Response().fail('获取课程信息失败', status=400)


class DeleteCourseInfo(APIView):
    def post(self, request):
        # 请求头获得token
        token = get_token_from_request(request)
        classId = request.data.get('classId')
        courseId = request.data.get('courseId')
        response = AdminService.delete_course_info(token, classId, courseId)
        if response:
            return Response().ok(response, status=200)
        else:
            return Response().fail('删除课程信息失败', status=400)


class UpdateCourseInfoFromExcel(APIView):
    def post(self, request):
        # 请求头获得token
        token = get_token_from_request(request)
        # 读取excel文件
        excelFile = request.FILES.get('file')
        updateData = pd.read_excel(excelFile)
        response = AdminService.update_course_from_excel(token, updateData)
        if response and response['code'] != 400:
            return Response().ok(response, status=200)
        else:
            return Response().fail('更新课程信息失败', status=400)