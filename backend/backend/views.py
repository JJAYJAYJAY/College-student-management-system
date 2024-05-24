from django.http import JsonResponse
from rest_framework.views import APIView

from .service import LoginService
from uitls.response import Response

class Login(APIView):
    def post(self, request):
        account = request.data.get('username')
        password = request.data.get('password')
        response = LoginService().login(account, password)
        if response:
            return Response().ok(response, status=200)
        else:
            return JsonResponse({'error': '用户名或密码错误'}, status=400)
