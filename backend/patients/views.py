from rest_framework import generics, permissions
from .models import Patient
from .serializers import PatientSerializer


class PatientCreateView(generics.CreateAPIView):
	serializer_class = PatientSerializer
	permission_classes = [permissions.IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)
