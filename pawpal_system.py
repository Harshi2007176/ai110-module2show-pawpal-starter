"""Backend class skeletons for the PawPal+ scheduling system."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any


@dataclass
class Task:
    """A single pet care activity."""

    name: str
    category: str
    duration: int
    priority: int
    is_recurring: bool = True
    preferred_time: str | None = None
    is_done: bool = False

    def mark_done(self) -> None:
        """Mark this task as completed."""
        pass


@dataclass
class Pet:
    """A pet with its own care tasks."""

    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task for this pet."""
        pass

    def remove_task(self, task: Task) -> None:
        """Remove a care task from this pet."""
        pass

    def get_tasks(self) -> list[Task]:
        """Return this pet's care tasks."""
        pass


@dataclass
class Owner:
    """The human owner responsible for one or more pets."""

    name: str
    pets: list[Pet] = field(default_factory=list)
    preferences: dict[str, Any] = field(default_factory=dict)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list."""
        pass

    def get_all_tasks(self) -> list[Task]:
        """Return all tasks across all of this owner's pets."""
        pass


@dataclass
class DailyPlan:
    """The generated care schedule for one day."""

    date: date
    scheduled_tasks: list[Task] = field(default_factory=list)
    total_time_used: int = 0

    def display(self) -> str:
        """Return a readable version of the daily plan."""
        pass

    def add_task_to_plan(self, task: Task) -> None:
        """Insert a task into the daily plan."""
        pass


@dataclass
class Scheduler:
    """Organizes tasks into a daily plan."""

    tasks: list[Task]
    available_time: int

    def sort_by_priority(self) -> list[Task]:
        """Return tasks ordered from highest to lowest priority."""
        pass

    def detect_conflicts(self) -> list[str]:
        """Return warnings for tasks that conflict with each other."""
        pass

    def generate_daily_plan(self) -> DailyPlan:
        """Build an ordered daily plan that respects the available time."""
        pass

    def explain_plan(self) -> str:
        """Explain why tasks were ordered or selected for the plan."""
        pass
