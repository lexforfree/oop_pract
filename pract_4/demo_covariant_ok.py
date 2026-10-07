"""
КОВАРИАНТНОСТЬ - корректное использование (сужение разрешено).

ReadOnlyStack[Dog] можно передать туда, где ожидается
ReadOnlyStack[Animal] - ковариантность "идёт в ту же сторону",
что и наследование (Dog -> Animal).

Запуск:
    mypy demo_covariant_ok.py      -> Success: no issues found
    python demo_covariant_ok.py    -> напечатает последнего в стеке
"""
from __future__ import annotations

from containers import ReadOnlyStack
from models import Animal, Dog


def show_last(stack: ReadOnlyStack[Animal]) -> None:
    print("Последний в стеке:", stack.peek())


if __name__ == "__main__":
    dog_view: ReadOnlyStack[Dog] = ReadOnlyStack([Dog("Рекс"), Dog("Бобик")])
    show_last(dog_view)  # ReadOnlyStack[Dog] передан туда, где ждут
    # ReadOnlyStack[Animal] -> OK, это и есть ковариантность