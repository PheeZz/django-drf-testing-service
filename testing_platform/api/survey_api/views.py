from django.db import models
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from testing_platform.survey.models import Question, Survey, UserAnswer

from .analytics import SurveyAnalyticsCollector
from .serializers import AnswersListSerializer, QuestionSerializer, SurveySerializer
from django.http import HttpRequest
from rest_framework.serializers import ModelSerializer


class SurveyAPIList(generics.ListCreateAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer


class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_queryset(self):
        survey_id = self.kwargs["survey_id"]
        return Question.objects.filter(survey=survey_id)

    def perform_create(self, serializer: ModelSerializer):
        survey_id = self.kwargs["survey_id"]
        survey = Survey.objects.get(id=survey_id)
        serializer.save(survey=survey)


class UserAnswerList(generics.CreateAPIView):
    queryset = UserAnswer.objects.all()
    serializer_class = AnswersListSerializer

    def perform_create(self, serializer: ModelSerializer):
        answers = serializer.validated_data["answers"]
        max_user_id = UserAnswer.objects.all().aggregate(models.Max("user_id"))
        user_id = max_user_id["user_id__max"] + 1 if max_user_id["user_id__max"] else 1

        for answer in answers:
            UserAnswer.objects.create(user_id=user_id, **answer)


class SurveyAnalytics(APIView):

    def get(self, request: HttpRequest, survey_id: int):
        pass_count = SurveyAnalyticsCollector.get_pass_count(survey_id)
        success_rate = SurveyAnalyticsCollector.calculate_success_rate_percentage(survey_id)
        hardest_question = SurveyAnalyticsCollector.calculate_hardest_question(survey_id)
        return Response(
            {
                "pass_count": pass_count,
                "success_rate": success_rate,
                "hardest_question": hardest_question,
            }
        )
