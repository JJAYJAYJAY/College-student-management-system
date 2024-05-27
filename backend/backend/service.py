import functools
from pprint import pprint
from typing import Any

import jwt
from django.db import connection, transaction

from backend import settings
from uitls.response import convert_array_keys_to_camel_case
from uitls.tools import safe_sql


def jwt_required(role_required=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(token, *args, **kwargs):
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                role = payload.get('role')
                if role_required is not None and role != role_required:
                    return {"msg": "无权限访问"}
                return func(payload, *args, **kwargs)
            except jwt.ExpiredSignatureError:
                return {"code": 400, "msg": "令牌过期"}
            except jwt.InvalidTokenError:
                return {"code": 400, "msg": "无效令牌"}
            except Exception as e:
                return {"code": 400, "msg": str(e)}
        return wrapper
    return decorator


class LoginService:
    def __init__(self):
        pass

    @staticmethod
    def login(account: str, password: str) -> Any | None:
        sql = "select role from Ljj_Account where account = %s and password = %s"
        result = safe_sql(sql, [account, password])
        if result[0]["role"] == 0:
            sql = "select class_id from Ljj_Student where account = %s"
            class_id = safe_sql(sql, [account])
        else:
            class_id = [{"class_id": None}]
        if result:
            response = {
                "token": jwt.encode({"account": account, "role": result[0]["role"]}, settings.SECRET_KEY,
                                    algorithm='HS256'),
                "role": result[0]["role"],
                "classId": class_id[0]["class_id"]
            }
            return response
        else:
            return None


class StudentService:
    def __init__(self):
        pass

    @staticmethod
    @jwt_required(role_required=0)
    def get_student_info(payload):
        account = payload['account']
        sql = """
        select 
            student_id,
            student_name, 
            if(Sex=0,'女','男') as sex,
            age, 
            had_credit, 
            region,   
            class_name, 
            major_name
        from Ljj_Student join ljj_class on Ljj_Student.class_id = ljj_class.Class_id
            join ljj_major on ljj_class.major_id = ljj_major.major_id
        where account = %s
        """
        result = safe_sql(sql, [account])
        return result[0]

    @staticmethod
    @jwt_required(role_required=0)
    def get_student_grade(payload):
        account = payload['account']
        response = {}
        # 查询总绩点、总学时和学分
        sql = """
            select 
            GPA
            from ljj_studentgpa
            where Student_id = %s
        """
        result = safe_sql(sql, [account])
        response["GPA"] = result[0]["GPA"]

        sql = """
            select
            had_credit
            from ljj_student
            where student_id = %s
        """
        result = safe_sql(sql, [account])
        response["had_credit"] = result[0]["had_credit"]

        sql = """
            select
            sum(hours) as total_hours
            from ljj_course join ljj_grade on ljj_course.course_id = ljj_grade.course_id
            where student_id = %s and grade is not null and grade >= 60
        """
        result = safe_sql(sql, [account])
        response["total_hours"] = result[0]["total_hours"]

        # 查询历年绩点
        sql = """
            select 
            GPA,
            term
            from ljj_studenttermgpa
            where Student_id = %s
        """
        result = safe_sql(sql, [account])
        response["term_gpa"] = result

        # 查询课程成绩
        sql = """
            select 
            course_name,
            test_method,
            credit,
            ljj_grade.term,
            grade,
            hours,
            if(Grade>=60,(Grade-50)/10,0) as point
            from ljj_course join ljj_grade on ljj_course.course_id = ljj_grade.course_id
            where Grade is not null and student_id = %s
        """
        result = safe_sql(sql, [account])
        response["course_grade"] = convert_array_keys_to_camel_case(result)
        return response

    @staticmethod
    @jwt_required(role_required=0)
    def get_student_course(payload, term, classId):
        response = {}
        sql = """
        select 
            course_name,
            credit,
            teacher_name,
            hours,
            test_method,
            term
        from ljj_classcourse
        where term = %s and class_id = %s
        """
        result = safe_sql(sql, [term, classId])
        response["course"] = convert_array_keys_to_camel_case(result)
        sql = "select distinct term from ljj_classcourse where class_id = %s"
        result = safe_sql(sql, [classId])
        response["term"] = convert_array_keys_to_camel_case(result)
        return response

    @staticmethod
    @jwt_required(role_required=0)
    def get_course_offering(payload, classId):
        response = {}
        # 查询所有班级
        sql = """
        select 
            class_id,
            class_name
        from ljj_class
        """
        result = safe_sql(sql)
        response["allCourse"] = convert_array_keys_to_camel_case(result)
        # 查询特定班级
        sql = """
        select 
            course_name,
            credit,
            teacher_name,
            hours,
            test_method,
            term
        from ljj_classcourse
        where class_id = %s
        """
        result = safe_sql(sql, [classId])
        response["detailCourse"] = convert_array_keys_to_camel_case(result)
        return response


class TeacherService:
    def __init__(self):
        pass

    @staticmethod
    @jwt_required(role_required=1)
    def get_teacher_info(payload):
        sql = """
        select 
            teacher_id,
            teacher_name,
            sex,
            age,
            job_title,
            phone
        from ljj_teacher
        where account = %s
        """
        result = safe_sql(sql, [payload['account']])
        return result[0]

    @staticmethod
    @jwt_required(role_required=1)
    def get_teacher_course(payload):
        response = {}
        sql = """
        select 
            course_name,
            credit,
            hours,
            class_name,
            test_method,
            term
        from ljj_teachercourse
        where teacher_id = %s
        """
        result = safe_sql(sql, [payload['account']])
        response["course"] = convert_array_keys_to_camel_case(result)
        return response

    @staticmethod
    @jwt_required(role_required=1)
    def teacher_get_student_grade(payload, classId, courseId):
        params = [payload['account']]
        response = {}
        sql = """
        select distinct 
            course_id,
            course_name
        from ljj_teachercourse
        where Teacher_id = %s
        """
        result = safe_sql(sql, params)
        response["courses"] = convert_array_keys_to_camel_case(result)
        if courseId:
            sql = """
                select 
                class_id,
                class_name
                from ljj_teachercourse
                where Teacher_id = %s and course_id = %s
            """
            result = safe_sql(sql, params + [courseId])
            response["classes"] = convert_array_keys_to_camel_case(result)
        if classId and courseId:
            sql = """
                select 
                ljj_studentcourse.course_id as course_id,
                course_name as course_name,
                test_method as test_method,
                credit as credit,
                grade as grade,
                hours as hours,
                Class_name as class_name,
                ljj_studentcourse.student_id as student_id,
                student_name as student_name,
                round(if(Grade>=60,(Grade-50)/10,0),1) as point,
                ljj_studentcourse.Term as term
                from ljj_studentcourse 
                    join ljj_grade on 
                    ljj_studentcourse.student_id = ljj_grade.student_id and 
                    ljj_studentcourse.course_id = ljj_grade.course_id
                    join ljj_class on ljj_studentcourse.class_id = ljj_class.class_id
                where ljj_studentcourse.class_id = %s and ljj_studentcourse.course_id = %s
            """
            result = safe_sql(sql, [classId, courseId])
            response["studentsScore"] = convert_array_keys_to_camel_case(result)
            sql = """
                select
                    round(avg(grade),2) as average_grade,
                    max(grade) as max_grade,
                    min(grade) as min_grade
                from ljj_studentcourse 
                    join ljj_grade on 
                    ljj_studentcourse.student_id = ljj_grade.student_id and 
                    ljj_studentcourse.course_id = ljj_grade.course_id
                    join ljj_class on ljj_studentcourse.class_id = ljj_class.class_id
                where ljj_studentcourse.class_id = %s and ljj_studentcourse.course_id = %s
            """
            result = safe_sql(sql, [classId, courseId])
            response["scoreTotalData"] = result[0]

            sql = """
            SELECT
                COUNT(ljj_studentcourse.Student_id) AS count,
                CASE
                    WHEN grade >= 0 AND grade < 60 THEN '0-60'
                    WHEN grade >= 60 AND grade < 65 THEN '60-65'
                    WHEN grade >= 65 AND grade < 70 THEN '65-70'
                    WHEN grade >= 70 AND grade < 75 THEN '70-75'
                    WHEN grade >= 75 AND grade < 80 THEN '75-80'
                    WHEN grade >= 80 AND grade < 85 THEN '80-85'
                    WHEN grade >= 85 AND grade < 90 THEN '85-90'
                    WHEN grade >= 90 AND grade < 95 THEN '90-95'
                    WHEN grade >= 95 AND grade <= 100 THEN '95-100'
                    when grade is null then '未录入'
                END AS grade_range
            FROM ljj_studentcourse 
            JOIN ljj_grade 
                ON ljj_studentcourse.student_id = ljj_grade.student_id 
                AND ljj_studentcourse.course_id = ljj_grade.course_id
            JOIN ljj_class 
                ON ljj_studentcourse.class_id = ljj_class.class_id
            WHERE ljj_studentcourse.class_id = %s 
                AND ljj_studentcourse.course_id = %s
            GROUP BY grade_range
            ORDER BY grade_range;
            """
            result = safe_sql(sql, [classId, courseId])
            response["gradeDistribution"] = convert_array_keys_to_camel_case(result)

        return response

    @staticmethod
    @jwt_required(role_required=1)
    def update_student_grade(payload, data):
        if len(data) == 0:
            return {"msg": "没有修改"}
        sql = "update ljj_grade set grade = %s where student_id = %s and course_id = %s"
        params = [(item['grade'], item['studentId'], item['courseId']) for item in data]
        with connection.cursor() as cursor:
            cursor.executemany(sql, params)
            connection.commit()
        return {"msg": "更新成功"}

    @staticmethod
    @jwt_required(role_required=1)
    def update_student_from_excel(payload, data):
        sql = "update ljj_grade set grade = %s where student_id = %s and course_id = %s"
        params = [(data.loc[i, '成绩'], data.loc[i, '学号'], data.loc[i, '课程号']) for i in range(len(data))]
        with connection.cursor() as cursor:
            cursor.executemany(sql, params)
            connection.commit()
        return {"msg": "更新成功"}


class AdminService:
    def __init__(self):
        pass

    @staticmethod
    @jwt_required(role_required=2)
    def get_admin_info(payload):
        account = payload['account']
        sql = "SELECT admin_id, admin_name FROM ljj_admin WHERE account = %s"
        result = safe_sql(sql, [account])
        return result[0] if result else None

    @staticmethod
    @jwt_required(role_required=2)
    def admin_get_student_info(payload):
        response = {}
        with transaction.atomic():
            sql = """
            select 
                ljj_student.student_id as student_id,
                ljj_student.student_name as student_name,
                if(Sex=0,'女','男') as sex,
                age,
                had_credit,
                region,
                class_name,
                major_name,
                round(GPA,3) as GPA
                from ljj_student left join ljj_class on ljj_student.class_id = ljj_class.class_id
                left join ljj_major  on ljj_class.major_id = ljj_major.major_id 
                left join ljj_studentgpa on ljj_student.student_id = ljj_studentgpa.student_id
            """
            result = safe_sql(sql)
            response["students"] = convert_array_keys_to_camel_case(result)
            sql = """
                select 
                region as name,
                count(*) as value
                from ljj_student 
                group by region 
            """
            result = safe_sql(sql)
            response["regionData"] = convert_array_keys_to_camel_case(result)

            # 统计男女比例
            sql = """
                select
                    count(*) as value,
                    if(sex = 0,'女','男') as name
                from ljj_student
                group by sex
            """
            result = safe_sql(sql)
            response["sexData"] = convert_array_keys_to_camel_case(result)

            sql = """
            select
                round(count(*),0) as total_student,
                round((select avg(GPA) from ljj_studentgpa),3) as average_GPA
            from ljj_student
            """
            result = safe_sql(sql)
            response['totalData'] = result[0]
            return response

    @staticmethod
    @jwt_required(role_required=2)
    def admin_get_teacher_info(payload):
        response = {}
        with transaction.atomic():
            sql = """
            select 
                teacher_id,
                teacher_name,
                if(Sex=0,'女','男') as sex,
                age,
                job_title,
                phone
                from ljj_teacher
            """
            result = safe_sql(sql)
            response["teachers"] = convert_array_keys_to_camel_case(result)

            sql = """
                select 
                job_title as name,
                count(*) as value
                from ljj_teacher
                group by job_title
            """
            result = safe_sql(sql)
            response["jobTitleData"] = convert_array_keys_to_camel_case(result)

            sql = """
                select
                    count(*) as value,
                    if(Sex = 0,'女','男') as name
                from
                ljj_teacher
                group by sex
            """
            result = safe_sql(sql)
            response["sexData"] = convert_array_keys_to_camel_case(result)

            sql = """
            select
                round(count(*),0) as total_teacher,
                round(avg(age),2) as average_age
            from ljj_teacher
            """
            result = safe_sql(sql)
            response['totalData'] = result[0]
        return response

    @staticmethod
    @jwt_required(role_required=2)
    def admin_get_student_change_info(payload):
        response = {}
        with transaction.atomic():
            sql = """
            select 
                student_id,
                student_name,
                if(sex=0,'女','男') as sex,
                age,
                had_credit,
                region,
                ljj_student.class_id as class_id,
                class_name,
                ljj_class.Major_id as major_id,
                major_name
                from ljj_student left join ljj_class on ljj_student.class_id = ljj_class.class_id
                left join ljj_major on ljj_class.major_id = ljj_major.major_id
            """
            result = safe_sql(sql)
            response["students"] = convert_array_keys_to_camel_case(result)

            sql = """
                select
                    class_id,
                    class_name
                from ljj_class
            """
            result = safe_sql(sql)
            response["classes"] = convert_array_keys_to_camel_case(result)
            return response

    @staticmethod
    @jwt_required(role_required=2)
    def update_student_info(payload, data):
        if len(data) == 0:
            return {"msg": "没有修改"}
        sql = """
            update ljj_student
            set student_name = %s, age = %s, sex=%s, class_id = %s, region = %s
            where student_id = %s
        """
        params = [
            (
                item['studentName'],
                item["age"],
                1 if item['sex'] == "男" else 0,
                item['classId'],
                item['region'],
                item['studentId']
            ) for item in data
        ]
        pprint(params)
        with connection.cursor() as cursor:
            cursor.executemany(sql, params)
            connection.commit()
        return {"msg": "更新成功"}

    @staticmethod
    @jwt_required(role_required=2)
    def delete_student_info(payload, studentId):
        sql = "delete from ljj_student where student_id = %s"
        with connection.cursor() as cursor:
            cursor.execute(sql, [studentId])
            connection.commit()
        return {"msg": "删除成功"}

    @staticmethod
    @jwt_required(role_required=2)
    def update_student_info_from_excel(payload, data):
        with transaction.atomic():
            sql = """
                select 
                student_id
                from ljj_student
                """
            result = safe_sql(sql)
            student_id = [item['student_id'] for item in result]
            params = [
                [
                    data.loc[i, "学生姓名"],
                    0 if data.loc[i, "性别"] == '女' else 1,
                    data.loc[i, "年龄"],
                    data.loc[i, "生源地"],
                    data.loc[i, "班级号"],
                    data.loc[i, '学号'],
                ] for i in range(len(data))
            ]
            for item in params:
                if item[-1] in student_id:
                    sql = """
                    update ljj_student
                    set student_name = %s, sex = %s, age = %s, region = %s, class_id = %s
                    where student_id = %s 
                    """
                    safe_sql(sql, item)
                else:
                    sql = """
                        call insert_student(%s,%s,%s,%s,%s,%s,%s)
                    """
                    safe_sql(sql, [item[-1], item[0], item[2], item[1], item[3], item[4], item[-1]])
            return {"msg": "更新成功"}

    @staticmethod
    @jwt_required(role_required=2)
    def admin_get_teacher_change_info(payload):
        response = {}
        with transaction.atomic():
            sql = """
                select 
                    teacher_id,
                    teacher_name,
                    job_title,
                    age,
                    if(Sex=0,'女','男') as sex,
                    phone
                from ljj_teacher
            """
            result = safe_sql(sql)
            response["teachers"] = convert_array_keys_to_camel_case(result)
            return response

    @staticmethod
    @jwt_required(role_required=2)
    def update_teacher_info(payload, data):
        if len(data) == 0:
            return {"msg": "没有修改"}
        sql = """
            update ljj_teacher
            set teacher_name = %s, Sex = %s, age = %s, job_title = %s, phone = %s
            where teacher_id = %s
        """
        params = [
            (
                item['teacherName'],
                0 if item['sex'] == "女" else 1,
                item['age'],
                item['jobTitle'],
                item['phone'],
                item['teacherId']
            ) for item in data
        ]
        with connection.cursor() as cursor:
            cursor.executemany(sql, params)
            connection.commit()
        return {"msg": "更新成功"}

    @staticmethod
    @jwt_required(role_required=2)
    def delete_teacher_info(payload, teacherId):
        sql = "delete from ljj_teacher where teacher_id = %s"
        with connection.cursor() as cursor:
            cursor.execute(sql, [teacherId])
            connection.commit()
        return {"msg": "删除成功"}

    @staticmethod
    @jwt_required(role_required=2)
    def update_teacher_info_from_excel(payload, data):
        with transaction.atomic():
            sql = """
                select 
                teacher_id
                from ljj_teacher
                """
            result = safe_sql(sql)
            teacher_id = [item['teacher_id'] for item in result]
            params = [
                [
                    data.loc[i, "教师姓名"],
                    0 if data.loc[i, "性别"] == '女' else 1,
                    data.loc[i, "年龄"],
                    data.loc[i, "职称"],
                    data.loc[i, '电话'],
                    data.loc[i, '教师号'],
                ] for i in range(len(data))
            ]
            for item in params:
                if item[-1] in teacher_id:
                    sql = """
                    update ljj_teacher
                    set teacher_name = %s, sex = %s, age = %s, job_title = %s, phone = %s
                    where teacher_id = %s 
                    """
                    safe_sql(sql, item)
                else:
                    sql = """
                        call insert_teacher(%s,%s,%s,%s,%s,%s)
                    """
                    safe_sql(sql, [item[-1], item[0], item[1], item[2], item[3], item[4]])
            return {"msg": "更新成功"}

    @staticmethod
    @jwt_required(role_required=2)
    def admin_get_course_info(payload, classId):
        response = {}
        with transaction.atomic():
            sql = """
            select 
                major_id,
                major_name
            from ljj_major
            """
            result = safe_sql(sql)
            response["majorData"] = convert_array_keys_to_camel_case(result)

            sql = """
                select 
                major_id,
                class_name,
                class_id
                from ljj_class
            """
            result = safe_sql(sql)
            majorClassDict = {}
            for item in result:
                if item['major_id'] not in majorClassDict:
                    majorClassDict[item['major_id']] = []
                majorClassDict[item['major_id']].append({
                    "className": item['class_name'],
                    "classId": item['class_id']
                })
            response["classData"] = majorClassDict

            sql = """
            select
                Major_name as majorName,
                ljj_class.class_id as classId,
                ljj_class.class_name as className,
                course_id as courseId,
                course_name as courseName,
                test_method as testMethod,
                credit as credit,
                hours as hours,
                term as term,
                teacher_name as teacherName
            from ljj_classcourse 
            join ljj_class on ljj_classcourse.class_id = ljj_class.class_id
            join ljj_major on ljj_class.major_id = ljj_major.major_id
            where ljj_classcourse.class_id = %s
            """
            result = safe_sql(sql, [classId])
            if result:
                response['courseData'] = convert_array_keys_to_camel_case(result)
        return response

    @staticmethod
    @jwt_required(role_required=2)
    def delete_course_info(payload, classId, courseId):
        sql = "delete from ljj_courseoffering where class_id =%s and course_id = %s"
        with connection.cursor() as cursor:
            cursor.execute(sql, [classId,courseId])
            connection.commit()
        return {"msg": "删除成功"}

    @staticmethod
    @jwt_required(role_required=2)
    def update_course_from_excel(payload, data):
        with transaction.atomic():
            sql = """
                select 
                class_id,
                course_id
                from ljj_courseoffering
                """
            result = safe_sql(sql)
            class_course = [(item['class_id'], item['course_id']) for item in result]
            params = [
                [
                    data.loc[i, "班级号"],
                    data.loc[i, "课程号"],
                    data.loc[i, "教师号"],
                ] for i in range(len(data))
            ]
            for item in params:
                if (item[0], item[1]) in class_course:
                    sql = """
                        update ljj_courseoffering
                        set teacher_id = %s
                        where Class_id = %s and course_id = %s
                    """
                    safe_sql(sql, [item[2], item[0], item[1]])
                else:
                    sql = """
                        insert into ljj_courseoffering values (%s,%s,%s)
                    """
                    safe_sql(sql, [item[0], item[1], item[2]])
            return {"code": 200, "msg": "更新成功"}
