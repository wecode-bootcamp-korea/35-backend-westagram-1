import json
import re
import bcrypt
import jwt

from django.http  import JsonResponse
from django.views import View

from users.models import User

class UserView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            name         = data['name']
            email        = data['email']
            password     = data['password']
            phone_number = data['phone_number']

            hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            REGEX_EMAIL    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            REGEX_PASSWORD = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
            
            if not re.match(REGEX_EMAIL, email):
                return JsonResponse({"message" : "EMAIL_VALIDATE_ERROR"}, status = 400)
            
            if not re.match(REGEX_PASSWORD, password):
                return JsonResponse({"message" : "PASSWORD_VALIDATE_ERROR"}, status = 400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"message" : "DATA_THAT_EXISTS_ERROR"}, status = 409)

            User.objects.create(
                name         = name,
                email        = email,
                password     = hash_password,
                phone_number = phone_number
                )

            return JsonResponse({"message": "SIGN_UP_SUCCESS"}, status = 201)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)

class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email    = data['email']
            password = data['password']

            if not bcrypt.checkpw(password.encode('utf-8'), User.objects.get(email=email).password.encode('utf-8')):
                return JsonResponse({"message": "INVALID_USER"}, status = 401)

            token = jwt.encode({'id' : User.objects.get(email=email).id}, 'secret', algorithm='HS256')

            return JsonResponse({"token": token}, status = 200)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)