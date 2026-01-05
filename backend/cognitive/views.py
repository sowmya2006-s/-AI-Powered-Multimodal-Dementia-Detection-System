from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from patients.models import Patient
from .models import CognitiveResult
from .visual.game_logic import VisualMemorySession
from .audio.game_logic import AudioMemorySession
from .scoring.memory_score import compute_memory_score

ROUND_DELAYS = [5, 10, 30, 60]
IMAGE_POOL = [f"image_{i}.jpg" for i in range(1, 11)]  # Placeholder pool
AUDIO_POOL = [f"audio_{i}.mp3" for i in range(1, 11)]  # Placeholder pool

class StartTest(APIView):
    def post(self, request):
        test_mode = request.data.get("test_mode", "visual")
        patient_id = request.data.get("patient_id")
        
        if not patient_id:
            return Response({"error": "patient_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        request.session["patient_id"] = patient_id
        request.session["test_mode"] = test_mode
        request.session["used_items"] = []
        request.session["round_scores"] = []
        request.session["round_index"] = 0
        request.session.modified = True
        
        print(f"DEBUG: Test started for patient {patient_id}, mode {test_mode}")
        return Response({"message": "Test started", "test_mode": test_mode, "round": 1}, status=status.HTTP_200_OK)

class GenerateRound(APIView):
    def get(self, request):
        round_index = request.session.get("round_index")
        if round_index is None:
            return Response({"error": "Test not started"}, status=status.HTTP_400_BAD_REQUEST)
        
        if round_index >= len(ROUND_DELAYS):
            return Response({"completed": True}, status=status.HTTP_200_OK)
        
        test_mode = request.session["test_mode"]
        delay = ROUND_DELAYS[round_index]
        used_items = request.session["used_items"]
        
        print(f"DEBUG: Generating Round {round_index + 1} for mode {test_mode}")
        
        try:
            if test_mode == "visual":
                session = VisualMemorySession(image_pool=IMAGE_POOL, used_images=used_items)
                round_data = session.generate_round(delay)
                request.session["used_items"] = round_data["used_images"]
            else:
                session = AudioMemorySession(audio_pool=AUDIO_POOL, used_audio=used_items)
                round_data = session.generate_round(delay)
                request.session["used_items"] = round_data["used_audio"]
            
            request.session["current_target"] = round_data["target"]
            request.session.modified = True
            
            round_data["round"] = round_index + 1
            return Response(round_data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SubmitAnswer(APIView):
    def post(self, request):
        if "current_target" not in request.session:
            return Response({"error": "No active round"}, status=status.HTTP_400_BAD_REQUEST)
        
        user_answer = request.data.get("answer")
        target = request.session["current_target"]
        
        score = 1 if user_answer == target else 0
        
        scores = request.session.get("round_scores", [])
        scores.append(score)
        request.session["round_scores"] = scores
        
        round_index = request.session.get("round_index", 0)
        request.session["round_index"] = round_index + 1
        
        print(f"DEBUG: Round {round_index + 1} submitted. Correct: {score == 1}. Next index: {round_index + 1}")
        
        del request.session["current_target"]
        request.session.modified = True
        
        return Response({
            "correct": score == 1,
            "next_round": request.session["round_index"] < len(ROUND_DELAYS)
        }, status=status.HTTP_200_OK)

class FinishTest(APIView):
    def post(self, request):
        round_scores = request.session.get("round_scores", [])
        if len(round_scores) < len(ROUND_DELAYS):
            return Response({"error": "Incomplete test"}, status=status.HTTP_400_BAD_REQUEST)
        
        patient_id = request.session["patient_id"]
        test_mode = request.session["test_mode"]
        
        patient = get_object_or_404(Patient, id=patient_id)
        result = compute_memory_score(round_scores)
        
        CognitiveResult.objects.create(
            patient=patient,
            test_mode=test_mode,
            round_1=round_scores[0],
            round_2=round_scores[1],
            round_3=round_scores[2],
            round_4=round_scores[3],
            memory_accuracy=result["accuracy"],
            recall_decay_rate=result["decay_rate"],
            risk_level=result["risk_level"]
        )
        
        print(f"DEBUG: Test finished for patient {patient_id}. Accuracy: {result['accuracy']}")
        
        # Clear session
        keys_to_clear = ["patient_id", "test_mode", "used_items", "round_scores", "round_index"]
        for key in keys_to_clear:
            if key in request.session:
                del request.session[key]
        request.session.modified = True
        
        return Response(result, status=status.HTTP_201_CREATED)

