"""
Обобщённые контейнеры для демонстрации вариантности типов.

Это "библиотечный" код: сюда вынесены generic-классы,
а примеры их использования - в соседних demo_*.py файлах.

Три TypeVar ниже - это буквально три темы сегодняшнего занятия:
    T         - инвариантен (поведение по умолчанию, без флагов)
    T_co      - ковариантен (covariant=True)
    T_contra  - контравариантен (contravariant=True)
"""
from __future__ import annotations

from typing import Generic, List, TypeVar

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)
T_contra = TypeVar("T_contra", contravariant=True)


class Stack(Generic[T]):
    """
    И читает (pop), и пишет (push) -> ТОЛЬКО инвариантность.

    Попробуйте поменять Generic[T] на Generic[T_co] в этом классе
    и запустить mypy - он сам откажется компилировать push(),
    потому что T_co используется в позиции параметра (запись).
    Это и есть механическая причина, почему inv/co/contra нельзя
    выбирать произвольно - компилятор типов следит за этим сам.
    """

    def __init__(self) -> None:
        self._items: List[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

    def snapshot(self) -> List[T]:
        """Копия содержимого - используется, когда нужно отдать данные наружу."""
        return list(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def __bool__(self) -> bool:
        return bool(self._items)


class ReadOnlyStack(Generic[T_co]):
    """
    Только читает (peek/all), никогда не пишет -> можно сделать
    ковариантным: ReadOnlyStack[Dog] безопасно использовать там, где
    ожидается ReadOnlyStack[Animal] (но не наоборот - см. demo_covariant_fail.py).
    """

    def __init__(self, items: List[T_co]) -> None:
        self._items: List[T_co] = list(items)

    def peek(self) -> T_co:
        return self._items[-1]

    def all(self) -> List[T_co]:
        return list(self._items)

    def __len__(self) -> int:
        return len(self._items)


class Handler(Generic[T_contra]):
    """
    Только принимает (handle), никогда не возвращает T_contra наружу ->
    можно сделать контравариантным: Handler[Animal] безопасно
    использовать там, где ожидается Handler[Dog] (но не наоборот -
    см. demo_contravariant_fail.py).
    """

    def handle(self, item: T_contra) -> None:
        raise NotImplementedError