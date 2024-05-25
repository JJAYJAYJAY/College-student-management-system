from typing import Dict, Any

import jwt

from backend import settings
from uitls.response import convert_dict_keys_to_camel_case, convert_array_keys_to_camel_case
from uitls.tools import safe_sql


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
    def get_student_info(token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            account = payload['account']
            role = payload['role']
            if role == 0:
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
            else:
                return None
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        except Exception as e:
            return None

    @staticmethod
    def get_student_grade(token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            account = payload['account']
            role = payload['role']
            if role == 0:
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
            else:
                return None
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        except Exception as e:
            return None

    @staticmethod
    def get_student_course(token, term, classId):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            role = payload['role']
            response = {}
            if role == 0:
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
            else:
                return None
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        except Exception as e:
            return None

    @staticmethod
    def get_course_offering(token, classId):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            role = payload['role']
            response = {}
            if role == 0:
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
            else:
                return None
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        except Exception as e:
            return None


class TeacherService:
    def __init__(self):
        pass

    @staticmethod
    def get_teacher_info(token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            account = payload['account']
            role = payload['role']
            if role == 1:
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
                result = safe_sql(sql, [account])
                return result[0]
            else:
                return None
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        except Exception as e:
            return None

    @staticmethod
    def get_teacher_course(token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            account = payload['account']
            role = payload['role']
            response = {}
            if role == 1:
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
                result = safe_sql(sql, [account])
                response["course"] = convert_array_keys_to_camel_case(result)
                return response
            else:
                return None
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        except Exception as e:
            return None
