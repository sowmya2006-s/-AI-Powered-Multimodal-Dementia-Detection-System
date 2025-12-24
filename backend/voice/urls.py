from django.urls import path
from .views import VoiceUploadView

urlpatterns = [
    path('upload/', VoiceUploadView.as_view()),
]
