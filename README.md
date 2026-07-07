# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

Running `python3 main.py`:

```text
Today's Schedule
================
Owner: Jordan

Daily plan for 2026-07-07:
- Morning Walk (30 min, priority 5)
- Breakfast (10 min, priority 4)
- Puzzle Toy (20 min, priority 3)
Total time used: 60 minutes

Reasoning:
Tasks were sorted by priority from highest to lowest, then added until the 60 minutes of available time were used. Scheduled tasks: Morning Walk, Breakfast, Puzzle Toy. Total time used: 60 minutes.
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

PawPal+ includes a few lightweight scheduling algorithms in `pawpal_system.py`.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Priority sorting | `Scheduler.sort_by_priority()` | Orders tasks from highest to lowest priority so important care tasks are considered first. |
| Time sorting | `Scheduler.sort_by_time()` | Orders tasks by their `HH:MM` time string, with untimed tasks placed last. |
| Time-limited planning | `Scheduler.generate_daily_plan()` | Builds a daily plan by adding incomplete tasks until the owner's available time is used. |
| Completion filtering | `Scheduler.filter_by_status()` | Returns either completed or incomplete tasks. |
| Pet filtering | `Scheduler.filter_by_pet()` | Returns only the tasks that belong to a named pet. |
| Conflict detection | `Scheduler.detect_conflicts()` | Returns warning messages when multiple tasks share the same exact time or preferred time. |
| Recurring tasks | `Scheduler.mark_task_complete()` | Marks a task complete and creates the next daily or weekly occurrence using `timedelta`. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
