"""
pawpal_system.py - Core domain logic for PawPal+
Implements Task, Pet, Owner, and Scheduler classes.
"""
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional, Tuple


@dataclass
class Task:
    """Represents an individual pet care activity."""
    description: str
    due_time: str  # Format: "HH:MM" (24-hour time)
    frequency: str = "once"  # "once", "daily", or "weekly"
    is_completed: bool = False
    pet_name: str = ""

    def mark_complete(self) -> None:
        """Marks the task as completed."""
        self.is_completed = True


@dataclass
class Pet:
    """Represents a pet and stores its assigned care tasks."""
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Assigns a task to this pet."""
        task.pet_name = self.name
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Returns all tasks associated with this pet."""
        return list(self.tasks)


@dataclass
class Owner:
    """Represents an owner managing multiple pets."""
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Adds a pet to the owner's care list."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Aggregates and returns tasks across all owned pets."""
        all_tasks: List[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    """Algorithmic organizer that schedules and audits tasks across an Owner's pets."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def get_daily_schedule(self) -> List[Task]:
        """Retrieves all tasks across pets sorted chronologically."""
        return self.sort_by_time(self.owner.get_all_tasks())

    def sort_by_time(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Sorts tasks chronologically using HH:MM due_time."""
        task_list = tasks if tasks is not None else self.owner.get_all_tasks()
        return sorted(
            task_list,
            key=lambda t: datetime.strptime(t.due_time, "%H:%M").time()
        )

    def filter_by_pet(self, pet_name: str) -> List[Task]:
        """Filters all tasks for a specific pet name."""
        return [t for t in self.owner.get_all_tasks() if t.pet_name.lower() == pet_name.lower()]

    def filter_by_status(self, is_completed: bool) -> List[Task]:
        """Filters tasks by completion status."""
        return [t for t in self.owner.get_all_tasks() if t.is_completed == is_completed]

    def detect_conflicts(self) -> List[Tuple[Task, Task]]:
        """Identifies pairs of tasks scheduled at the exact same due time."""
        tasks = self.sort_by_time(self.owner.get_all_tasks())
        conflicts: List[Tuple[Task, Task]] = []
        for i in range(len(tasks)):
            for j in range(i + 1, len(tasks)):
                if tasks[i].due_time == tasks[j].due_time:
                    conflicts.append((tasks[i], tasks[j]))
        return conflicts

    def complete_and_reschedule(self, task: Task) -> Optional[Task]:
        """
        Marks a task complete and generates the subsequent recurring Task if applicable.
        Daily tasks recur for next day; weekly tasks recur 7 days later.
        """
        task.mark_complete()
        freq = task.frequency.lower()

        if freq not in ["daily", "weekly"]:
            return None

        days_ahead = 1 if freq == "daily" else 7
        next_date = (datetime.now() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")

        new_task = Task(
            description=f"{task.description} (Next: {next_date})",
            due_time=task.due_time,
            frequency=task.frequency,
            is_completed=False,
            pet_name=task.pet_name,
        )

        for pet in self.owner.pets:
            if pet.name.lower() == task.pet_name.lower():
                pet.add_task(new_task)
                break

        return new_task