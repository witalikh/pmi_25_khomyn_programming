from django.urls import path
from .views import RegistrationAPIView, LoginAPIView

urlpatterns = [
   path('users/', RegistrationAPIView.as_view()),
   path('login/', LoginAPIView.as_view()),
]
