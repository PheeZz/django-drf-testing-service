from rest_framework import serializers

from testing_platform.survey.models import Survey, Question, UserAnswer


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class UserAnswerSerializer(serializers.Serializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    user_answer = serializers.BooleanField()


class AnswersListSerializer(serializers.Serializer):
    answers = UserAnswerSerializer(many=True)

    def create(self, validated_data, user_id: int):
        answers = validated_data.pop("answers")
        for answer in answers:
            UserAnswer.objects.create(user_id=user_id, **answer)
        return validated_data


class AnalyticsSerializer(serializers.Serializer):
    survey_id = serializers.IntegerField()
    pass_count = serializers.IntegerField()
    success_rate = serializers.FloatField()
    hardest_question = serializers.CharField()
