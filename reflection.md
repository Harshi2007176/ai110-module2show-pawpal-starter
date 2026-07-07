# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My initial UML design consists of five classes: Owner, Pet, Task, Scheduler, and DailyPlan. The Owner class stores the owner's name, their list of pets, and their preferences, and is responsible for adding pets and collecting tasks across all of them. The Pet class stores each pet's name, species, age, and list of tasks, and is responsible for adding, removing, and retrieving its own tasks. The Task class holds the details of a single care activity — its name, category, duration, priority, whether it recurs, a preferred time, and completion status — and is responsible for marking itself done. The Scheduler class acts as the core logic of the system, taking in all tasks and available time to sort by priority, detect conflicts, generate a daily plan, and explain its scheduling decisions. Finally, the DailyPlan class stores the finished schedule, including the date, ordered tasks, and total time used, and is responsible for displaying the plan. Together, these classes form a clear structure where an Owner has many Pets, each Pet has many Tasks, and the Scheduler organizes those Tasks into a DailyPlan.

**b. Design changes**

Yes, my design changed after reviewing the skeleton with AI feedback. The AI pointed out that DailyPlan.scheduled_tasks only stored Task objects with no way to record when each task was actually scheduled, which would make real conflict detection impossible. To fix this, I [changed scheduled_tasks to store each task alongside a start time / added a ScheduledTask class pairing a task with a start time]. I also renamed duration to duration_minutes for clarity, since the original name didn't specify units.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

One tradeoff my scheduler makes is that conflict detection only checks for exact matching task times, such as two tasks both scheduled at 18:00. It does not yet check for overlapping durations, like a 30-minute walk at 18:00 conflicting with a feeding at 18:15. I asked AI how the algorithm could be simplified, and it suggested breaking the conflict logic into smaller helper methods. I decided to keep the current version because it is still readable for this project and avoids making the code feel more complicated than the assignment needs.

This tradeoff is reasonable because PawPal+ is a beginner-friendly scheduling app, and exact-time warnings already help the pet owner notice obvious conflicts. A more advanced version could compare start and end times, but the current approach keeps the logic easier to explain, test, and maintain.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
