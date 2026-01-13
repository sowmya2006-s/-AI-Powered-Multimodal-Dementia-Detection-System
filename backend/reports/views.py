import os
import sys
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from patients.models import Patient
from voice.models import VoiceTest
from cognitive.models import CognitiveResult
from .models import AssessmentReport
from accounts.models import User

# Add project root to sys.path for AI models
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.append(project_root)

from ai_models.mri.bagging_inference import predict_mri_ensemble

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

class MRIUploadView(APIView):
    def post(self, request):
        patient_id = request.data.get("patient_id")
        file_obj = request.FILES.get("mri_image")

        if not file_obj:
            return Response({"error": "mri_image (file) is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not patient_id:
             # Demo Mode: Use or create a generic demo patient
             try:
                 user, _ = User.objects.get_or_create(email="demo@viva.com")
                 patient, _ = Patient.objects.get_or_create(
                    user=user, 
                    name="Demo Patient", 
                    defaults={'age': 70, 'gender': 'M', 'language': 'en', 'education': 'HS'}
                )
                 patient_id = patient.id
             except Exception as e:
                 print(f"Error creating demo patient: {e}")
                 # Fallback if DB is completely broken (unlikely)
                 return Response({"error": "System error: Could not initialize demo session."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        patient = get_object_or_404(Patient, id=patient_id)

        # Save temporary file for inference
        os.makedirs("temp_mri", exist_ok=True)
        temp_path = os.path.join("temp_mri", file_obj.name)
        with open(temp_path, 'wb+') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)

        # Run AI Inference (BAGGING ENSEMBLE)
        label, prob = predict_mri_ensemble(temp_path)
        
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)

        if label == "Unknown" or prob == 0.0:
             return Response({"error": "MRI analysis failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Update latest report if it exists
        report = AssessmentReport.objects.filter(patient=patient).order_by('-created_at').first()
        if report:
            report.recommendation += f" | MRI Analysis Result: {label} (Confidence: {prob:.2f})"
            report.save()

        return Response({
            "patient_id": patient_id,
            "mri_result": label,
            "confidence": prob,
            "recommendation": "Consult neurologist for next steps." if label != "NonDemented" else "Routine checkups recommended."
        }, status=status.HTTP_200_OK)
