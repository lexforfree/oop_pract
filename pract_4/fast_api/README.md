# Вариантность типов в FastAPI-сервисе

Тот же материал, что и в `mypy_examples/`, но на этот раз — в структуре
настоящего (хоть и маленького) веб-сервиса: приют для животных с API
на FastAPI, in-memory хранилищем и событиями. Протестировано и реально
работает (см. раздел "Проверено" внизу).

## Что где лежит

```
app/
  models.py       доменные классы Animal/Dog/Cat (dataclass, не pydantic)
  schemas.py      pydantic-схемы + ApiResponse[T_co] — ковариантная обёртка ответа
  repository.py   Repository[T] (инвариант) + ReadOnlyRepository[T_co] (ковариант)
  events.py       EventHandler[T_contra] (контравариант) + EventBus
  main.py         FastAPI-приложение, связывающее всё вместе
Dockerfile
docker-compose.yml
mypy.ini
requirements.txt
```

## Как каждый вид вариантности используется в реальном коде

| Где в коде | Вариантность | Зачем |
|---|---|---|
| `Repository[T]` | инвариант | основное хранилище — и пишет (`add`), и читает (`get`, `get_all`) |
| `ReadOnlyRepository[T_co]` | ковариант | `dog_repo.as_read_only()` и `cat_repo.as_read_only()` можно передать в одну и ту же функцию `_print_report`, типизированную по `Animal` |
| `EventHandler[T_contra]` | контравариант | один `AnimalRegisteredLogger` (`EventHandler[Animal]`) обрабатывает и регистрацию собак, и кошек — не нужно писать по обработчику на каждый тип |
| `ApiResponse[T_co]` | ковариант | единая обёртка ответа API, переиспользуемая для любого типа данных в `data` |

## Запуск с Docker (основной способ для занятия)

```bash
docker compose up --build
```

Открыть в браузере: `http://localhost:8000/docs` — там интерактивная
документация Swagger, можно прямо из браузера дёргать `/dogs`, `/cats`,
`/debug/variance-report` и видеть логи событий в терминале, где запущен
`docker compose up` (там же видно вывод `_print_report`).

### Отдельная проверка типов через mypy (как в CI)

```bash
docker compose --profile check run --rm mypy
```

Эта команда не поднимает сервер — только проверяет типы и завершается,
печатая `Success: no issues found in 6 source files`. Именно так
статическая проверка обычно встраивается в пайплайн перед деплоем.

## Запуск без Docker (если нужно быстро, для отладки)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

uvicorn app.main:app --reload
mypy app --config-file mypy.ini
```

## Сценарий для демонстрации на занятии

1. `docker compose up --build`, открыть `/docs`
2. `POST /dogs` с телом `{"name": "Рекс", "breed": "Лабрадор"}` — в терминале
   сразу видно `[event] зарегистрировано животное: Рекс` — это сработал
   контравариантный `EventHandler[Animal]` на объекте `Dog`
3. То же самое с `POST /cats` — **тот же самый** обработчик, без единой
   строчки дополнительного кода под кошек
4. `GET /debug/variance-report` — показывает, что одна функция
   `_print_report(repo: ReadOnlyRepository[Animal])` одинаково работает
   и с `ReadOnlyRepository[Dog]`, и с `ReadOnlyRepository[Cat]`
5. `docker compose --profile check run --rm mypy` — показать, что весь
   проект проходит статическую проверку типов целиком, 0 ошибок

## Проверено

Код в этом проекте реально запускался и проверялся перед тем, как
попасть в материалы занятия:
- `mypy app --config-file mypy.ini` → `Success: no issues found in 6 source files`
- Полный прогон через `TestClient` (создание/чтение собак и кошек,
  404 на несуществующий id, `/debug/variance-report`, `/health`) —
  все эндпоинты отработали корректно, события залогированы.

## Идея для самостоятельного расширения (не обязательно для занятия)

Попробуйте сознательно "сломать" типизацию — например, объявить
`ReadOnlyRepository[T_co]` с дополнительным методом `add(self, item: T_co)`
— и посмотреть, как mypy откажется принимать такой класс ещё на этапе
его объявления, даже до того, как появится хоть одна точка использования.