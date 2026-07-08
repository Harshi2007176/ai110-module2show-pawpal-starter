from datetime import date
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_completion_changes_status():
    task = Task("Morning Walk", "walk", 30, 5)

    task.mark_done()

    assert task.is_done is True


def test_adding_task_increases_pet_task_count():
    pet = Pet("Bella", "dog", 4)
    task = Task("Breakfast", "feeding", 10, 4)

    starting_count = len(pet.tasks)
    pet.add_task(task)

    assert len(pet.tasks) == starting_count + 1


# --- Sorting correctness: tasks come back in chronological (HH:MM) order ---
def test_sort_by_time_returns_tasks_in_chronological_order():
    dinner = Task("Dinner", "feeding", 10, 4, time="18:00")
    breakfast = Task("Breakfast", "feeding", 10, 5, time="07:30")
    lunch = Task("Lunch Walk", "walk", 20, 3, time="12:15")
    scheduler = Scheduler([dinner, breakfast, lunch], available_time=60)

    ordered = scheduler.sort_by_time()

    assert ordered == [breakfast, lunch, dinner]


# Edge case: a task with no time (None) should sort to the end, not crash.
def test_sort_by_time_puts_untimed_tasks_last():
    timed = Task("Walk", "walk", 30, 5, time="09:00")
    untimed = Task("Nap check", "rest", 5, 1, time=None)
    scheduler = Scheduler([untimed, timed], available_time=60)

    ordered = scheduler.sort_by_time()

    assert ordered == [timed, untimed]


# --- Recurrence logic: completing a daily task creates one for the next day ---
def test_completing_daily_task_creates_next_day_occurrence():
    owner = Owner("Jordan")
    bella = Pet("Bella", "dog", 4)
    walk = Task(
        "Morning Walk",
        "walk",
        30,
        5,
        frequency="daily",
        due_date=date(2026, 7, 7),
    )
    bella.add_task(walk)
    owner.add_pet(bella)
    scheduler = Scheduler(owner, available_time=60)

    next_walk = scheduler.mark_task_complete(walk)

    assert walk.is_done is True
    assert next_walk is not None
    assert next_walk.due_date == date(2026, 7, 8)
    assert next_walk.is_done is False
    assert bella.get_tasks() == [walk, next_walk]


# Edge case: a non-recurring task should NOT spawn a copy.
def test_completing_non_recurring_task_creates_no_copy():
    task = Task("Vet Visit", "medication", 45, 5, is_recurring=False)
    task_list = [task]
    scheduler = Scheduler(task_list, available_time=60)

    next_task = scheduler.mark_task_complete(task)

    assert next_task is None
    assert task_list == [task]


# --- Conflict detection: two tasks at the same time are flagged ---
def test_detect_conflicts_flags_duplicate_times():
    owner = Owner("Jordan")
    bella = Pet("Bella", "dog", 4)
    mochi = Pet("Mochi", "cat", 2)
    walk = Task("Walk", "walk", 30, 5, time="08:00")
    breakfast = Task("Breakfast", "feeding", 10, 4, time="08:00")
    bella.add_task(walk)
    mochi.add_task(breakfast)
    owner.add_pet(bella)
    owner.add_pet(mochi)
    scheduler = Scheduler(owner, available_time=60)

    conflicts = scheduler.detect_conflicts()

    assert any("08:00 conflict" in warning for warning in conflicts)


# Edge case: distinct times = no conflict.
def test_detect_conflicts_returns_empty_when_times_differ():
    early = Task("Walk", "walk", 30, 5, time="08:00")
    late = Task("Dinner", "feeding", 10, 4, time="18:00")
    scheduler = Scheduler([early, late], available_time=60)

    assert scheduler.detect_conflicts() == []
