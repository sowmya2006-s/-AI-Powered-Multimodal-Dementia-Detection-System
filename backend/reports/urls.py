from django.urls import path
from .views import FusionReportView

urlpatterns = [
    path('generate-fusion/', FusionReportView.as_view(), name='generate_fusion'),
]
