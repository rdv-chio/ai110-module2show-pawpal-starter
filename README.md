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

```Plaintext
🐾 Starting PawPal+ CLI Demonstration
========================================

📅 Aggregated Schedule (Chronological Order):
  [08:00] Lowe     - Morning oral medication        (daily) [○ Pending]
  [08:00] Betito   - Administer ear drops           (once) [○ Pending]
  [14:00] Betito   - Brushing and coat grooming     (weekly) [○ Pending]
  [18:00] Lowe     - Evening wet food               (daily) [○ Pending]

⚠️ Conflict Detection Check:
  * Conflict at 08:00: 'Morning oral medication' (Lowe) vs 'Administer ear drops' (Betito)

🔄 Completing Task and Generating Next Occurrence:
  Completing: Morning oral medication for Lowe...
  Original Status: Completed
  Generated Next Task: 'Morning oral medication (Next: 2026-10-15)' at 08:00

========================================
✅ PawPal+ CLI Demo execution finished successfully.
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest -v
```

Sample test output:

```Plaintext
================================================= test session starts ==================================================
platform linux -- Python 3.11.15, pytest-9.1.1, pluggy-1.6.0
rootdir: /mnt/d/code/codepath/ai110/ai110-module2show-pawpal-starter
collected 5 items

tests/test_pawpal.py::test_task_completion PASSED                                                                [ 20%]
tests/test_pawpal.py::test_pet_task_aggregation PASSED                                                           [ 40%]
tests/test_pawpal.py::test_chronological_sorting PASSED                                                          [ 60%]
tests/test_pawpal.py::test_conflict_detection PASSED                                                             [ 80%]
tests/test_pawpal.py::test_recurrence_daily PASSED                                                               [100%]

================================================== 5 passed in 0.18s ===================================================
```

**Confidence Level:** ⭐⭐⭐⭐⭐ (5/5) — All primary OOP aggregation pathways, 24-hour time sorting, conflict detection pairs, and recurrence calculations pass automated verification.

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Parses `due_time` strings (`HH:MM`) into `datetime.time` objects for chronological sorting across multiple pets. |
| Filtering | `Scheduler.filter_by_pet()`, `Scheduler.filter_by_status()` | Filters aggregated tasks by matching pet name or completion state (`is_completed`). |
| Conflict handling | `Scheduler.detect_conflicts()` | Scans aggregated tasks across all pets and returns tuples of tasks sharing identical execution times. |
| Recurring tasks | `Scheduler.complete_and_reschedule()` | Marks a task complete and, if `daily` or `weekly`, schedules the next occurrence with an offset date. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. **Initialize State:** The app launches with owner "Rocio" and two registered pets ("Lowe" and "Betito") in `st.session_state`.
2. **Review Aggregated Timeline:** All tasks across all pets are pulled via `Owner.get_all_tasks()` and displayed chronologically.
3. **Conflict Awareness:** The UI immediately flags simultaneous tasks (e.g., both Lowe and Betito having care items scheduled at 08:00) using `st.warning`.
4. **Interactive Completion:** Clicking the "Complete" button triggers `complete_and_reschedule()`, marking the current task done and inserting tomorrow's instance into the schedule.
5. **Add Pet / Add Task:** The sidebar provides forms to register additional pets or schedule tasks on the fly, dynamically updating the master schedule upon rerun.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
