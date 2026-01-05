from django.urls import path
from .views import VoiceUploadView, PatientAudioStorageView

urlpatterns = [
    path('upload/', VoiceUploadView.as_view()), # Phase 1: Inference
    path('store/', PatientAudioStorageView.as_view()), # Phase 2: Storage
]
