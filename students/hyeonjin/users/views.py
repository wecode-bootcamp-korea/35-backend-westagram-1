import json, re, bcrypt, jwt

from django.http  import JsonResponse
from django.views import View

from users.models import User
from my_settings import SECRET_KEY, ALGORITHM


EMAIL_VALIDATION    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
PASSWORD_VALIDATION = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'

class SignupView(View):
    
    def post(self, request):
        data = json.loads(request.body)

        try:                       
            email        = data['email']
            password     = data['password']
            name         = data['name']
            phone_number = data['phone_number']
            others       = data['others']

            global EMAIL_VALIDATION
            global PASSWORD_VALIDATION

            if not re.match(EMAIL_VALIDATION, email):
                return JsonResponse({'message': 'Email Validation Error'}, status=400)

            if not re.match(PASSWORD_VALIDATION, password):
                return JsonResponse({'message': 'Password Validation Error'}, status=400)
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'E-mail Duplicate'}, status=400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

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

            user = User.objects.get(email=email)
            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({"message":"INVALID_USER"}, status=401)

            encoded_jwt = jwt.encode({'user_id': user.id}, SECRET_KEY, ALGORITHM)
            return JsonResponse({"message":"SUCCESS", "access_token": encoded_jwt}, status=200)  
                
        except User.DoesNotExist:
            return JsonResponse({"message":"INVALID_USER"}, status=401)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)



