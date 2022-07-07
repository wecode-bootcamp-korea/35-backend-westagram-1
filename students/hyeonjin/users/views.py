import json
import re

from django.http import JsonResponse

from django.shortcuts import render
from django.views import View

# Create your views here.


class JoinView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            email = data["email"]
            password = data["password"]
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        email_validation = re.compile(
            '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        if not email_validation.match(data["email"]):
            return JsonResponse({"message": "Email Validation Error"}, status=400)
        if
