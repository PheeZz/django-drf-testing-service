# Тестовое задание Django + DRF

## Описание

Необходимо разработать сервис для формирования и прохождения тестов. Тест должен содержать набор вопросов с указанием правильного ответа (всегда используются варианты ответов - Да / Нет). По результатам тестирования должна быть возможность получить общую информацию о следующих показателях (о тесте):

- Количество прохождений теста;
- Процент успешного прохождения (если кол-во правильных ответов 50% и выше);
- Самый сложный вопрос.

## Доп. информация

- Авторизация не нужна (но нужно предложение какие варианты авторизации можно использовать);
- Использовать встроенный функционал sqlite3;
- Для реализации необходимо использовать Django + DRF;
- Для формирования итогового отчета по тесту должен использоваться класс с отдельными методами (по каждой аналитике);
- Итоговый сервис должен быть загружен в github с README (краткое описание реализации) и публичной ссылкой;
- Код и нэйминг должен быть чист и понятен
- Один из пункт тестового задания - будет сформирован pull-request, который необходимо будет отработать.
- Должно использоваться виртуальное окружение (python3.11) c сохраненными зависимостями в requirements.txt
