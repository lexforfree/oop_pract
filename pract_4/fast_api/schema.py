"""
Pydantic-схемы запросов/ответов.

ApiResponse[T_co] — ковариантная generic-обёртка ответа API. Используем
TypeVar("T_co", covariant=True) по тем же причинам, что и в mypy_examples:
обёртка только ОТДАЁТ данные наружу (поле data только для чтения по смыслу
использования в ответах), поэтому ApiResponse[DogOut] можно статически
рассматривать как частный случай ApiResponse[AnimalOut].
"""
from __future__ import annotations

from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T_co = TypeVar("T_co", covariant=True)


class AnimalOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    created_at: datetime


class DogOut(AnimalOut):
    breed: str


class CatOut(AnimalOut):
    indoor: bool


class DogCreate(BaseModel):
    name: str
    breed: str = "Дворняга"


class CatCreate(BaseModel):
    name: str
    indoor: bool = True


class ApiResponse(BaseModel, Generic[T_co]):
    """Единая обёртка ответа для всех эндпоинтов — и для одного объекта,
    и для списка (см. main.py, где T_co подставляется и как DogOut,
    и как list[DogOut])."""

    data: T_co
    message: str = "ok"