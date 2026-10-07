"""
Repository (инвариантен) — основное хранилище, с ним работают эндпоинты
на запись и точечное чтение.

ReadOnlyRepository (ковариантен) — безопасный "снимок" для отчётных
сценариев: можно передавать ReadOnlyRepository[Dog] и ReadOnlyRepository[Cat]
в одну и ту же функцию, типизированную как ReadOnlyRepository[Animal].
"""
from __future__ import annotations

from typing import Dict, Generic, List, Optional, TypeVar

from models import Animal

T = TypeVar("T", bound=Animal)
T_co = TypeVar("T_co", bound=Animal, covariant=True)


class Repository(Generic[T]):
    """И пишет (add), и читает (get/get_all) -> инвариантность."""

    def __init__(self) -> None:
        self._items: Dict[int, T] = {}
        self._next_id: int = 1

    def add(self, item: T) -> T:
        item.id = self._next_id
        self._items[self._next_id] = item
        self._next_id += 1
        return item

    def get(self, item_id: int) -> Optional[T]:
        return self._items.get(item_id)

    def get_all(self) -> List[T]:
        return list(self._items.values())

    def as_read_only(self) -> "ReadOnlyRepository[T]":
        """Возвращает СНИМОК данных на текущий момент — не прокси
        над мутабельным хранилищем (так же, как ReadOnlyStack
        в mypy_examples/containers.py — это важно для безопасности
        самой ковариантности)."""
        return ReadOnlyRepository(self.get_all())


class ReadOnlyRepository(Generic[T_co]):
    """Только читает (get/get_all) -> можно сделать ковариантным."""

    def __init__(self, items: List[T_co]) -> None:
        self._items: List[T_co] = list(items)

    def get_all(self) -> List[T_co]:
        return list(self._items)

    def find(self, item_id: int) -> Optional[T_co]:
        for item in self._items:
            if item.id == item_id:
                return item
        return None