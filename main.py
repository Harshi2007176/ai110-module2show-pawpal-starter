"""Temporary terminal demo for the PawPal+ logic layer."""

from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def build_demo_owner() -> Owner:
    """Create sample owner, pets, and care tasks for a terminal demo."""
    owner = Owner(
        name="Jordan",
        preferences={"available_hours_per_day": 1, "prefers": "morning walks"},
    )

    bella = Pet(name="Bella", species="dog", age=4)
    mochi = Pet(name="Mochi", species="cat", age=2)

    bella.add_task(
        Task(
            name="Evening Walk",
            category="walk",
            duration=30,
            priority=5,
            description="Give Bella exercise after work.",
            time="18:00",
            preferred_time="evening",
        )
    )
    bella.add_task(
        Task(
            name="Morning Brush",
            category="grooming",
            duration=15,
            priority=2,
            description="Quick coat brushing.",
            time="08:30",
            preferred_time="morning",
            is_done=True,
        )
    )
    mochi.add_task(
        Task(
            name="Cat Breakfast",
            category="feeding",
            duration=10,
            priority=4,
            description="Serve Mochi's morning food.",
            time="07:30",
            preferred_time="morning",
        )
    )
    mochi.add_task(
        Task(
            name="Puzzle Toy",
            category="enrichment",
            duration=20,
            priority=3,
            description="Set out an enrichment toy.",
            time="18:00",
            preferred_time="afternoon",
        )
    )

    owner.add_pet(bella)
    owner.add_pet(mochi)
    return owner


def main() -> None:
    """Run a simple terminal demonstration of the scheduling logic."""
    owner = build_demo_owner()
    scheduler = Scheduler(owner, available_time=60)
    plan = scheduler.generate_daily_plan(plan_date=date.today())

    print("Today's Schedule")
    print("================")
    print(f"Owner: {owner.name}")
    print()
    print(plan.display())
    print()
    print("Reasoning:")
    print(scheduler.explain_plan())
    print()

    print("Sorted by Time")
    print("==============")
    for task in scheduler.sort_by_time():
        print(f"{task.time} - {task.name} ({task.category})")
    print()

    print("Incomplete Tasks")
    print("================")
    for task in scheduler.filter_by_status(is_done=False):
        print(f"- {task.name}")
    print()

    print("Conflict Warnings")
    print("=================")
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for conflict in conflicts:
            print(f"- {conflict}")
    else:
        print("- No conflicts found.")
    print()

    print("Bella's Tasks")
    print("=============")
    for task in scheduler.filter_by_pet("Bella"):
        status = "done" if task.is_done else "not done"
        print(f"- {task.name} at {task.time} ({status})")
    print()

    print("Recurring Completion")
    print("====================")
    breakfast = next(
        task for task in owner.get_all_tasks() if task.name == "Cat Breakfast"
    )
    next_breakfast = scheduler.mark_task_complete(breakfast)
    print(f"Completed: {breakfast.name} for {breakfast.due_date}")
    if next_breakfast:
        print(f"Next occurrence: {next_breakfast.name} for {next_breakfast.due_date}")


if __name__ == "__main__":
    main()
