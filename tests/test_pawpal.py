"""
tests/test_pawpal.py - Unit and behavioral tests for PawPal+
"""
import pytest
from pawpal_system import Owner, Pet, Task, Scheduler


@pytest.fixture
def populated_system():
    owner = Owner(name="Rocio")
    lowe = Pet(name="Lowe", species="Cat")
    betito = Pet(name="Betito", species="Cat")
    owner.add_pet(lowe)
    owner.add_pet(betito)

    t1 = Task(description="Evening food", due_time="18:00", frequency="daily")
    t2 = Task(description="Morning medication", due_time="08:00", frequency="daily")
    t3 = Task(description="Ear drops", due_time="08:00", frequency="once")

    lowe.add_task(t1)
    lowe.add_task(t2)
    betito.add_task(t3)

    scheduler = Scheduler(owner=owner)
    return owner, lowe, betito, scheduler


def test_task_completion():
    task = Task(description="Grooming", due_time="10:00")
    assert not task.is_completed
    task.mark_complete()
    assert task.is_completed


def test_pet_task_aggregation(populated_system):
    owner, lowe, betito, _ = populated_system
    all_tasks = owner.get_all_tasks()
    assert len(all_tasks) == 3
    assert len(lowe.get_tasks()) == 2
    assert len(betito.get_tasks()) == 1


def test_chronological_sorting(populated_system):
    _, _, _, scheduler = populated_system
    sorted_tasks = scheduler.get_daily_schedule()
    times = [t.due_time for t in sorted_tasks]
    assert times == ["08:00", "08:00", "18:00"]


def test_conflict_detection(populated_system):
    _, _, _, scheduler = populated_system
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 1
    t_a, t_b = conflicts[0]
    assert t_a.due_time == "08:00"
    assert t_b.due_time == "08:00"
    assert {t_a.pet_name, t_b.pet_name} == {"Lowe", "Betito"}


def test_recurrence_daily(populated_system):
    owner, lowe, _, scheduler = populated_system
    med_task = [t for t in lowe.get_tasks() if "medication" in t.description][0]
    initial_count = len(lowe.get_tasks())

    new_task = scheduler.complete_and_reschedule(med_task)
    assert med_task.is_completed
    assert new_task is not None
    assert "Next:" in new_task.description
    assert len(lowe.get_tasks()) == initial_count + 1