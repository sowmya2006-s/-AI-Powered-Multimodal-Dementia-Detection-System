from rest_framework import serializers
from .models import VoiceTest

class VoiceTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoiceTest
        fields = '__all__'
        read_only_fields = ['mfcc_image', 'dementia_score']
