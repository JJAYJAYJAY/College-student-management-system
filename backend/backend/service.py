from uitls.tools import safe_sql


class LoginService:
    def __init__(self):
        pass

    def login(self, account: str, password: str) -> dict:
        sql = "select role from Ljj_Account where account = %s and password = %s"
        result = safe_sql(sql, [account, password])
        if result:
            return result[0]
        else:
            return None
