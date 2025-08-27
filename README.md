# School Bot REST API

RESTful API сервер для управления учебным процессом, интегрированный с Telegram ботом. Сервер предоставляет endpoints для управления пользователями, группами, домашними заданиями и вложениями.

## 🚀 Технологии

- **FastAPI** - современный, быстрый веб-фреймворк для построения API
- **SQLAlchemy** - ORM для работы с базой данных
- **SQLite** - база данных (можно легко заменить на PostgreSQL/MySQL)
- **Pydantic** - валидация данных и сериализация
- **Uvicorn** - ASGI сервер для запуска приложения

## 📁 Структура проекта
rest_server/
├── app/
│ ├── models/ # Модели базы данных
│ │ ├── user.py
│ │ ├── group.py
│ │ ├── homework.py
│ │ ├── user_group.py
│ │ ├── attachment.py
│ │ └── init.py
│ ├── schemas/ # Pydantic схемы
│ │ ├── user.py
│ │ ├── group.py
│ │ ├── homework.py
│ │ ├── user_group.py
│ │ ├── attachment.py
│ │ └── init.py
│ ├── routes/ # Маршруты API
│ │ ├── users.py
│ │ ├── groups.py
│ │ ├── homeworks.py
│ │ ├── user_groups.py
│ │ ├── attachments.py
│ │ └── init.py
│ ├── database.py # Настройка базы данных
│ ├── main.py # Основное приложение
│ └── init.py
├── school_bot.db # База данных SQLite
├── run.py # Скрипт запуска
└── README.md


## 🛠️ Установка и запуск

### Предварительные требования

- Python 3.8+
- pip (менеджер пакетов Python)

### Установка зависимостей

```bash
pip install fastapi uvicorn sqlalchemy pydantic

Запуск сервера
# Запуск development сервера
uvicorn run:app --reload --host 0.0.0.0 --port 8000

# Или через run.py
python run.py

Сервер будет доступен по адресу: http://localhost:8000

📚 API Endpoints
Пользователи (/users)
POST /users/ - Создать нового пользователя

GET /users/ - Получить список всех пользователей

GET /users/{user_id} - Получить пользователя по ID

GET /users/telegram/{telegram_id} - Получить пользователя по Telegram ID

PUT /users/{user_id} - Обновить данные пользователя

DELETE /users/{user_id} - Удалить пользователя

Группы (/groups)
POST /groups/ - Создать новую группу

GET /groups/ - Получить список всех групп

GET /groups/{group_id} - Получить группу по ID

PUT /groups/{group_id} - Обновить данные группы

DELETE /groups/{group_id} - Удалить группу

Связи пользователей и групп (/user-groups)
POST /user-groups/ - Добавить пользователя в группу

GET /user-groups/ - Получить все связи

GET /user-groups/user/{user_id} - Получить группы пользователя

GET /user-groups/group/{group_id} - Получить пользователей группы

GET /user-groups/{user_id}/{group_id} - Получить конкретную связь

PUT /user-groups/{user_id}/{group_id} - Изменить роль пользователя

DELETE /user-groups/{user_id}/{group_id} - Удалить пользователя из группы

Домашние задания (/homeworks)
POST /homeworks/ - Создать новое домашнее задание

GET /homeworks/ - Получить список всех заданий

GET /homeworks/{homework_id} - Получить задание по ID

GET /homeworks/group/{group_id} - Получить задания группы

PUT /homeworks/{homework_id} - Обновить задание

DELETE /homeworks/{homework_id} - Удалить задание

Вложения (/attachments)
POST /attachments/ - Создать вложение

GET /attachments/ - Получить список вложений

GET /attachments/{attachment_id} - Получить вложение по ID

GET /attachments/homework/{homework_id} - Получить вложения задания

PUT /attachments/{attachment_id} - Обновить информацию о вложении

DELETE /attachments/{attachment_id} - Удалить вложение

📖 Документация API
После запуска сервера доступна автоматическая документация:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc