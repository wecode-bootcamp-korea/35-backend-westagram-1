from django.urls import path, include

from users.views import UserView

urlpatterns = [
    path('', UserView.as_view()),
]