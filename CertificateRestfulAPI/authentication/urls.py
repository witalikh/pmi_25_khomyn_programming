from django.urls import path
from .views import RegistrationAPIView, LoginAPIView, RefreshAPIView

urlpatterns = [
   path('users/', RegistrationAPIView.as_view()),
   path('login/', LoginAPIView.as_view()),
   path('refresh/', RefreshAPIView.as_view())
]
