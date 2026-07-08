import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")

if "owner" not in st.session_state:
    st.session_state["owner"] = Owner(name=owner_name)

owner = st.session_state["owner"]
owner.name = owner_name

st.markdown("### Pets")

with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    age = st.number_input("Age", min_value=0, max_value=30, value=2)
    submitted_pet = st.form_submit_button("Add pet")

if submitted_pet:
    owner.add_pet(Pet(name=pet_name, species=species, age=int(age)))
    st.success(f"Added {pet_name}.")

if owner.pets:
    pet_rows = [
        {"Name": pet.name, "Species": pet.species, "Age": pet.age}
        for pet in owner.pets
    ]
    st.table(pet_rows)
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")

if owner.pets:
    pet_options = [
        f"{index + 1}. {pet.name} ({pet.species})"
        for index, pet in enumerate(owner.pets)
    ]
    selected_pet_label = st.selectbox("Pet", pet_options)
    selected_pet_index = pet_options.index(selected_pet_label)
    selected_pet = owner.pets[selected_pet_index]

    with st.form("add_task_form"):
        task_title = st.text_input("Task title", value="Morning walk")
        category = st.selectbox(
            "Category",
            ["walk", "feeding", "medication", "grooming", "enrichment"],
        )
        duration = st.number_input(
            "Duration (minutes)",
            min_value=1,
            max_value=240,
            value=20,
        )
        priority = st.slider("Priority", min_value=1, max_value=5, value=3)
        preferred_time = st.selectbox(
            "Preferred time",
            ["morning", "afternoon", "evening", "anytime"],
        )
        scheduled_time = st.time_input("Scheduled time (HH:MM)", value=None)
        submitted_task = st.form_submit_button("Add task")

    if submitted_task:
        selected_pet.add_task(
            Task(
                name=task_title,
                category=category,
                duration=int(duration),
                priority=int(priority),
                preferred_time=preferred_time,
                time=scheduled_time.strftime("%H:%M") if scheduled_time else None,
            )
        )
        st.success(f"Added {task_title} for {selected_pet.name}.")

    all_tasks = owner.get_all_tasks()
    if all_tasks:
        task_rows = []
        for pet in owner.pets:
            for task in pet.get_tasks():
                task_rows.append(
                    {
                        "Pet": pet.name,
                        "Task": task.name,
                        "Category": task.category,
                        "Duration": task.duration,
                        "Priority": task.priority,
                        "Time": task.time or "—",
                        "Preferred time": task.preferred_time,
                        "Done": "✅" if task.is_done else "⬜",
                    }
                )
        st.write("Current tasks:")
        st.table(task_rows)
    else:
        st.info("No tasks yet. Add one above.")
else:
    st.info("Add a pet before scheduling tasks.")

st.divider()

st.subheader("Build Schedule")
available_time = st.number_input(
    "Available time today (minutes)",
    min_value=1,
    max_value=480,
    value=60,
)

if st.button("Generate schedule"):
    scheduler = Scheduler(owner, available_time=int(available_time))
    plan = scheduler.generate_daily_plan()
    conflicts = scheduler.detect_conflicts()

    # --- Conflict warnings: surface first, one actionable warning per conflict ---
    st.markdown("### ⚠️ Conflict Check")
    if conflicts:
        st.warning(
            f"Found {len(conflicts)} scheduling conflict(s). "
            "Consider moving one of the overlapping tasks to a different time."
        )
        for conflict in conflicts:
            st.warning(f"🔁 {conflict}")
    else:
        st.success("No scheduling conflicts found. You're all set! 🎉")

    # --- Today's plan as a professional table + summary metrics ---
    st.markdown("### 🗓️ Today's Schedule")
    if plan.scheduled_tasks:
        plan_rows = [
            {
                "Task": task.name,
                "Category": task.category,
                "Time": task.time or "—",
                "Duration (min)": task.duration,
                "Priority": task.priority,
            }
            for task in plan.scheduled_tasks
        ]
        st.table(plan_rows)

        col1, col2, col3 = st.columns(3)
        col1.metric("Tasks scheduled", len(plan.scheduled_tasks))
        col2.metric("Time used", f"{plan.total_time_used} min")
        col3.metric("Time free", f"{int(available_time) - plan.total_time_used} min")
    else:
        st.info("No tasks fit in the available time. Add tasks or increase available time.")

    # --- Sorted views using Scheduler sorting methods ---
    st.markdown("### 🔀 All Tasks, Sorted")
    sort_choice = st.radio(
        "Sort by",
        ["Priority (high → low)", "Time (early → late)"],
        horizontal=True,
    )
    if sort_choice.startswith("Priority"):
        sorted_tasks = scheduler.sort_by_priority()
    else:
        sorted_tasks = scheduler.sort_by_time()

    if sorted_tasks:
        st.table(
            [
                {
                    "Task": task.name,
                    "Time": task.time or "—",
                    "Priority": task.priority,
                    "Duration (min)": task.duration,
                    "Status": "✅ Done" if task.is_done else "⬜ Open",
                }
                for task in sorted_tasks
            ]
        )

    # --- Filter: what's still outstanding ---
    incomplete = scheduler.filter_by_status(is_done=False)
    st.markdown(f"### 📋 Outstanding Tasks ({len(incomplete)})")
    if incomplete:
        for task in incomplete:
            st.write(f"- {task.name} ({task.duration} min, priority {task.priority})")
    else:
        st.success("Everything is done. Nice work! 🐾")

    # --- Plan reasoning ---
    st.markdown("### 💡 Reasoning")
    st.info(scheduler.explain_plan())
