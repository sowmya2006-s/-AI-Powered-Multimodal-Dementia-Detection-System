from django.db import models
from patients.models import Patient

class AssessmentReport(models.Model):
    RISK_LEVELS = [
        ('LOW', 'Low Risk'),
        ('MEDIUM', 'Medium Risk'),
        ('HIGH', 'High Risk'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    voice_score = models.FloatField(null=True, blank=True)
    cognitive_score = models.FloatField(null=True, blank=True)
    mri_score = models.FloatField(null=True, blank=True)
    mri_label = models.CharField(max_length=50, null=True, blank=True)
    overall_risk = models.CharField(max_length=10, choices=RISK_LEVELS)
    mri_triggered = models.BooleanField(default=False)
    recommendation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report - {self.patient.name} - {self.overall_risk}"
