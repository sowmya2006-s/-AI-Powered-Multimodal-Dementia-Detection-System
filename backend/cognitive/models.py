from django.db import models
from patients.models import Patient

class CognitiveResult(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    test_mode = models.CharField(
        max_length=10,
        choices=[("visual", "Visual"), ("audio", "Audio")]
    )

    round_1 = models.IntegerField()
    round_2 = models.IntegerField()
    round_3 = models.IntegerField()
    round_4 = models.IntegerField()

    memory_accuracy = models.FloatField()
    recall_decay_rate = models.FloatField()

    risk_level = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.name} - {self.test_mode} - {self.risk_level}"
