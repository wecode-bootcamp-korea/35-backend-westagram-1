import json, re, bcrypt

from django.http  import JsonResponse
from django.views import View

from users.models import User

class SignUpView(View):
    def post(self, request):
        try:
            data           = json.loads(request.body)
            name           = data['name']
            email          = data["email"]
            password       = data["password"]
            mobile_number  = data['mobile_number']
            REGEX_EMAIL    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            REGEX_PASSWORD = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'

            if not re.match(REGEX_EMAIL, email):
                return JsonResponse({"message":"EMAIL_VALIDATION_ERROR"}, status=400)

            if not re.match(REGEX_PASSWORD, password):
                return JsonResponse({"message":"PASSWORD_VALIDATION_ERROR"}, status=400)
            
            if User.objects.filter(email = email).exists():
                return JsonResponse({"message":"DUPLICATION_ERROR"}, status=400)
        
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
             name          = name,
             email         = email,
             password      = hashed_password,
             mobile_number = mobile_number,
            )
            return JsonResponse({'message':'SUCCESS'}, status=201)
            
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

class LogInView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']

            if not User.objects.filter( email = email, password = password).exists():
                return JsonResponse({'message':'INVALID_USER'}, status=401)
            return JsonResponse({'message':'SUCCESS'}, status=200)
        
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)