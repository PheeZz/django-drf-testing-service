import requests
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render

from testing_platform.constants import BASE_API_URL

from .forms import QuestionFormSet, SurveyForm


def survey_list(request: HttpRequest):
    response = requests.get(f"{BASE_API_URL}/survey/")
    if response.status_code == 200:
        surveys = response.json()
    else:
        surveys = []

    return render(request, "survey_list.html", {"surveys": surveys})


def survey_questions(request: HttpRequest, survey_id):
    response = requests.get(f"{BASE_API_URL}/survey/{survey_id}/questions/")
    if response.status_code == 200:
        questions = response.json()
    else:
        questions = []
    survey_name = request.GET.get("name", "")
    return render(
        request,
        "survey_questions.html",
        {
            "questions": questions,
            "survey_name": survey_name,
            "survey_id": survey_id,
        },
    )


def submit_answers(request: HttpRequest, survey_id: int):
    if request.method == "POST":
        answers = []
        for key, value in request.POST.items():
            if key.startswith("answer"):
                question_id = key.replace("answer_", "")
                answer = {
                    "question": int(question_id),
                    "user_answer": value == "true",
                }
                answers.append(answer)

        payload = {"answers": answers}
        response = requests.post(f"{BASE_API_URL}/survey/{survey_id}/user_answers/", json=payload)
        survey_name = request.GET.get("name")
        if response.status_code == 201:
            return render(
                request,
                "survey_submitted.html",
                {
                    "survey_name": survey_name,
                },
            )
        else:
            return JsonResponse({"message": "Failed to submit answers."}, status=400)

    else:
        return JsonResponse({"message": "Method not allowed."}, status=405)


def survey_analytics(request: HttpRequest, survey_id: int):
    response = requests.get(f"{BASE_API_URL}/survey/{survey_id}/analytics/")
    if response.status_code == 200:
        analytics = response.json()
    else:
        analytics = {}
    survey_name = request.GET.get("name")
    return render(
        request,
        "survey_analytics.html",
        {
            "analytics": analytics,
            "survey_name": survey_name,
        },
    )


def create_survey(request: HttpRequest):
    if request.method == "POST":
        survey_form = SurveyForm(request.POST)
        question_formset = QuestionFormSet(request.POST)
        if survey_form.is_valid() and question_formset.is_valid():
            survey_name = survey_form.cleaned_data["name"]
            response = requests.post(f"{BASE_API_URL}/survey/", json={"name": survey_name})

            if response.status_code == 201:
                survey_id = response.json()["id"]
                for form in question_formset:
                    question_text = form.cleaned_data["question_text"]
                    correct_answer = form.cleaned_data["correct_answer"]
                    response = requests.post(
                        f"{BASE_API_URL}/survey/{survey_id}/questions/",
                        json={
                            "survey": survey_id,
                            "question_text": question_text,
                            "correct_answer": correct_answer,
                        },
                    )
                    if response.status_code != 201:
                        error_message = "Ошибка. Не удалось создать вопросы"
                        return render(
                            request,
                            "create_survey.html",
                            {
                                "survey_form": survey_form,
                                "question_formset": question_formset,
                                "error_message": error_message,
                            },
                        )
                return survey_list(request)

            else:
                error_message = "Ошибка, не удалось создать тест"
                return render(
                    request,
                    "create_survey.html",
                    {
                        "survey_form": survey_form,
                        "question_formset": question_formset,
                        "error_message": error_message,
                    },
                )
    else:
        # get request
        survey_form = SurveyForm()
        question_formset = QuestionFormSet()
    return render(
        request,
        "create_survey.html",
        {"survey_form": survey_form, "question_formset": question_formset},
    )
