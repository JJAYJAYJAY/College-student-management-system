from django.db import connection


def safe_sql(sql, params: list = []):
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        # 获取查询结果
        records = dict_fetchall(cursor)
    return records


def dict_fetchall(cursor):
    """将游标返回的行数据转换为字典列表"""
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def get_token_from_request(request):
    # 获取授权头部
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        # 提取token
        token = auth_header.split(' ')[1]
        return token
    return None
