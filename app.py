import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

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

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    due_time = st.text_input("Due Time (HH:MM)", value="08:00")
with col3:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col4:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

# Fix 1: Include due_time when button is clicked
if st.button("Add task"):
    st.session_state.tasks.append(
        {"title": task_title, "due_time": due_time, "duration_minutes": int(duration), "priority": priority}
    )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

#if st.button("Generate schedule"):
#    st.warning(
#        "Not implemented yet. Next step: create your scheduling logic (classes/functions) and call it here."
#    )
#    st.markdown()
"""
Suggested approach:
1. Design your UML (draft).
2. Create class stubs (no logic).
3. Implement scheduling behavior.
4. Connect your scheduler here and display results.
"""
if st.button("Generate schedule"):
    if not st.session_state.tasks:
        st.warning("Please add at least one task first.")
    else:
        # 1. Build domain objects
        owner = Owner(name=owner_name)
        pet = Pet(name=pet_name, species=species)
        for t in st.session_state.tasks:
            # Default to "08:00" if no due_time was provided
            time_val = t.get("due_time", "08:00")
            pet.add_task(Task(description=t["title"], due_time=time_val))
        owner.add_pet(pet)

        # 2. Run scheduler logic
        scheduler = Scheduler(owner=owner)

        # 3. Check for conflicts
        conflicts = scheduler.detect_conflicts()
        if conflicts:
            for a, b in conflicts:
                st.warning(f"⚠️ Conflict at {a.due_time}: '{a.description}' overlaps with '{b.description}'")

        # 4. Display sorted schedule
        st.success(f"Generated schedule for {pet.name} ({owner.name}'s pet):")
        sorted_tasks = scheduler.get_daily_schedule()
        display_data = [
            {"Time": t.due_time, "Task": t.description, "Status": "Pending"}
            for t in sorted_tasks
        ]
        st.table(display_data)