"""
КОНТРАВАРИАНТНОСТЬ - корректное использование (расширение разрешено).

Handler[Animal] можно передать туда, где ожидается Handler[Dog] -
направление ОБРАТНОЕ по сравнению с ковариантностью: обработчик
более общего типа подходит и для более частного случая.

Запуск:
    mypy demo_contravariant_ok.py   -> Success: no issues found
    python demo_contravariant_ok.py -> напечатает лог
"""
from __future__ import annotations

from containers import Handler
from models import Animal, Dog


class AnimalLogger(Handler[Animal]):
    """Умеет обрабатывать ЛЮБОЕ животное - значит, справится и с Dog."""

    def handle(self, item: Animal) -> None:
        print(f"Залогировано животное: {item}")


def process_dog(handler: Handler[Dog], dog: Dog) -> None:
    handler.handle(dog)


if __name__ == "__main__":
    process_dog(AnimalLogger(), Dog("Рекс"))
    # Handler[Animal] передан туда, где ждут Handler[Dog] -> OK,
    # это и есть контравариантность