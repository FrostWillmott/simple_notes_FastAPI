# Notes CRUD API

Простое CRUD API для управления заметками на FastAPI.

## Установка
```bash
uv sync
```

## Запуск
```bash
uv run uvicorn main:app --reload
```

## API Documentation

После запуска откройте: http://127.0.0.1:8000/docs

## Эндпоинты

- POST /notes/ - создать заметку
- GET /notes/ - получить все заметки
- GET /notes/{id} - получить заметку по ID
- PUT /notes/{id} - обновить заметку
- DELETE /notes/{id} - удалить заметку
