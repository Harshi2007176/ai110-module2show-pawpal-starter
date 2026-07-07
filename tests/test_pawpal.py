from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pawpal_system import Pet, Task


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
