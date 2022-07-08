import json
import re

from django.http import JsonResponse
from django.views import View

from users.models import User

class SignupView(View):
    
    def post(self, request):
        data = json.loads(request.body)

        # 이메일이나 패스워드가 전달되지 않는 경우 KeyError 예외처리
        # 다른 데이터도 모두 KeyError 확인
        try:                       
            email        = data['email']
            password     = data['password']
            name         = data['name']
            phone_number = data['phone_number']
            others       = data['others']
            
            # 이메일에 @와 .이 포함되어 있는지
            # 비밀번호 8자리 이상, 문자, 숫자, 특수문자 복합인지- 확인하기 위해 정규표현식 활용 
            email_validation = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            password_validation = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'

            if not re.match(email_validation, data['email']):
                return JsonResponse({'message': 'Email Validation Error'}, status=400)

            if not re.match(password_validation, data['password']):
                return JsonResponse({'message': 'Password Validation Error'}, status=400)
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'E-mail Duplicate'}, status=400)

            User.objects.create(
                name         = name,
                email        = email,
                password     = password,
                phone_number = phone_number,
            )
            return JsonResponse({'message':'SUCCESS'}, status=201)

        except KeyError:
           return JsonResponse({'message': 'KEY_ERROR'}, status=400)
