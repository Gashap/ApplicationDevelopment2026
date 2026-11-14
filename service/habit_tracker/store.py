"""Внутренняя модель и in-memory хранилище привычек.

HabitEntity — то, как привычка хранится внутри сервиса. Наружу она не уходит:
контроллер переводит её в DTO HabitView из спеки, поэтому owner_id,
reminder_job_id и прочие служебные поля клиент никогда не увидит.
"""
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional


@dataclass
class HabitEntity:
    id: int
    owner_id: str
    title: str
    frequency: str
    description: Optional[str] = None
    target_per_week: Optional[int] = None
    status: str = "ACTIVE"
    current_streak: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    reminder_job_id: Optional[str] = None


class HabitStore:
    """Данные живут в памяти процесса и пропадают после перезапуска."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._habits: Dict[int, HabitEntity] = {}
        self._next_id = 1

    def create(self, owner_id: str, title: str, frequency: str,
               description: Optional[str] = None,
               target_per_week: Optional[int] = None) -> HabitEntity:
        with self._lock:
            habit = HabitEntity(
                id=self._next_id,
                owner_id=owner_id,
                title=title,
                frequency=frequency,
                description=description,
                target_per_week=target_per_week,
            )
            self._habits[habit.id] = habit
            self._next_id += 1
            return habit

    def find(self, habit_id: int) -> Optional[HabitEntity]:
        return self._habits.get(habit_id)

    def list_for_owner(self, owner_id: str, status: Optional[str] = None) -> List[HabitEntity]:
        return [
            h for h in sorted(self._habits.values(), key=lambda h: h.id)
            if h.owner_id == owner_id and (status is None or h.status == status)
        ]

    def delete(self, habit_id: int) -> None:
        with self._lock:
            self._habits.pop(habit_id, None)

    def clear(self) -> None:
        with self._lock:
            self._habits.clear()
            self._next_id = 1


store = HabitStore()
