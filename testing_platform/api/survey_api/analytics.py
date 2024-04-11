import math

from django.db import models

from testing_platform.survey.models import Question, UserAnswer


class SurveyAnalyticsCollector:

    @classmethod
    def _get_users_ids_finished_survey(cls, survey_id: int) -> list[int]:
        return UserAnswer.objects.filter(question__survey_id=survey_id).values("user_id").distinct()

    @classmethod
    def get_pass_count(cls, survey_id: int) -> int:
        return len(cls._get_users_ids_finished_survey(survey_id)) or 0

    @classmethod
    def calculate_success_rate_percentage(cls, survey_id: int) -> float:
        users_ids_finished_survey = cls._get_users_ids_finished_survey(survey_id)
        if not users_ids_finished_survey:
            return 0.0
        questions_count = Question.objects.filter(survey_id=survey_id).count()
        users_with_correct_answers_bigger_than_half = 0

        for user in users_ids_finished_survey:
            user_answers = UserAnswer.objects.filter(user_id=user["user_id"])
            correct_answers = user_answers.filter(
                user_answer=models.F("question__correct_answer")
            ).count()
            if correct_answers > questions_count / 2:
                users_with_correct_answers_bigger_than_half += 1

        return round(
            users_with_correct_answers_bigger_than_half / len(users_ids_finished_survey) * 100,
            3,
        )

    @classmethod
    def calculate_hardest_question(cls, survey_id: int) -> str:
        questions = Question.objects.filter(survey_id=survey_id)
        if not cls.get_pass_count(survey_id):
            return "Пока никто не прошел этот тест"
        hardest_question = None
        hardest_question_correct_answers = math.inf
        for question in questions:
            correct_answers = UserAnswer.objects.filter(
                question_id=question.id, user_answer=question.correct_answer
            ).count()
            if correct_answers < hardest_question_correct_answers:
                hardest_question = question
                hardest_question_correct_answers = correct_answers
        return hardest_question.question_text
