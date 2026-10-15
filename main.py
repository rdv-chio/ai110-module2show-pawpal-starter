"""
main.py - CLI demonstration verifying pawpal_system.py logic.
"""
from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    print("🐾 Starting PawPal+ CLI Demonstration\n" + "=" * 40)

    # 1. Instantiate Owner and Pets
    owner = Owner(name="Rocio")
    lowe = Pet(name="Lowe", species="Cat")
    betito = Pet(name="Betito", species="Cat")
    owner.add_pet(lowe)
    owner.add_pet(betito)

    # 2. Add tasks across multiple pets (out of order, including a conflict)
    t1 = Task(description="Evening wet food", due_time="18:00", frequency="daily")
    t2 = Task(description="Morning oral medication", due_time="08:00", frequency="daily")
    t3 = Task(description="Brushing and coat grooming", due_time="14:00", frequency="weekly")
    t4 = Task(description="Administer ear drops", due_time="08:00", frequency="once")  # Same time as t2

    lowe.add_task(t1)
    lowe.add_task(t2)
    betito.add_task(t3)
    betito.add_task(t4)

    # 3. Instantiate Scheduler and sort
    scheduler = Scheduler(owner=owner)
    print("\n📅 Aggregated Schedule (Chronological Order):")
    sorted_tasks = scheduler.get_daily_schedule()
    for task in sorted_tasks:
        status = "✓ Done" if task.is_completed else "○ Pending"
        print(f"  [{task.due_time}] {task.pet_name:<8} - {task.description:<30} ({task.frequency}) [{status}]")

    # 4. Conflict Detection
    print("\n⚠️ Conflict Detection Check:")
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for a, b in conflicts:
            print(f"  * Conflict at {a.due_time}: '{a.description}' ({a.pet_name}) vs '{b.description}' ({b.pet_name})")
    else:
        print("  No scheduling conflicts detected.")

    # 5. Task Completion & Recurrence
    print("\n🔄 Completing Task and Generating Next Occurrence:")
    print(f"  Completing: {t2.description} for {t2.pet_name}...")
    next_task = scheduler.complete_and_reschedule(t2)
    print(f"  Original Status: {'Completed' if t2.is_completed else 'Incomplete'}")
    if next_task:
        print(f"  Generated Next Task: '{next_task.description}' at {next_task.due_time}")

    print("\n" + "=" * 40 + "\n✅ PawPal+ CLI Demo execution finished successfully.")


if __name__ == "__main__":
    main()