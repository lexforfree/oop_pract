"""
КОВАРИАНТНОСТЬ - неправильное направление.

У ковариантности есть только ОДНА рабочая сторона: можно подставить
более узкий тип туда, где ждут более широкий (Dog вместо Animal).
Обратное - подставить ReadOnlyStack[Animal] туда, где объявлен
ReadOnlyStack[Dog] - небезопасно и должно быть ошибкой.

Запуск:
    mypy demo_covariant_fail.py   -> error: Incompatible types in assignment
    python demo_covariant_fail.py -> выполнится, но результат вас удивит
"""
from __future__ import annotations

from containers import ReadOnlyStack
from models import Animal, Cat, Dog

animal_view: ReadOnlyStack[Animal] = ReadOnlyStack([Dog("Рекс"), Cat("Мурка")])

# mypy error ожидается на следующей строке:
dog_view: ReadOnlyStack[Dog] = animal_view
# Если бы mypy это разрешил, у нас была бы переменная "только собаки",
# в которой на самом деле прячется кот. Запуск ниже это и показывает.

if __name__ == "__main__":
    print("Python не видит проблемы и просто выполняет код:")
    for item in dog_view.all():
        print(" -", item, "(а должны были быть только собаки!)")