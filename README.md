# Тестовое задание Django + DRF

## Как запустить

1. Склонировать репозиторий
2. Создать виртуальное окружение и установить зависимости
3. Прогнать миграции
4. Запустить сервер

```bash
git clone https://github.com/pheezz/django-drf-testing-service.git
cd django-drf-testing-service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Возможные варианты авторизации для реализации

- JWT
- Basic Auth

Для реализации JWT необходимо добавить табличку пользователей и токенов, а также добавить views для регистрации и авторизации. Пару access/refresh токенов можно хранить в куках. Refresh token хранить в базе в закодированном base64 виде. В случае реализации jwt пользователю не нужно будет вводить логин и пароль при каждом входе.

Для реализации Basic Auth необходимо добавить табличку пользователей и views для регистрации и авторизации. При каждом запросе пользователя необходимо передавать логин и пароль в заголовке Authorization. Как вариант можно сохранять сессию в базе данных или в кеше.

## Описание реализации

- В проекте два основных пакета: `survey` и `api.survey_api`.
- В `survey` находятся модели, views для веб интерфейса, urls, а также шаблоны. Данные агрегируются посредством API запросов к `survey_api` с помощью библиотеки requests.
- В `survey_api` находятся views для API, сериализаторы и urls.
- Также в пакете `survey_api` находится модуль `analytics.py`, который содержит функции сбора общей информации по пройденным опросам.

## API url endpoints

- `/api/v1/survey/` GET - список всех опросов
- `/api/v1/survey/` POST - создание нового опроса
- `/api/v1/survey/<int:survey_id>/questions/` GET - список вопросов для опроса
- `/api/v1/survey/<int:survey_id>/questions/` POST - создание нового вопроса для опроса
- `/api/v1/survey/<int:survey_id>/user_answers/` POST - ответы пользователя на вопросы опроса
- `/api/v1/survey/<int:survey_id>/analytics/` GET - аналитика по опросу
