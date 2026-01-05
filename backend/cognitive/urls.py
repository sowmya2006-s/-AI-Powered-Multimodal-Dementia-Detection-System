from django.urls import path
from .views import StartTest, GenerateRound, SubmitAnswer, FinishTest

urlpatterns = [
    path('start/', StartTest.as_view(), name='start_test'),
    path('generate-round/', GenerateRound.as_view(), name='generate_round'),
    path('submit-answer/', SubmitAnswer.as_view(), name='submit_answer'),
    path('finish/', FinishTest.as_view(), name='finish_test'),
]
