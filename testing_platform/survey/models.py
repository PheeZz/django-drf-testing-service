from django.db import models

# Create your models here.


class Survey(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=256)
    correct_answer = models.BooleanField()

    def __str__(self):
        return self.question_text


class UserAnswer(models.Model):
    user_id = models.IntegerField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answer = models.BooleanField()

    def __str__(self):
        return self.user_answer
