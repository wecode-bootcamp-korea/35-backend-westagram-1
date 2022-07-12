import json,re, bcrypt, jwt

from django.http  import JsonResponse
from django.views import View
from django.conf import settings

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

            return JsonResponse({"message" : "SIGN_UP_SUCCESS"}, status = 201)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)

class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email    = data['email']
            password = data['password']
            
            user = User.objects.get(email=email)

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({"message" : "INVALID_USER"}, status = 401)

            acess_token = jwt.encode({'id' : user.id}, settings.SECRET_KEY, settings.ALGOLITHM)

            return JsonResponse({"message" : "SIGN_IN_SUCCESS", "token": acess_token}, status = 200)

        except User.DoesNotExist:
            return JsonResponse({"message" : "DOES_NOT_EXIST_ERROR"}, status = 404)
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)