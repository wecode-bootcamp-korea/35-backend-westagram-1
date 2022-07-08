import json
import re

from django.db    import IntegrityError
from django.http  import JsonResponse
from django.views import View

from users.models import User

class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            name          = data['name']
            email         = data['email']
            password      = data['password']
            mobile_number = data['mobile_number']

            email_validation = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            if email_validation.match(email) == None:
                return JsonResponse({'message':'EMAIL_VALIDATION_FALSE'}, status=400)
            
            password_validation = re.compile('^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$')
            if password_validation.match(password) == None:
                return JsonResponse({'message':'PASSWORD_VALIDATION_FALSE'}, status=400)


            User.objects.create(
                name          = name,
                email         = email,
                password      = password,
                mobile_number = mobile_number
            )

            return JsonResponse({'message': 'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        except IntegrityError:
            return JsonResponse({'message': 'EMAIL_MUST_BE_UNIQUE'}, status=400)