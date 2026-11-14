# Habit Tracker API

**Зачем этот API:** чтобы пользователь мог заводить свои привычки, смотреть их список, менять и удалять, а клиент работал по заранее согласованному контракту.

## Что в репозитории

- [`api.yaml`](api.yaml) — спецификация OpenAPI 3.0.3
- [`service/`](service) — сервис, сгенерированный `openapi-generator-cli` (генератор `python-flask`)
- `README.md` — как делали

## Спека

| Глагол | Путь | summary | Ответы |
|--------|------|---------|--------|
| GET    | `/api/habits` | Список привычек текущего пользователя | 200, 400, 401 |
| POST   | `/api/habits` | Создать привычку | 201, 400, 401 |
| GET    | `/api/habits/{habitId}` | Получить одну привычку | 200, 401, 403, 404 |
| PATCH  | `/api/habits/{habitId}` | Изменить часть полей привычки | 200, 400, 401, 403, 404 |
| DELETE | `/api/habits/{habitId}` | Удалить привычку | 204, 401, 403, 404 |

401 — «не знаю, кто ты» (нет токена), 403 — «знаю, кто ты, но нельзя» (привычка чужая), 404 — привычки нет.
DTO описаны в `components/schemas` (`NewHabitRequest`, `HabitPatchRequest`, `HabitView`, `HabitPage`, `ApiError`), внутренние поля (`ownerId` и т.п.) в них не входят.

## Кодоген

```bash
java -jar openapi-generator-cli.jar validate -i api.yaml        # No validation issues detected.
java -jar openapi-generator-cli.jar generate -i api.yaml -g python-flask -o service \
  --additional-properties=packageName=habit_tracker              # openapi-generator-cli 7.10.0
```

Запуск:

```bash
cd service
pip install -r requirements.txt
python -m habit_tracker     # Swagger UI: http://localhost:8080/ui/
curl -H "Authorization: Bearer any-token" "http://localhost:8080/api/habits?status=ACTIVE"
```

## Как делали

С агентом: **Devin (Cognition AI)**. Итоговый промт — текст задания с просьбой переписать проект на Python:

> Адаптируй проект под задание и перепиши его под Python. Текст задания: Спроектировать API в Swagger-стиле и сгенерировать по нему код… (далее полный текст задания).

Что поправили руками:

1. В `api.yaml` добавлен `x-body-name` для тел POST и PATCH: без него сгенерированные контроллеры падали с `TypeError`.
2. `list_habits` в `service/habit_tracker/controllers/habits_controller.py`: вместо заглушки `'do some magic!'` возвращает список демо-привычек с фильтром `status` и `limit`/`offset`. Заодно исправлен сгенерированный тест для этого метода. Остальные эндпоинты оставлены заглушками генератора.
