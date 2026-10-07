"""
Доменные классы (не pydantic!) — та же иерархия Animal/Dog/Cat,
что и во всём курсе, только теперь в контексте настоящего веб-сервиса.
Отделены от pydantic-схем (schemas.py) сознательно: это обычная практика
в FastAPI-проектах — domain-слой и слой API не должны быть одним и тем же.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Animal:
    id: int
    name: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class Dog(Animal):
    breed: str = "Дворняга"


@dataclass
class Cat(Animal):
    indoor: bool = True