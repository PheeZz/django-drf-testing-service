from django.urls import path

from .views import QuestionList, SurveyAnalytics, SurveyAPIList, UserAnswerList

urlpatterns = [
    path("", SurveyAPIList.as_view(), name="survey"),
    path("<int:survey_id>/questions/", QuestionList.as_view(), name="questions"),
    path("<int:survey_id>/user_answers/", UserAnswerList.as_view(), name="user_answers"),
    path("<int:survey_id>/analytics/", SurveyAnalytics.as_view(), name="analytics"),
]
