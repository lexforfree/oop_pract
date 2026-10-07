"""Minimal domain model for the variance demo examples."""


class Animal:
    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return self.name


class Dog(Animal):
    pass


class Cat(Animal):
    pass
