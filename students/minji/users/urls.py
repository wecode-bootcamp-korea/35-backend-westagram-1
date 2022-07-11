from django.urls import path

from users.views import SignUpView

urlpatterns = [
    path('/users', SignUpView.as_view()),
]