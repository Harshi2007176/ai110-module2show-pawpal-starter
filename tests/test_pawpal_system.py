from datetime import date, timedelta
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_can_be_marked_done():
    task = Task("Morning walk", "walk", 30, 5)

    task.mark_done()

    assert task.is_done is True


def test_pet_manages_its_task_list():
    pet = Pet("Bella", "dog", 4)
    task = Task("Breakfast", "feeding", 10, 5)

    pet.add_task(task)
    tasks = pet.get_tasks()
    pet.remove_task(task)

    assert tasks == [task]
    assert pet.get_tasks() == []


def test_owner_gathers_tasks_from_all_pets():
    owner = Owner("Jordan")
    dog = Pet("Bella", "dog", 4)
    cat = Pet("Mochi", "cat", 2)
    walk = Task("Walk", "walk", 30, 5)
    food = Task("Dinner", "feeding", 10, 4)

    dog.add_task(walk)
    cat.add_task(food)
    owner.add_pet(dog)
    owner.add_pet(cat)

    assert owner.get_all_tasks() == [walk, food]


def test_scheduler_retrieves_tasks_from_owner_and_sorts_by_priority():
    owner = Owner("Jordan")
    pet = Pet("Bella", "dog", 4)
    low = Task("Brush fur", "grooming", 15, 2)
    high = Task("Medication", "medication", 5, 5)
    pet.add_task(low)
    pet.add_task(high)
    owner.add_pet(pet)

    scheduler = Scheduler(owner, available_time=30)

    assert scheduler.get_tasks() == [low, high]
    assert scheduler.sort_by_priority() == [high, low]


def test_scheduler_generates_time_limited_daily_plan():
    tasks = [
        Task("Play", "enrichment", 25, 2),
        Task("Medication", "medication", 5, 5),
        Task("Walk", "walk", 30, 4),
    ]
    scheduler = Scheduler(tasks, available_time=35)

    plan = scheduler.generate_daily_plan(plan_date=date(2026, 7, 7))

    assert plan.date == date(2026, 7, 7)
    assert plan.scheduled_tasks == [tasks[1], tasks[2]]
    assert plan.total_time_used == 35
    assert "Medication" in plan.display()
    assert "35 minutes" in scheduler.explain_plan()


def test_scheduler_sorts_tasks_by_hh_mm_time():
    tasks = [
        Task("Dinner", "feeding", 10, 4, time="18:00"),
        Task("Breakfast", "feeding", 10, 5, time="08:00"),
        Task("Lunch Walk", "walk", 20, 3, time="12:30"),
    ]
    scheduler = Scheduler(tasks, available_time=60)

    sorted_tasks = scheduler.sort_by_time()

    assert sorted_tasks == [tasks[1], tasks[2], tasks[0]]


def test_scheduler_filters_tasks_by_completion_status():
    done = Task("Done task", "grooming", 10, 1, is_done=True)
    not_done = Task("Open task", "walk", 20, 5)
    scheduler = Scheduler([done, not_done], available_time=60)

    assert scheduler.filter_by_status(is_done=False) == [not_done]
    assert scheduler.filter_by_status(is_done=True) == [done]


def test_scheduler_filters_tasks_by_pet_name():
    owner = Owner("Jordan")
    bella = Pet("Bella", "dog", 4)
    mochi = Pet("Mochi", "cat", 2)
    walk = Task("Walk", "walk", 30, 5)
    food = Task("Food", "feeding", 10, 4)
    bella.add_task(walk)
    mochi.add_task(food)
    owner.add_pet(bella)
    owner.add_pet(mochi)
    scheduler = Scheduler(owner, available_time=60)

    assert scheduler.filter_by_pet("Bella") == [walk]
    assert scheduler.filter_by_pet("Mochi") == [food]


def test_scheduler_completes_daily_task_and_adds_next_occurrence_to_pet():
    owner = Owner("Jordan")
    bella = Pet("Bella", "dog", 4)
    task = Task(
        "Morning walk",
        "walk",
        30,
        5,
        frequency="daily",
        due_date=date(2026, 7, 7),
    )
    bella.add_task(task)
    owner.add_pet(bella)
    scheduler = Scheduler(owner, available_time=60)

    next_task = scheduler.mark_task_complete(task)

    assert task.is_done is True
    assert next_task is not None
    assert next_task.due_date == date(2026, 7, 7) + timedelta(days=1)
    assert next_task.is_done is False
    assert bella.get_tasks() == [task, next_task]


def test_scheduler_completes_weekly_task_and_adds_next_occurrence_to_list():
    task = Task(
        "Brush coat",
        "grooming",
        15,
        2,
        frequency="weekly",
        due_date=date(2026, 7, 7),
    )
    task_list = [task]
    scheduler = Scheduler(task_list, available_time=60)

    next_task = scheduler.mark_task_complete(task)

    assert task.is_done is True
    assert next_task is not None
    assert next_task.due_date == date(2026, 7, 7) + timedelta(weeks=1)
    assert task_list == [task, next_task]


def test_scheduler_completes_non_recurring_task_without_copying_it():
    task = Task(
        "One-time vet visit",
        "medication",
        45,
        5,
        frequency="once",
        is_recurring=False,
        due_date=date(2026, 7, 7),
    )
    task_list = [task]
    scheduler = Scheduler(task_list, available_time=60)

    next_task = scheduler.mark_task_complete(task)

    assert task.is_done is True
    assert next_task is None
    assert task_list == [task]


def test_scheduler_detects_tasks_at_the_same_time_across_pets():
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

    assert conflicts == [
        "08:00 conflict: Bella - Walk, Mochi - Breakfast are scheduled at the same time."
    ]
