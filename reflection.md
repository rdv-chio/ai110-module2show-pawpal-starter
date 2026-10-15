# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
- The initial design defined four core entities: `Task`, `Pet`, `Owner`, and `Scheduler`.
- `Task` models an individual care item with timing and completion state. `Pet` maintains a collection of its own tasks. `Owner` acts as the aggregate root holding multiple pets and exposing `get_all_tasks()`. `Scheduler` serves as the logic engine that inspects the owner's aggregated tasks without modifying underlying pet ownership structures.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
- Initially, the scheduler could have been implemented by passing a list of tasks directly. I updated the architecture so `Scheduler` explicitly takes an `Owner` instance as an dependency. This guarantees that multi-pet scheduling operates through the owner's domain boundary rather than an untyped list of disconnected task objects.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
- The scheduler considers exact due times (`HH:MM` format), recurrence frequencies (`once`, `daily`, `weekly`), and pet associations.
- Chronological execution was prioritized first because real-world pet care (such as medication and feeding schedules) is time-critical.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
- Conflict detection checks for exact time matches (`time_a == time_b`) rather than time-interval overlapping durations (e.g., 30-minute blocks).
- This is reasonable for this scenario because it keeps task input friction minimal while still alerting an owner that two separate care activities are demanded at the exact same moment.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
- AI was used as a system co-architect to draft initial class skeletons, scaffold unit test fixtures, and translate domain boundaries into Mermaid.js UML specifications.
- Prompts that specified interface signatures and structural constraints (e.g., "Implement Scheduler to retrieve tasks via Owner.get_all_tasks() rather than a single Pet") produced the most reliable results.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
- The AI initially suggested storing tasks in a single global list inside `Scheduler`. I rejected this because it broke the OOP model where pets own their care routines and owners manage their pets. I retained the hierarchical relationship `Owner -> Pet -> Task` and had the scheduler act as an operational layer.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?
- Verified task completion state transitions, multi-pet task aggregation via the owner, chronological sorting across different pets, exact-match conflict detection, and recurrence date calculation with automatic re-queuing.
- These tests were critical to verify that multi-pet interactions function properly before integrating the logic into Streamlit's state cycle.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?
- Confidence: 5/5 for the core domain requirements.
- Future edge cases to test include handling cross-midnight intervals, invalid 24-hour time strings, and timezone differences.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
- The CLI-first workflow with `main.py` and automated `pytest` suites allowed fast verification without wrestling with UI reruns or state resets.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
- In a next iteration, I would add duration intervals to support schedule overlap detection and JSON persistence to preserve pets across restarts.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
- Designing clear domain boundaries up front makes writing tests and attaching user interfaces straightforward, while using AI as a design partner works best when you dictate class relationships rather than letting the AI decide system boundaries.