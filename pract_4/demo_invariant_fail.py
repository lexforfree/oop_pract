"""
ИНВАРИАНТНОСТЬ - нарушение в ОБЕИХ направлениях.

У инвариантного типа нет "разрешённой" стороны - ни расширение,
ни сужение не проходят. Это отличает его от ковариантности
и контравариантности, у каждой из которых есть одно рабочее направление.

Запуск:
    mypy demo_invariant_fail.py
    -> два error: Incompatible types in assignment

    python demo_invariant_fail.py
    -> выполнится ПОЛНОСТЬЮ, без единой ошибки в рантайме!
       Именно в этом разрыве между mypy и python - весь смысл занятия.
"""
from __future__ import annotations

from containers import Stack
from models import Animal, Dog

dog_stack: Stack[Dog] = Stack()
dog_stack.push(Dog("Рекс"))

# Попытка №1: Stack[Dog] -> Stack[Animal] (расширение).
# mypy error ожидается на следующей строке:
animal_stack: Stack[Animal] = dog_stack
# Если бы это разрешили - через animal_stack можно было бы
# animal_stack.push(Cat(...)), и dog_stack оказался бы испорчен изнутри.

generic_animals: Stack[Animal] = Stack()

# Попытка №2: Stack[Animal] -> Stack[Dog] (сужение).
# mypy error ожидается на следующей строке:
narrowed: Stack[Dog] = generic_animals
# Тоже небезопасно: generic_animals может в будущем получить Cat
# через push(), а narrowed обещает хранить только Dog.

if __name__ == "__main__":
    print("Файл выполнился до конца без единой ошибки.")
    print("Запустите `mypy demo_invariant_fail.py`, чтобы увидеть то,")
    print("что обычный запуск python никогда не покажет.")