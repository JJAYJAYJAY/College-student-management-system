from django.db import models


class Major(models.Model):
    major_id = models.CharField(primary_key=True, max_length=50)
    major_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'Ljj_Major'


class Class(models.Model):
    class_id = models.CharField(primary_key=True, max_length=50)
    class_name = models.CharField(max_length=100)
    major = models.ForeignKey(Major, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Ljj_Class'


class Course(models.Model):
    course_id = models.CharField(primary_key=True, max_length=50)
    course_name = models.CharField(max_length=100)
    major = models.ForeignKey(Major, on_delete=models.CASCADE)
    credit = models.IntegerField()
    hours = models.IntegerField()
    term = models.CharField(max_length=20)

    class Meta:
        db_table = 'Ljj_Course'


class Student(models.Model):
    student_id = models.CharField(primary_key=True, max_length=50)
    student_name = models.CharField(max_length=100)
    sex = models.IntegerField(choices=((0, 'Female'), (1, 'Male')))
    age = models.IntegerField()
    had_credit = models.IntegerField()
    region = models.CharField(max_length=20)
    class_info = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)
    account = models.CharField(max_length=100)

    class Meta:
        db_table = 'Ljj_Student'


class Admin(models.Model):
    admin_id = models.CharField(primary_key=True, max_length=50)
    admin_name = models.CharField(max_length=100)
    account = models.CharField(max_length=100)

    class Meta:
        db_table = 'Ljj_Admin'


class Teacher(models.Model):
    teacher_id = models.CharField(primary_key=True, max_length=50)
    teacher_name = models.CharField(max_length=100)
    sex = models.IntegerField(choices=((0, 'Female'), (1, 'Male')))
    age = models.IntegerField()
    job_title = models.CharField(max_length=60)
    phone = models.CharField(max_length=20)
    account = models.CharField(max_length=100)

    class Meta:
        db_table = 'Ljj_Teacher'


class Account(models.Model):
    account = models.CharField(primary_key=True, max_length=50)
    password = models.CharField(max_length=100)
    role = models.IntegerField(choices=((0, 'Student'), (1, 'Admin'), (2, 'Teacher')))

    class Meta:
        db_table = 'Ljj_Account'


class CourseEnrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    grade = models.IntegerField()
    term = models.CharField(max_length=20)

    class Meta:
        db_table = 'Ljj_CourseEnrollment'


class CourseOffering(models.Model):
    class_info = models.ForeignKey(Class, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Ljj_CourseOffering'
