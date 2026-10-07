"""
ФИНАЛЬНЫЙ ПРИМЕР: Producer / Consumer в одном сценарии.

Мини-модель приюта для животных, использующая все три вида
вариантности сразу - ровно так, как это обычно и происходит
в реальном коде: один и тот же проект использует invariant-хранилище,
covariant-отчётность и contravariant-обработчики событий одновременно.

Запуск:
    mypy demo_producer_consumer.py   -> Success: no issues found
    python demo_producer_consumer.py -> полноценно отработает сценарий
"""
from __future__ import annotations

from containers import Handler, ReadOnlyStack, Stack
from models import Animal, Dog


class AdoptionLogger(Handler[Animal]):
    """Контравариантный consumer: логирует усыновление ЛЮБОГО животного."""

    def handle(self, item: Animal) -> None:
        print(f"[Лог усыновления] {item} нашёл дом")


class Shelter:
    """
    Внутри - инвариантный Stack (мы и добавляем, и забираем животных).
    Наружу для отчётов - ковариантный ReadOnlyStack (только смотрим).
    Для событий усыновления - принимаем контравариантный Handler.
    """

    def __init__(self) -> None:
        self._dogs: Stack[Dog] = Stack()

    def accept(self, dog: Dog) -> None:
        self._dogs.push(dog)

    def report(self) -> ReadOnlyStack[Dog]:
        return ReadOnlyStack(self._dogs.snapshot())

    def adopt_next(self, handler: Handler[Dog]) -> None:
        """
        Handler[Dog] запрошен по сигнатуре, но благодаря контравариантности
        сюда можно передать и Handler[Animal] - именно это ниже и происходит.
        """
        if self._dogs:
            dog = self._dogs.pop()
            handler.handle(dog)


if __name__ == "__main__":
    shelter = Shelter()
    shelter.accept(Dog("Рекс"))
    shelter.accept(Dog("Бобик"))

    print("Отчёт по приюту (covariant read-only view):")
    for dog in shelter.report().all():
        print(" -", dog)

    print()
    print("Усыновление (contravariant handler):")
    # AdoptionLogger - это Handler[Animal], а adopt_next() просит Handler[Dog].
    # Работает благодаря контравариантности.
    shelter.adopt_next(AdoptionLogger())
    shelter.adopt_next(AdoptionLogger())