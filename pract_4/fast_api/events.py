"""
Repository (инвариантен) — основное хранилище, с ним работают эндпоинты
на запись и точечное чтение.

ReadOnlyRepository (ковариантен) — безопасный "снимок" для отчётных
сценариев: можно передавать ReadOnlyRepository[Dog] и ReadOnlyRepository[Cat]
в одну и ту же функцию, типизированную как ReadOnlyRepository[Animal].
"""
from __future__ import annotations

from typing import Protocol, TypeVar

from models import Animal

T_contra = TypeVar("T_contra", contravariant=True)


class EventHandler(Protocol[T_contra]):
    def handle(self, item: T_contra) -> None:
        ...


class AnimalRegisteredLogger:
    """One handler for many animal types: contravariance in action."""

    def handle(self, animal: Animal) -> None:
        print(f"[event] зарегистрировано животное: {animal.name}")


class EventBus:
    def __init__(self) -> None:
        self._handlers: list[EventHandler[Animal]] = []

    def subscribe(self, handler: EventHandler[Animal]) -> None:
        self._handlers.append(handler)

    def publish(self, animal: Animal) -> None:
        for handler in self._handlers:
            handler.handle(animal)