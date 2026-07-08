# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My initial UML design consists of five classes: Owner, Pet, Task, Scheduler, and DailyPlan. The Owner class stores the owner's name, their list of pets, and their preferences, and is responsible for adding pets and collecting tasks across all of them. The Pet class stores each pet's name, species, age, and list of tasks, and is responsible for adding, removing, and retrieving its own tasks. The Task class holds the details of a single care activity — its name, category, duration, priority, whether it recurs, a preferred time, and completion status — and is responsible for marking itself done. The Scheduler class acts as the core logic of the system, taking in all tasks and available time to sort by priority, detect conflicts, generate a daily plan, and explain its scheduling decisions. Finally, the DailyPlan class stores the finished schedule, including the date, ordered tasks, and total time used, and is responsible for displaying the plan. Together, these classes form a clear structure where an Owner has many Pets, each Pet has many Tasks, and the Scheduler organizes those Tasks into a DailyPlan.

**b. Design changes**

Yes, my design changed as I implemented the logic. Rather than adding a separate ScheduledTask class, I kept conflict detection simple by giving the Task class its own optional `time` field (an `HH:MM` string) plus a `preferred_time` slot, so the Scheduler could compare tasks directly without a new class. I also added `frequency`, `due_date`, and `is_recurring` fields to Task to support daily and weekly recurrence, and expanded the Scheduler beyond the original skeleton with `sort_by_time`, `filter_by_status`, `filter_by_pet`, and `mark_task_complete`. The Scheduler was also generalized to accept either an Owner or a plain list of tasks, which made it much easier to test. These changes are reflected in `diagrams/uml_final.mmd`.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

My scheduler considers three main constraints: the owner's **available time** for the day, each task's **priority** (1–5), and **timing** (both an exact `HH:MM` time and a preferred time slot like "morning"). The daily plan greedily adds the highest-priority incomplete tasks until the available time runs out, so time and priority are the two constraints that directly shape the plan.

I decided priority and available time mattered most because they answer the core question the app exists to solve: "given a limited day, which care tasks should happen first?" Preferred time and exact time matter too, but I treated them as inputs to conflict *warnings* rather than hard scheduling rules — the owner stays in control of when things actually happen, and the app just flags overlaps.

**b. Tradeoffs**

One tradeoff my scheduler makes is that conflict detection only checks for exact matching task times, such as two tasks both scheduled at 18:00. It does not yet check for overlapping durations, like a 30-minute walk at 18:00 conflicting with a feeding at 18:15. I asked AI how the algorithm could be simplified, and it suggested breaking the conflict logic into smaller helper methods. I decided to keep the current version because it is still readable for this project and avoids making the code feel more complicated than the assignment needs.

This tradeoff is reasonable because PawPal+ is a beginner-friendly scheduling app, and exact-time warnings already help the pet owner notice obvious conflicts. A more advanced version could compare start and end times, but the current approach keeps the logic easier to explain, test, and maintain.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI across every phase: brainstorming the UML classes, converting the diagram into Python skeletons, implementing the scheduling algorithms, writing the automated test suite, and upgrading the Streamlit UI. The most helpful prompts were **specific and file-anchored** — for example, "based on my final `pawpal_system.py`, what should I change in my UML?" or "what are the most important edge cases to test for a pet scheduler with sorting and recurring tasks?" Open-ended prompts gave generic answers; prompts that referenced my actual code gave answers I could act on directly.

**b. Judgment and verification**

One moment I did not accept a suggestion as-is: the AI proposed splitting my conflict-detection logic into several small helper methods and adding a separate `ScheduledTask` class to track start/end times. I kept the simpler version — an optional `time` field on Task and exact-time matching — because a beginner-friendly app doesn't need duration-overlap detection yet, and the extra class would have made the code harder to explain and test. I verified AI suggestions by **running `python -m pytest` after every change** (all 20 tests stayed green) and by running `main.py` to watch the real output, rather than trusting that generated code worked.

**c. AI Strategy**

- **Most effective features:** Generating class skeletons straight from my UML and drafting the test suite were the biggest time-savers. Inline edits with immediate `pytest` feedback let me iterate fast, and asking the assistant to explain generated test code before saving it kept me from committing anything I didn't understand.
- **A suggestion I rejected/modified:** As above, I rejected the `ScheduledTask` class and the multi-helper refactor of `detect_conflicts`, keeping a single readable method with exact-time matching to preserve a clean, explainable design.
- **Separate chat sessions per phase:** Using a fresh session for testing (separate from design and implementation) kept each conversation focused. The testing session only had test files and the scheduler in context, so its suggestions were about edge cases and assertions instead of drifting back into design debates. It also made it easy to pick work back up without scrolling through unrelated history.
- **Lead architect takeaway:** The AI is fast and confident, but it optimizes for a plausible answer, not necessarily *my* design goals. My job was to hold the vision — keep the system simple, decide which constraints mattered, and reject "improvements" that added complexity the project didn't need. AI wrote a lot of the code, but I owned the architecture, the tradeoffs, and the verification.

---

## 4. Testing and Verification

**a. What you tested**

I tested the core "intelligence" of the scheduler across 20 automated tests: sorting correctness (tasks return in chronological `HH:MM` order, with untimed tasks last), recurrence logic (completing a daily task creates a new task for the next day, while non-recurring tasks create no copy), and conflict detection (two tasks at the same exact time are flagged, and distinct times produce no warning). I also tested the core model behavior — task completion, pet task management, owner task aggregation, priority sorting, time-limited planning, and filtering.

These tests were important because they cover exactly the features that make PawPal+ "smart." If sorting, recurrence, or conflict detection silently broke, the whole point of the app would fail, so having them locked down by tests gives me confidence to change other code without fear.

**b. Confidence**

I'm fairly confident — **4 out of 5**. All 20 tests pass, and they cover every core algorithm plus several edge cases (empty times, non-recurring tasks, non-conflicting schedules). I held back from full confidence because a few paths are still untested: case-insensitive pet filtering, unknown recurrence frequencies like "monthly," three-way time conflicts, and duration overlaps (a 30-minute walk at 18:00 overlapping a task at 18:15). Those are the edge cases I would test next.

---

## 5. Reflection

**a. What went well**

I'm most satisfied with the conflict detection and recurrence features working end-to-end and being backed by tests. Seeing the app correctly warn that two tasks clash at 18:00, and watching a completed daily task automatically roll forward to the next day, made the system feel genuinely useful rather than just a data-entry form.

**b. What you would improve**

With another iteration I would add duration-aware conflict detection (comparing start and end times, not just exact matches), let users edit and delete tasks and mark them done directly in the Streamlit UI, and persist data so tasks survive a page refresh. I'd also add tests for the remaining edge cases listed above.

**c. Key takeaway**

The most important thing I learned is that working with powerful AI tools makes *me* the lead architect, not the coder-of-record. The AI can generate code and tests quickly, but keeping the design simple, choosing which constraints mattered, and verifying every change with tests were my responsibility. Good prompts and good judgment mattered more than knowing every line of syntax.
