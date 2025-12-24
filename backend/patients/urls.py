from django.urls import path
from .views import PatientCreateView

urlpatterns = [
    path('create/', PatientCreateView.as_view()),
]
