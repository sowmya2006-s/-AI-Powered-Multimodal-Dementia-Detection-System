from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from patients.models import Patient
from voice.models import VoiceTest
from cognitive.models import CognitiveResult
from .models import AssessmentReport

class FusionReportView(APIView):
    def post(self, request):
        patient_id = request.data.get("patient_id")
        if not patient_id:
            return Response({"error": "patient_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        patient = get_object_or_404(Patient, id=patient_id)
        
        # Get latest results
        voice_test = VoiceTest.objects.filter(patient=patient).order_by('-created_at').first()
        # Cognitive might be disabled/missing
        try:
             cognitive_result = CognitiveResult.objects.filter(patient=patient).order_by('-created_at').first()
        except:
             cognitive_result = None
        
        if not voice_test and not cognitive_result:
            return Response({
                "error": "No completed tests found for this patient."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Voice Logic
        voice_risk = "LOW"
        voice_score = 0.0
        if voice_test:
            voice_score = voice_test.dementia_score or 0.0
            if voice_score > 0.7:
                voice_risk = "HIGH"
            elif voice_score > 0.4:
                voice_risk = "MEDIUM"

        # Cognitive Logic
        cognitive_risk = "LOW"
        cog_score = 0.0
        if cognitive_result:
            cognitive_risk = cognitive_result.risk_level
            cog_score = cognitive_result.memory_accuracy

        # Fusion Logic (Or Logic)
        overall_risk = "LOW"
        if voice_risk == "HIGH" or cognitive_risk == "HIGH":
            overall_risk = "HIGH"
        elif voice_risk == "MEDIUM" or cognitive_risk == "MEDIUM":
            overall_risk = "MEDIUM"
        
        # If we have only one source, trust that source
        if not cognitive_result:
            overall_risk = voice_risk
        
        mri_triggered = (overall_risk == "HIGH")
        
        recommendation = "Regular monitoring recommended."
        if overall_risk == "HIGH":
            recommendation = "CRITICAL: High risk detected. Immediate MRI and neurologist consultation required."
        elif overall_risk == "MEDIUM":
            recommendation = "Follow-up assessment in 3 months recommended."

        report = AssessmentReport.objects.create(
            patient=patient,
            voice_score=voice_score,
            cognitive_score=cog_score,
            overall_risk=overall_risk,
            mri_triggered=mri_triggered,
            recommendation=recommendation
        )

        return Response({
            "report_id": report.id,
            "overall_risk": overall_risk,
            "mri_triggered": mri_triggered,
            "recommendation": recommendation,
            "voice_score": voice_score,
            "cognitive_score": cog_score
        }, status=status.HTTP_201_CREATED)
