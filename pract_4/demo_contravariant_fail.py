"""
КОНТРАВАРИАНТНОСТЬ - неправильное направление.

Handler[Dog] НЕЛЬЗЯ использовать как Handler[Animal] - специалист
только по собакам не готов обработать кота, которого ему могут
прислать как "просто животное".

Запуск:
    mypy demo_contravariant_fail.py
    -> error: Incompatible types in assignment

    python demo_contravariant_fail.py
    -> а вот это уже не "тихая порча данных", а самый настоящий
       краш в рантайме: AttributeError. Хороший повод показать,
       что вариантность - это не придирки mypy на пустом месте.
"""
from __future__ import annotations

from containers import Handler
from models import Animal, Cat, Dog


class DogOnlyHandler(Handler[Dog]):
    def handle(self, item: Dog) -> None:
        print(item.bark())  # метод bark() есть только у Dog!


dog_handler: Handler[Dog] = DogOnlyHandler()

# mypy error ожидается на следующей строке:
animal_handler: Handler[Animal] = dog_handler

if __name__ == "__main__":
    # dog_handler и animal_handler - это ОДИН и тот же объект DogOnlyHandler.
    # Снаружи мы думаем, что передаём Animal, но bark() у Cat просто нет:
    animal_handler.handle(Cat("Мурка"))  # -> AttributeError во время выполнения