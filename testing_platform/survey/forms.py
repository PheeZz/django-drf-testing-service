# forms.py
from django import forms
from django.forms import inlineformset_factory

from .models import Question, Survey


class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ["name"]
        labels = {"name": "Название теста"}


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["question_text", "correct_answer"]
        labels = {"question_text": "Описание вопроса", "correct_answer": "Правильный ответ"}
        widgets = {"correct_answer": forms.RadioSelect(choices=((True, "Да"), (False, "Нет")))}


# exclude Delete checkbox
QuestionFormSet = inlineformset_factory(
    Survey, Question, form=QuestionForm, extra=5, can_delete=False
)
