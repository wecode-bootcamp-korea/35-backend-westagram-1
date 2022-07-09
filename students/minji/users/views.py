import json
import re

from django.http  import JsonResponse
from django.views import View

from users.models import User

class SignUpView(View):
    def post(self, request):
        try:
            data                = json.loads(request.body)
            email               = data["email"]
            password            = data["password"]
            REGEX_EMAIL    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            REGEX_PASSWORD = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'

            if not re.match(REGEX_EMAIL, value):
                return JsonResponse({"message":"EMAIL_VALIDATION_ERROR"}, status=400)

            if not re.match(REGEX_PASSWORD, value):
                return JsonResponse({"message":"PASSWORD_VALIDATION_ERROR"}, status=400)
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({"message":"DUPLICATION_ERROR"}, status=400)
        
            User.objects.create(
             name          = data['name'],
             email         = data['email'],
             password      = data['password'],
             mobile_number = data['mobile_number'],
            )
            return JsonResponse({'message':'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)