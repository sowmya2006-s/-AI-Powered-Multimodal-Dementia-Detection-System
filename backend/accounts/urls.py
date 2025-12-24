from django.urls import path
from .views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView
from .tokens import EmailTokenObtainPairSerializer


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer


urlpatterns = [
    path('signup/', RegisterView.as_view()),
    path('login/', EmailTokenObtainPairView.as_view()),
]
