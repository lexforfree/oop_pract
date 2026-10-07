"""
FastAPI-приложение демонстрирует вариантность типов не в вакууме,
а в структуре, которую вы реально могли бы написать в проекте:

    Repository[T]            — инвариантное хранилище (write + read)
    ReadOnlyRepository[T_co]  — ковариантный "снимок" для отчётов
    EventHandler[T_contra]    — контравариантный обработчик событий

Запуск без Docker:
    uvicorn main:app --reload
    открыть http://127.0.0.1:8000/docs

Запуск с Docker — см. README.md в корне проекта.
"""
from __future__ import annotations

from typing import List

from fastapi import FastAPI, HTTPException

from events import AnimalRegisteredLogger, EventBus
from models import Cat, Dog
from repository import ReadOnlyRepository, Repository
from schema import ApiResponse, CatCreate, CatOut, DogCreate, DogOut

app = FastAPI(
    title="Variance Demo API",
    description="Инвариантность / ковариантность / контравариантность на примере приюта для животных",
    version="1.0.0",
)

dog_repo: Repository[Dog] = Repository()
cat_repo: Repository[Cat] = Repository()

event_bus = EventBus()
event_bus.subscribe(AnimalRegisteredLogger())  # один обработчик на всех животных


def _print_report(label: str, repo: "ReadOnlyRepository") -> None:
    """
    Единственная функция для вывода отчёта по ЛЮБОМУ типу животных.
    Аннотация параметра — ReadOnlyRepository[Animal] (см. вызовы ниже) —
    а передаём мы туда и ReadOnlyRepository[Dog], и ReadOnlyRepository[Cat].
    Это и есть ковариантность в действии, не на игрушечном, а на рабочем коде.
    """
    print(f"--- {label} ---")
    for animal in repo.get_all():
        print(" -", animal.name)


@app.post("/dogs", response_model=ApiResponse[DogOut])
def create_dog(payload: DogCreate) -> ApiResponse[DogOut]:
    dog = dog_repo.add(Dog(id=0, name=payload.name, breed=payload.breed))
    event_bus.publish(dog)  # EventHandler[Animal] обработал Dog благодаря contravariance
    return ApiResponse(data=DogOut.model_validate(dog))


@app.get("/dogs", response_model=ApiResponse[List[DogOut]])
def list_dogs() -> ApiResponse[List[DogOut]]:
    read_only: ReadOnlyRepository[Dog] = dog_repo.as_read_only()
    items = [DogOut.model_validate(d) for d in read_only.get_all()]
    return ApiResponse(data=items)


@app.get("/dogs/{dog_id}", response_model=ApiResponse[DogOut])
def get_dog(dog_id: int) -> ApiResponse[DogOut]:
    dog = dog_repo.get(dog_id)
    if dog is None:
        raise HTTPException(status_code=404, detail="Dog not found")
    return ApiResponse(data=DogOut.model_validate(dog))


@app.post("/cats", response_model=ApiResponse[CatOut])
def create_cat(payload: CatCreate) -> ApiResponse[CatOut]:
    cat = cat_repo.add(Cat(id=0, name=payload.name, indoor=payload.indoor))
    event_bus.publish(cat)
    return ApiResponse(data=CatOut.model_validate(cat))


@app.get("/cats", response_model=ApiResponse[List[CatOut]])
def list_cats() -> ApiResponse[List[CatOut]]:
    read_only: ReadOnlyRepository[Cat] = cat_repo.as_read_only()
    items = [CatOut.model_validate(c) for c in read_only.get_all()]
    return ApiResponse(data=items)


@app.get("/cats/{cat_id}", response_model=ApiResponse[CatOut])
def get_cat(cat_id: int) -> ApiResponse[CatOut]:
    cat = cat_repo.get(cat_id)
    if cat is None:
        raise HTTPException(status_code=404, detail="Cat not found")
    return ApiResponse(data=CatOut.model_validate(cat))


@app.get("/debug/variance-report")
def variance_report() -> dict[str, list[str]]:
    """
    Демонстрационный эндпоинт: вызывает ОДНУ И ТУ ЖЕ функцию _print_report
    и для собак, и для кошек — наглядная ковариантность вживую, плюс
    видно в docker logs / консоли при вызове.
    """
    dog_view = dog_repo.as_read_only()
    cat_view = cat_repo.as_read_only()
    _print_report("Dogs", dog_view)
    _print_report("Cats", cat_view)
    return {
        "dogs": [d.name for d in dog_view.get_all()],
        "cats": [c.name for c in cat_view.get_all()],
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}