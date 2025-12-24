from rest_framework import generics, permissions
from .models import VoiceTest
from .serializers import VoiceTestSerializer
from .utils import extract_mfcc
from django.conf import settings
import os

class VoiceUploadView(generics.CreateAPIView):
    serializer_class = VoiceTestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        voice_test = serializer.save()

        # Get absolute path of the uploaded file
        audio_path = voice_test.audio_file.path

        # Define MFCC directory
        mfcc_dir = os.path.join(settings.MEDIA_ROOT, 'mfcc')
        os.makedirs(mfcc_dir, exist_ok=True)

        # Define MFCC file path
        mfcc_path = os.path.join(mfcc_dir, f'{voice_test.id}.png')

        # Generate MFCC
        extract_mfcc(audio_path, mfcc_path)

        # Save the relative path to the model
        voice_test.mfcc_image = f'mfcc/{voice_test.id}.png'
        voice_test.save()
