import json
import re
import bcrypt

from django.http  import JsonResponse
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

            # global EMAIL_VALIDATION
            # global PASSWORD_VALIDATION

            EMAIL_VALIDATION    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            PASSWORD_VALIDATION = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'

            if not re.match(EMAIL_VALIDATION, email):
                return JsonResponse({'message': 'Email Validation Error'}, status=400)

            if not re.match(PASSWORD_VALIDATION, password):
                return JsonResponse({'message': 'Password Validation Error'}, status=400)
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'E-mail Duplicate'}, status=400)

            encoded_password = password.encode('utf-8')
            hashed_password  = bcrypt.hashpw(encoded_password, bcrypt.gensalt())

            User.objects.create(
                name         = name,
                email        = email,
                password     = hashed_password,
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

            encoded_password = password.encode('utf-8')
            hashed_password  = bcrypt.hashpw(encoded_password, bcrypt.gensalt())            

            if not User.objects.filter(email=email, password=hashed_password).exists():
                return JsonResponse({"message":"INVALID_USER"}, status=401)
            return JsonResponse({"message":"SUCCESS"}, status=200)    

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)



