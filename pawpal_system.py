"""Backend class skeletons for the PawPal+ scheduling system."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import date, timedelta
from typing import Any


@dataclass
class Task:
    """A single pet care activity."""

    name: str
    category: str
    duration: int
    priority: int
    description: str = ""
    frequency: str = "daily"
    time: str | None = None
    due_date: date = field(default_factory=date.today)
    is_recurring: bool = True
    preferred_time: str | None = None
    is_done: bool = False

    def mark_done(self) -> None:
        """Mark this task as completed."""
        self.is_done = True

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.mark_done()


@dataclass
class Pet:
    """A pet with its own care tasks."""

    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task for this pet."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a care task from this pet."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self) -> list[Task]:
        """Return this pet's care tasks."""
        return list(self.tasks)


@dataclass
class Owner:
    """The human owner responsible for one or more pets."""

    name: str
    pets: list[Pet] = field(default_factory=list)
    preferences: dict[str, Any] = field(default_factory=dict)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return all tasks across all of this owner's pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


@dataclass
class DailyPlan:
    """The generated care schedule for one day."""

    date: date
    scheduled_tasks: list[Task] = field(default_factory=list)
    total_time_used: int = 0

    def display(self) -> str:
        """Return a readable version of the daily plan."""
        if not self.scheduled_tasks:
            return f"Daily plan for {self.date}: no tasks scheduled."

        lines = [f"Daily plan for {self.date}:"]
        for task in self.scheduled_tasks:
            lines.append(
                f"- {task.name} ({task.duration} min, priority {task.priority})"
            )
        lines.append(f"Total time used: {self.total_time_used} minutes")
        return "\n".join(lines)

    def add_task_to_plan(self, task: Task) -> None:
        """Insert a task into the daily plan."""
        self.scheduled_tasks.append(task)
        self.total_time_used += task.duration


@dataclass
class Scheduler:
    """Organizes tasks into a daily plan."""

    tasks: list[Task] | Owner
    available_time: int
    last_plan: DailyPlan | None = field(default=None, init=False)

    def get_tasks(self) -> list[Task]:
        """Retrieve tasks from an owner or from a direct task list."""
        if isinstance(self.tasks, Owner):
            return self.tasks.get_all_tasks()
        return list(self.tasks)

    def sort_by_priority(self) -> list[Task]:
        """Return tasks ordered from highest to lowest priority."""
        return sorted(self.get_tasks(), key=lambda task: task.priority, reverse=True)

    def sort_by_time(self) -> list[Task]:
        """Return tasks ordered by HH:MM time."""
        return sorted(self.get_tasks(), key=lambda task: task.time or "99:99")

    def filter_by_status(self, is_done: bool) -> list[Task]:
        """Return tasks matching a completion status."""
        return [task for task in self.get_tasks() if task.is_done is is_done]

    def filter_by_pet(self, pet_name: str) -> list[Task]:
        """Return tasks that belong to a named pet."""
        if not isinstance(self.tasks, Owner):
            return []

        for pet in self.tasks.pets:
            if pet.name.lower() == pet_name.lower():
                return pet.get_tasks()

        return []

    def mark_task_complete(self, task: Task) -> Task | None:
        """Complete a task and create its next recurring occurrence."""
        task.mark_done()
        next_due_date = self._next_due_date(task)

        if next_due_date is None:
            return None

        next_task = replace(task, due_date=next_due_date, is_done=False)
        self._add_next_task(task, next_task)
        return next_task

    def _next_due_date(self, task: Task) -> date | None:
        """Return the next due date for daily or weekly tasks."""
        if not task.is_recurring:
            return None

        frequency = task.frequency.lower()
        if frequency == "daily":
            return task.due_date + timedelta(days=1)
        if frequency == "weekly":
            return task.due_date + timedelta(weeks=1)

        return None

    def _add_next_task(self, original_task: Task, next_task: Task) -> None:
        """Add a recurring copy beside the original task."""
        if isinstance(self.tasks, Owner):
            for pet in self.tasks.pets:
                if original_task in pet.tasks:
                    pet.add_task(next_task)
                    return
        else:
            self.tasks.append(next_task)

    def detect_conflicts(self) -> list[str]:
        """Return warnings for tasks that conflict with each other."""
        conflicts = []
        tasks_by_time: dict[str, list[tuple[str | None, Task]]] = {}

        for pet_name, task in self._tasks_with_pet_names():
            if task.time:
                tasks_by_time.setdefault(task.time, []).append((pet_name, task))

        for task_time, scheduled_tasks in tasks_by_time.items():
            if len(scheduled_tasks) > 1:
                task_names = ", ".join(
                    self._format_conflict_task(pet_name, task)
                    for pet_name, task in scheduled_tasks
                )
                conflicts.append(
                    f"{task_time} conflict: {task_names} are scheduled at the same time."
                )

        tasks_by_preferred_time: dict[str, list[Task]] = {}
        for task in self.get_tasks():
            if task.preferred_time:
                tasks_by_preferred_time.setdefault(task.preferred_time, []).append(task)

        for preferred_time, tasks in tasks_by_preferred_time.items():
            if len(tasks) > 1:
                task_names = ", ".join(task.name for task in tasks)
                conflicts.append(
                    f"{preferred_time} has multiple preferred tasks: {task_names}"
                )

        return conflicts

    def _tasks_with_pet_names(self) -> list[tuple[str | None, Task]]:
        """Return tasks paired with pet names when available."""
        if isinstance(self.tasks, Owner):
            task_pairs = []
            for pet in self.tasks.pets:
                for task in pet.get_tasks():
                    task_pairs.append((pet.name, task))
            return task_pairs

        return [(None, task) for task in self.tasks]

    def _format_conflict_task(self, pet_name: str | None, task: Task) -> str:
        """Format a task for a conflict warning."""
        if pet_name:
            return f"{pet_name} - {task.name}"
        return task.name

    def generate_daily_plan(self, plan_date: date | None = None) -> DailyPlan:
        """Build an ordered daily plan that respects the available time."""
        plan = DailyPlan(date=plan_date or date.today())

        for task in self.sort_by_priority():
            if task.is_done:
                continue
            if plan.total_time_used + task.duration <= self.available_time:
                plan.add_task_to_plan(task)

        self.last_plan = plan
        return plan

    def explain_plan(self) -> str:
        """Explain why tasks were ordered or selected for the plan."""
        if self.last_plan is None:
            self.generate_daily_plan()

        assert self.last_plan is not None
        if not self.last_plan.scheduled_tasks:
            return "No tasks fit within the available time."

        task_names = ", ".join(task.name for task in self.last_plan.scheduled_tasks)
        return (
            "Tasks were sorted by priority from highest to lowest, then added "
            f"until the {self.available_time} minutes of available time were used. "
            f"Scheduled tasks: {task_names}. Total time used: "
            f"{self.last_plan.total_time_used} minutes."
        )
