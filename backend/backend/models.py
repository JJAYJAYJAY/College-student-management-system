from django.db import models


class LjjMajor(models.Model):
    Major_id = models.CharField(max_length=50, primary_key=True)
    Major_name = models.CharField(max_length=100, null=False)

    class Meta:
        db_table = 'Ljj_Major'
        verbose_name = '专业'
        verbose_name_plural = '专业'


class LjjClass(models.Model):
    Class_id = models.CharField(max_length=50, primary_key=True)
    Class_name = models.CharField(max_length=100, null=False)
    Major_id = models.ForeignKey(LjjMajor, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Ljj_Class'
        verbose_name = '班级'
        verbose_name_plural = '班级'


class LjjCourse(models.Model):
    Course_id = models.CharField(max_length=50, primary_key=True)
    Course_name = models.CharField(max_length=100, null=False)
    Test_method = models.CharField(max_length=20, null=False)
    Credit = models.IntegerField(null=False)
    Hours = models.IntegerField(null=False)
    Term = models.CharField(max_length=20, null=False)

    class Meta:
        db_table = 'Ljj_Course'
        verbose_name = '课程'
        verbose_name_plural = '课程'


class LjjAccount(models.Model):
    Account = models.CharField(max_length=50, primary_key=True)
    Password = models.CharField(max_length=100, null=False)
    Role = models.IntegerField(choices=((0, '学生'), (1, '教师'), (2, '管理员')), null=False)

    class Meta:
        db_table = 'Ljj_Account'
        verbose_name = '账户'
        verbose_name_plural = '账户'


class LjjStudent(models.Model):
    Student_id = models.CharField(max_length=50, primary_key=True)
    Student_name = models.CharField(max_length=100, null=False)

    class Meta:
        db_table = 'Ljj_Student'
        verbose_name = '学生'
        verbose_name_plural = '学生'


class LjjAdmin(models.Model):
    Admin_id = models.CharField(max_length=50, primary_key=True)
    Admin_name = models.CharField(max_length=100, null=False)

    class Meta:
        db_table = 'Ljj_Admin'
        verbose_name = '管理员'
        verbose_name_plural = '管理员'


class LjjTeacher(models.Model):
    Teacher_id = models.CharField(max_length=50, primary_key=True)
    Teacher_name = models.CharField(max_length=100, null=False)

    class Meta:
        db_table = 'Ljj_Teacher'
        verbose_name = '教师'
        verbose_name_plural = '教师'


class LjjGrade(models.Model):
    Student_id = models.ForeignKey(LjjStudent, on_delete=models.CASCADE)
    Course_id = models.ForeignKey(LjjCourse, on_delete=models.CASCADE)
    Grade = models.IntegerField(null=False)
    Term = models.CharField(max_length=20, null=False)

    class Meta:
        db_table = 'Ljj_Grade'
        verbose_name = '成绩'
        verbose_name_plural = '成绩'


class LjjCourseOffering(models.Model):
    Class_id = models.ForeignKey(LjjClass, on_delete=models.CASCADE)
    Course_id = models.ForeignKey(LjjCourse, on_delete=models.CASCADE)
    Teacher_id = models.ForeignKey(LjjTeacher, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Ljj_CourseOffering'
        verbose_name = '课程开设'
        verbose_name_plural = '课程开设'
