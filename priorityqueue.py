from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass(order=False)
class Task:
    """
    A simple task model for scheduling.

    priority: higher number = higher priority
    arrival_time: when the task becomes available
    deadline: optional, for reporting or tie-breaking use cases
    """
    task_id: str
    priority: int
    arrival_time: int = 0
    deadline: Optional[int] = None
    payload: str = ""

    def __repr__(self) -> str:
        return f"Task(id={self.task_id}, pr={self.priority}, at={self.arrival_time}, dl={self.deadline})"


class MaxHeapPriorityQueue:
    """
    Max-heap priority queue implemented on top of a Python list (array-based heap).

    Design choice:
    - A list gives O(1) index access and natural parent/child calculations.
    - We maintain a position map {task_id -> index} to support increase/decrease_key efficiently.
    """

    def __init__(self) -> None:
        self._heap: List[Task] = []
        self._pos: Dict[str, int] = {}  # task_id -> index

    def is_empty(self) -> bool:
        return len(self._heap) == 0

    def _higher_priority(self, a: Task, b: Task) -> bool:
        """
        Return True if a should come before b in the max-heap ordering.
        Tie-breakers:
        1) higher priority first
        2) earlier arrival_time first
        3) smaller task_id for deterministic ordering
        """
        if a.priority != b.priority:
            return a.priority > b.priority
        if a.arrival_time != b.arrival_time:
            return a.arrival_time < b.arrival_time
        return a.task_id < b.task_id

    def _swap(self, i: int, j: int) -> None:
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]
        self._pos[self._heap[i].task_id] = i
        self._pos[self._heap[j].task_id] = j

    def _sift_up(self, idx: int) -> None:
        while idx > 0:
            parent = (idx - 1) // 2
            if self._higher_priority(self._heap[idx], self._heap[parent]):
                self._swap(idx, parent)
                idx = parent
            else:
                return

    def _sift_down(self, idx: int) -> None:
        n = len(self._heap)
        while True:
            left = 2 * idx + 1
            if left >= n:
                return
            right = left + 1

            best = left
            if right < n and self._higher_priority(self._heap[right], self._heap[left]):
                best = right

            if self._higher_priority(self._heap[best], self._heap[idx]):
                self._swap(idx, best)
                idx = best
            else:
                return

    def insert(self, task: Task) -> None:
        if task.task_id in self._pos:
            raise ValueError(f"Task with id={task.task_id} already exists in the queue.")

        self._heap.append(task)
        idx = len(self._heap) - 1
        self._pos[task.task_id] = idx
        self._sift_up(idx)

    def extract_max(self) -> Task:
        if self.is_empty():
            raise IndexError("extract_max from empty priority queue")

        top = self._heap[0]
        last = self._heap.pop()
        del self._pos[top.task_id]

        if self._heap:
            self._heap[0] = last
            self._pos[last.task_id] = 0
            self._sift_down(0)

        return top

    def peek_max(self) -> Task:
        if self.is_empty():
            raise IndexError("peek_max from empty priority queue")
        return self._heap[0]

    def increase_key(self, task_id: str, new_priority: int) -> None:
        """
        Increase priority of an existing task and restore heap property.
        Time: O(log n)
        """
        if task_id not in self._pos:
            raise KeyError(f"Task id={task_id} not found.")

        i = self._pos[task_id]
        if new_priority < self._heap[i].priority:
            raise ValueError("increase_key requires new_priority >= current priority")

        self._heap[i].priority = new_priority
        self._sift_up(i)

    def decrease_key(self, task_id: str, new_priority: int) -> None:
        """
        Decrease priority of an existing task and restore heap property.
        Time: O(log n)
        """
        if task_id not in self._pos:
            raise KeyError(f"Task id={task_id} not found.")

        i = self._pos[task_id]
        if new_priority > self._heap[i].priority:
            raise ValueError("decrease_key requires new_priority <= current priority")

        self._heap[i].priority = new_priority
        self._sift_down(i)

    def __len__(self) -> int:
        return len(self._heap)


def simulate_scheduler(tasks: List[Task], max_time: int = 50) -> List[Tuple[int, Task]]:
    """
    Simple discrete-time simulation:
    - At each time t, all tasks with arrival_time == t are inserted.
    - If queue not empty, we execute one task (extract_max) at that time.
    Returns a timeline: list of (time, executed_task).

    This is not meant to be OS-realistic; it's a clear demonstration of PQ operations.
    """
    pq = MaxHeapPriorityQueue()
    by_time: Dict[int, List[Task]] = {}
    for task in tasks:
        by_time.setdefault(task.arrival_time, []).append(task)

    timeline: List[Tuple[int, Task]] = []
    for t in range(max_time + 1):
        for task in by_time.get(t, []):
            pq.insert(task)

        if not pq.is_empty():
            executed = pq.extract_max()
            timeline.append((t, executed))

    return timeline


if __name__ == "__main__":
    demo_tasks = [
        Task("A", priority=3, arrival_time=0, deadline=10),
        Task("B", priority=10, arrival_time=1, deadline=3),
        Task("C", priority=5, arrival_time=1, deadline=8),
        Task("D", priority=10, arrival_time=2, deadline=5),
        Task("E", priority=1, arrival_time=3, deadline=12),
    ]

    timeline = simulate_scheduler(demo_tasks, max_time=6)
    print("Execution timeline (time -> task):")
    for t, task in timeline:
        print(f"t={t}: {task}")
