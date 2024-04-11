from django.urls import path

from .views import (create_survey, submit_answers, survey_analytics,
                    survey_list, survey_questions)

urlpatterns = [
    path("", survey_list, name="survey_list"),
    path("<int:survey_id>/questions/", survey_questions, name="survey_questions"),
    path("<int:survey_id>/submit_answers/", submit_answers, name="submit_answers"),
    path("<int:survey_id>/analytics", survey_analytics, name="survey_analytics"),
    path("create_survey/", create_survey, name="create_survey"),
]
