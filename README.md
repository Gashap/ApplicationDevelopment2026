# Habit Tracker API — OpenAPI 3.0 + python-flask кодоген

**Зачем этот API:** чтобы пользователь мог заводить свои привычки (читать, бегать, пить воду…), смотреть их список, менять и удалять — а клиент (мобилка/веб) работал по заранее согласованному контракту, не зная, как устроено хранилище.

## Что где лежит

| Путь | Что это |
|------|---------|
| [`api.yaml`](api.yaml) | Спецификация OpenAPI 3.0.3 — источник правды (API first) |
| [`service/`](service) | Сервис, сгенерированный `openapi-generator-cli` (генератор **python-flask**, Flask + Connexion) и доработанный руками |
| `README.md` | Этот файл: как делали |

## Часть 1 · Спека (`api.yaml`)

5 операций, 4 разных глагола:

| Глагол | Путь | summary | Успех | Ошибки |
|--------|------|---------|-------|--------|
| GET    | `/api/habits` | Список привычек текущего пользователя | 200 `HabitPage` | 400, 401 |
| POST   | `/api/habits` | Создать привычку | 201 `HabitView` + `Location` | 400, 401 |
| GET    | `/api/habits/{habitId}` | Получить одну привычку | 200 `HabitView` | 401, 403, 404 |
| PATCH  | `/api/habits/{habitId}` | Изменить часть полей привычки | 200 `HabitView` | 400, 401, 403, 404 |
| DELETE | `/api/habits/{habitId}` | Удалить привычку | 204 (без тела) | 401, 403, 404 |

- **Параметры:** `habitId` (path), `status` / `limit` / `offset` (query), тела запросов — `NewHabitRequest`, `HabitPatchRequest`.
- **Успешные коды** подобраны по смыслу операции: 200 — данные отданы, 201 — ресурс создан, 204 — удалено, тела нет.
- **401 vs 403:** `401 Unauthorized` — «не знаю, кто ты» (нет токена / токен неизвестен); `403 Forbidden` — «знаю, кто ты, но нельзя» (привычка принадлежит другому пользователю). `404` — привычки с таким id нет.
- **DTO в `components/schemas`:** `NewHabitRequest`, `HabitPatchRequest`, `HabitView`, `HabitPage`, `ApiError`, enum'ы `Frequency`, `HabitStatus`. Внутренняя сущность (`HabitEntity` в [`service/habit_tracker/store.py`](service/habit_tracker/store.py) с `owner_id`, `reminder_job_id`) наружу **не едет** — контроллер переводит её в `HabitView`, а `additionalProperties: false` не даёт клиенту прислать лишние поля (например, `ownerId`).
- Спека валидна: `openapi-generator-cli validate -i api.yaml` → `No validation issues detected.` (можно также вставить в editor.swagger.io).

## Часть 2 · Кодоген

```bash
# openapi-generator-cli 7.10.0 (нужна Java 11+)
curl -Lo openapi-generator-cli.jar \
  https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/7.10.0/openapi-generator-cli-7.10.0.jar

java -jar openapi-generator-cli.jar validate -i api.yaml
java -jar openapi-generator-cli.jar generate -i api.yaml -g python-flask -o service \
  --additional-properties=packageName=habit_tracker
```

(то же самое, что `openapi-generator-cli generate -i api.yaml -g python-flask -o service`, если генератор установлен через npm/brew.)

Генератор создал: модели DTO (`service/habit_tracker/models/`), контроллеры-заглушки с `return 'do some magic!'`, `security_controller.py`, `__main__.py` (Connexion поднимает Flask и сам валидирует запросы по спеке), Swagger UI, Dockerfile, тесты-заготовки. Нетронутый результат генерации — отдельный коммит в истории, поэтому все ручные правки видны в диффе следующих коммитов.

### Запуск

```bash
cd service
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt -r test-requirements.txt
python -m habit_tracker          # http://localhost:8080
                                 # Swagger UI: http://localhost:8080/ui/
python -m pytest -q              # 7 тестов на все эндпоинты и коды ответов
```

Демо-токены: `Bearer alice-token`, `Bearer bob-token`. Данные хранятся в памяти и пропадают после перезапуска.

```bash
curl -i http://localhost:8080/api/habits                              # 401
curl -i -X POST http://localhost:8080/api/habits \
  -H "Authorization: Bearer alice-token" -H "Content-Type: application/json" \
  -d '{"title":"Читать 20 минут","frequency":"WEEKLY","targetPerWeek":5}'  # 201
curl -i http://localhost:8080/api/habits/1 -H "Authorization: Bearer bob-token"   # 403
curl -i -X PATCH http://localhost:8080/api/habits/1 \
  -H "Authorization: Bearer alice-token" -H "Content-Type: application/json" \
  -d '{"status":"ARCHIVED"}'                                          # 200
curl -i -X DELETE http://localhost:8080/api/habits/1 -H "Authorization: Bearer alice-token"  # 204
curl -i -X DELETE http://localhost:8080/api/habits/1 -H "Authorization: Bearer alice-token"  # 404
```

## Часть 3 · Как делали

**С агентом.** Проект сначала был реализован на C# (ASP.NET Core Minimal API) по той же спеке, затем переписан на Python через кодоген. Переписывание делал агент **Devin (Cognition AI)**: перенёс `api.yaml` в корень, запустил `openapi-generator-cli` с генератором `python-flask`, дописал логику и тесты, удалил C#-код.

Итоговый промт агенту:

> Адаптируй проект под задание и перепиши его под Python. Текст задания: Спроектировать API в Swagger-стиле и сгенерировать по нему код… (далее полный текст задания: спека api.yaml OpenAPI 3.0 с 4–5 эндпоинтами под разные глаголы, кодоген `openapi-generator-cli generate -i api.yaml -g python-flask -o service`, README «как делали»).

### Что поправили руками после генерации

1. **`api.yaml`: добавлен `x-body-name`** у обоих `requestBody`. Без него Connexion передаёт тело в аргумент `body`, а сгенерированные контроллеры ждут `new_habit_request` / `habit_patch_request` → `TypeError` и 500 на POST/PATCH. После правки сервис перегенерирован (изменился только `service/habit_tracker/openapi/openapi.yaml`).
2. **`controllers/habits_controller.py`:** вместо `'do some magic!'` — реальная логика 5 операций: фильтр/пагинация списка, `201 + Location` на создание, частичное обновление, `204` на удаление, проверки 404 → 403. Убран сгенерированный баг в `list_habits` (`HabitStatus.from_dict(request.get_json())` для query-параметра).
3. **`store.py` (новый):** внутренняя `HabitEntity` + потокобезопасное in-memory хранилище; маппинг Entity → DTO `HabitView`, чтобы `owner_id` и служебные поля не уходили наружу.
4. **`controllers/security_controller.py`:** заглушка всегда пускала любого (`{'uid': 'user_id'}`); теперь токен проверяется по словарю демо-пользователей, неизвестный токен → `None` → Connexion отвечает 401.
5. **`errors.py` (новый) + `__main__.py`:** Connexion по умолчанию отдаёт ошибки в формате `application/problem+json`; добавлены обработчики, чтобы 400/401/404 возвращались в форме DTO `ApiError {"message": ...}`, как описано в спеке. Включён `JSON_AS_ASCII = False`, чтобы кириллица не экранировалась.
6. **Тесты:** заготовки (которые падали) заменены на 7 тестов по всем эндпоинтам и кодам 200/201/204/400/401/403/404; в тестах включён `validate_responses=True` — ответы сервиса сверяются со спекой.
7. **`.openapi-generator-ignore`:** добавлены ручные файлы, чтобы повторный `generate` их не затёр.
