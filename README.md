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

## ✨ Features

PawPal+ implements several lightweight scheduling algorithms in `pawpal_system.py`,
all exposed through both the Streamlit UI (`app.py`) and the CLI demo (`main.py`):

- **Priority scheduling** — builds a daily plan by adding incomplete tasks from
  highest to lowest priority until the owner's available time is used up
  (`generate_daily_plan`).
- **Sorting by priority** — orders every task from most to least important
  (`sort_by_priority`).
- **Sorting by time** — orders tasks chronologically by their `HH:MM` time,
  placing untimed tasks last (`sort_by_time`).
- **Filtering by status** — separates completed from outstanding tasks
  (`filter_by_status`).
- **Filtering by pet** — returns only the tasks belonging to a named pet,
  case-insensitively (`filter_by_pet`).
- **Conflict warnings** — flags when two tasks share the same exact time, or the
  same preferred time slot, so the owner can reschedule (`detect_conflicts`).
- **Daily & weekly recurrence** — completing a recurring task automatically
  generates its next occurrence one day or one week later; non-recurring tasks
  are left alone (`mark_task_complete`).
- **Plan explanation** — produces a plain-language summary of why tasks were
  chosen and ordered (`explain_plan`).

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
- Evening Walk (30 min, priority 5)
- Cat Breakfast (10 min, priority 4)
- Puzzle Toy (20 min, priority 3)
Total time used: 60 minutes

Reasoning:
Tasks were sorted by priority from highest to lowest, then added until the 60 minutes of available time were used. Scheduled tasks: Evening Walk, Cat Breakfast, Puzzle Toy. Total time used: 60 minutes.
```

## 🧪 Testing PawPal+

Run the full automated test suite from the project root:

```bash
python -m pytest
```

The suite lives in `tests/` and covers the core scheduling behaviors,
including both happy paths and edge cases:

- **Sorting correctness** — tasks return in chronological (`HH:MM`) order,
  and untimed tasks (`time=None`) sort to the end without crashing.
- **Recurrence logic** — completing a daily task creates a new task for the
  next day; non-recurring tasks create no copy.
- **Conflict detection** — the `Scheduler` flags two tasks scheduled at the
  same exact time, and returns no warnings when times differ.
- **Core model behavior** — task completion status, pet task management,
  owner task aggregation, priority sorting, time-limited daily planning,
  and completion/pet filtering.

Successful run:

```
============================= test session starts ==============================
platform darwin -- Python 3.13.13, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/harshinibondila/ai110-module2show-pawpal-starter
plugins: anyio-4.14.0
collected 20 items

tests/test_pawpal.py ........                                            [ 40%]
tests/test_pawpal_system.py ............                                 [100%]

============================== 20 passed in 0.02s ==============================
```

**Confidence Level: ★★★★☆ (4/5)**

All 20 tests pass, covering every core scheduling algorithm plus key edge
cases (empty times, non-recurring tasks, non-conflicting schedules). Held
back from 5 stars because a few paths remain untested — case-insensitive
pet filtering, unknown recurrence frequencies (e.g. `monthly`), and
three-way time conflicts — so reliability is high but not yet exhaustively
proven.

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

## 🎬 Demo Walkthrough

### Main UI features

The Streamlit app (`streamlit run app.py`) lets a pet owner:

- **Set the owner** — enter the owner's name.
- **Add pets** — name, species, and age; added pets appear in a table.
- **Add tasks per pet** — title, category, duration, priority (1–5), a preferred
  time slot, and an optional exact `HH:MM` scheduled time.
- **Review all tasks** — a table shows every task with its pet, duration,
  priority, time, and done status.
- **Build a schedule** — set the available minutes for the day and generate a
  plan. The app then displays conflict checks, the day's plan, sortable task
  views, outstanding tasks, and the plan's reasoning.

### Example workflow

1. Enter the owner name (e.g. *Jordan*).
2. Add a pet — *Bella*, a 4-year-old dog.
3. Add a task for Bella — *Evening Walk*, 30 min, priority 5, scheduled `18:00`.
4. Add another task — *Puzzle Toy*, 20 min, priority 3, also scheduled `18:00`.
5. Set available time to 60 minutes and click **Generate schedule**.
6. PawPal+ warns that *Evening Walk* and *Puzzle Toy* clash at `18:00`, shows the
   priority-ordered daily plan, and explains its reasoning.

### Key Scheduler behaviors shown

- **Priority ordering** — the daily plan lists the highest-priority tasks first.
- **Sorting** — tasks can be re-sorted by priority or by time on demand.
- **Conflict warnings** — same-time tasks are flagged with an amber warning that
  names both tasks and suggests moving one.
- **Filtering** — outstanding (not-done) tasks are listed separately.
- **Recurrence** — completing a daily task rolls it forward to the next day.

### Sample CLI output

Running `python3 main.py`:

```text
Today's Schedule
================
Owner: Jordan

Daily plan for 2026-07-07:
- Evening Walk (30 min, priority 5)
- Cat Breakfast (10 min, priority 4)
- Puzzle Toy (20 min, priority 3)
Total time used: 60 minutes

Reasoning:
Tasks were sorted by priority from highest to lowest, then added until the 60 minutes of available time were used. Scheduled tasks: Evening Walk, Cat Breakfast, Puzzle Toy. Total time used: 60 minutes.

Sorted by Time
==============
07:30 - Cat Breakfast (feeding)
08:30 - Morning Brush (grooming)
18:00 - Evening Walk (walk)
18:00 - Puzzle Toy (enrichment)

Incomplete Tasks
================
- Evening Walk
- Cat Breakfast
- Puzzle Toy

Conflict Warnings
=================
- 18:00 conflict: Bella - Evening Walk, Mochi - Puzzle Toy are scheduled at the same time.
- morning has multiple preferred tasks: Morning Brush, Cat Breakfast

Bella's Tasks
=============
- Evening Walk at 18:00 (not done)
- Morning Brush at 08:30 (done)

Recurring Completion
====================
Completed: Cat Breakfast for 2026-07-07
Next occurrence: Cat Breakfast for 2026-07-08
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
