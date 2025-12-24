from django.db import models
from patients.models import Patient

class VoiceTest(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    audio_file = models.FileField(upload_to='voice/')
    mfcc_image = models.ImageField(upload_to='mfcc/', null=True, blank=True)
    dementia_score = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"VoiceTest - {self.patient.name}"
