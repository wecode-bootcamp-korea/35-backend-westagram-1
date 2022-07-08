import json
import re

from django.http import JsonResponse
from django.views import View

from users.models import User

class SignupView(View):
    
    def post(self, request):
        data = json.loads(request.body)

        try:                       
            email        = data['email']
            password     = data['password']
            name         = data['name']
            phone_number = data['phone_number']
            others       = data['others']
            
            email_validation    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            password_validation = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'

            if not re.match(email_validation, email):
                return JsonResponse({'message': 'Email Validation Error'}, status=400)

            if not re.match(password_validation, password):
                return JsonResponse({'message': 'Password Validation Error'}, status=400)
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'E-mail Duplicate'}, status=400)

            User.objects.create(
                name         = name,
                email        = email,
                password     = password,
                phone_number = phone_number
            )
            return JsonResponse({'message':'SUCCESS'}, status=201)

        except KeyError:
           return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class LoginView(View):

    def post(self, request):
        data = json.loads(request.body)

        try:
            email    = data['email']
            password = data['password']

            usr = User.objects.get(email=email)
            if usr.password == password:
                print(usr.password)
                print(password)
                return JsonResponse({"message":"SUCCESS"}, status=200)
               
            else:
                return JsonResponse({"message":"WRONG_PASSWORD"}, status=401)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)
        except User.DoesNotExist :
            return JsonResponse({"message": "INVALID_USER"}, status=401)

