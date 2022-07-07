import json
import re

from django.http import JsonResponse

from django.shortcuts import render
from django.views import View

class SignupView(View):
    """
    목적: 사용자 정보를 데이터베이스에 저장

    1. client에게 사용자 정보를 받는다.
    2. 받은 정보를 DB에 저장한다.
    """
    def post(self, request):
        """
        request.body = {
            "name"        : "hyeonjin"
            "email"       : "hhj@sample.com"
            "password"    : "password12*"
            "phone_number": "01012341234"
            "others"      : "text"
        }
        """
        data = json.loads(request.body)

        # 이메일이나 패스워드가 전달되지 않는 경우 KeyError 예외처리
        try:                       
            email    = data["email"]
            password = data["password"]
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        # Email Validation # 이메일에 @와 .이 포함되어 있는지 확인하기 위해 정규표현식 활용 
        email_validation = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        if email_validation.match(data["email"]) == None:
            return JsonResponse({"message": "Email Validation Error"}, status=400)

        # Password Validation # 비밀번호 8자리 이상, 문자, 숫자, 특수문자 복합인지 확인
        password_validation = re.compile("^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$")
        if password_validation.match(data['password']) == None:
            return JsonResponse({"message": "Password Validation Error"}, status=400)

