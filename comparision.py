from __future__ import annotations
import random
import statistics
import time
from typing import Callable, List, Tuple

from heapsort import heapsort


def mergesort(a: List[int]) -> List[int]:
    """
    Iterative (bottom-up) merge sort to avoid recursion depth issues.
    Returns a new sorted list.
    """
    n = len(a)
    if n <= 1:
        return list(a)

    src = list(a)
    dst = [0] * n

    width = 1
    while width < n:
        for left in range(0, n, 2 * width):
            mid = min(left + width, n)
            right = min(left + 2 * width, n)

            i, j, k = left, mid, left
            while i < mid and j < right:
                if src[i] <= src[j]:
                    dst[k] = src[i]
                    i += 1
                else:
                    dst[k] = src[j]
                    j += 1
                k += 1

            while i < mid:
                dst[k] = src[i]
                i += 1
                k += 1

            while j < right:
                dst[k] = src[j]
                j += 1
                k += 1

        src, dst = dst, src
        width *= 2

    return src


def quicksort(a: List[int]) -> List[int]:
    """
    Randomized 3-way Quicksort (handles duplicates well).
    """
    arr = list(a)
    _quicksort_3way(arr, 0, len(arr) - 1)
    return arr


def _quicksort_3way(a: List[int], lo: int, hi: int) -> None:
    while lo < hi:
        # random pivot
        pivot_index = random.randint(lo, hi)
        pivot = a[pivot_index]

        # 3-way partition: < pivot | == pivot | > pivot
        lt, i, gt = lo, lo, hi
        while i <= gt:
            if a[i] < pivot:
                a[lt], a[i] = a[i], a[lt]
                lt += 1
                i += 1
            elif a[i] > pivot:
                a[i], a[gt] = a[gt], a[i]
                gt -= 1
            else:
                i += 1

        # Now recurse on smaller side first (keeps recursion depth low)
        left_size = lt - lo
        right_size = hi - gt

        if left_size < right_size:
            _quicksort_3way(a, lo, lt - 1)
            lo = gt + 1   # tail-call elimination (loop)
        else:
            _quicksort_3way(a, gt + 1, hi)
            hi = lt - 1


def gen_data(n: int, kind: str) -> List[int]:
    if kind == "random":
        return [random.randint(0, n) for _ in range(n)]
    if kind == "sorted":
        return list(range(n))
    if kind == "reverse":
        return list(range(n, 0, -1))
    if kind == "few_unique":
        # Many duplicates (interesting for some algorithms)
        return [random.randint(0, 10) for _ in range(n)]
    raise ValueError(f"Unknown kind: {kind}")


def time_func(fn: Callable[[List[int]], List[int]], data: List[int], trials: int = 7) -> float:
    """
    Returns median runtime in milliseconds over 'trials'.
    """
    times = []
    for _ in range(trials):
        arr = list(data)
        t0 = time.perf_counter()
        out = fn(arr)
        t1 = time.perf_counter()
        # correctness check (cheap sanity)
        if out != sorted(arr):
            raise AssertionError(f"{fn.__name__} produced incorrect output.")
        times.append((t1 - t0) * 1000)
    return statistics.median(times)


def run() -> None:
    algos: List[Tuple[str, Callable[[List[int]], List[int]]]] = [
        ("Heapsort", heapsort),
        ("Quicksort (rand)", quicksort),
        ("Merge Sort", mergesort),
    ]

    sizes = [1_000, 5_000, 10_000, 20_000]
    kinds = ["random", "sorted", "reverse", "few_unique"]

    print("Median time (ms) over 7 trials\n")

    for kind in kinds:
        print(f"=== Data distribution: {kind} ===")
        for n in sizes:
            data = gen_data(n, kind)
            row = [f"n={n:>6}"]
            for name, fn in algos:
                ms = time_func(fn, data, trials=7)
                row.append(f"{name}: {ms:8.2f}")
            print(" | ".join(row))
        print()


if __name__ == "__main__":
    run()
