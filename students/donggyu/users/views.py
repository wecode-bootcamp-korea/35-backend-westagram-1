import json
import re

from django.http  import JsonResponse
from django.views import View

from users.models import User

class UserView(View):
    def post(self, request):
        # 유저 회원가입
        try:
            data = json.loads(request.body)

            post_name         = data['name']
            post_email        = data['email']
            post_password     = data['password']
            post_phone_number = data['phone_number']

            # 이메일 데이터 유효성 검사
            cheak_email = re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', post_email)

            if cheak_email == None:
                return JsonResponse({"message" : "EMAIL_DATA_ERROR"}, status = 400)

            # 패스워드 데이터 유효성 검사
            cheak_password = re.match('^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$', post_password)

            if cheak_password == None:
                return JsonResponse({"message" : "PASSWORD_DATA_ERROR"}, status = 400)

            # 이메일 중복 검사
            exist_query_set = User.objects.all()

            for exist_object in exist_query_set:
                if post_email == exist_object.email:
                    return JsonResponse({"message" : "DATA_THAT_EXISTS_ERROR"}, status = 409)


            User.objects.create(
                name         = post_name,
                email        = post_email,
                password     = post_password,
                phone_number = post_phone_number
                )

            return JsonResponse({"message": "SUCCESS"}, status = 201)

        except:
            # 필수 데이터 입력확인
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)