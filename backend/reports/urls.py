from django.urls import path
from .views import FusionReportView, MRIUploadView

urlpatterns = [
    path('generate/', FusionReportView.as_view(), name='generate-report'),
    path('mri-upload/', MRIUploadView.as_view(), name='mri-upload'),
]
