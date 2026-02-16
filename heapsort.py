from __future__ import annotations
from typing import List


def _sift_down(a: List[int], start: int, end: int) -> None:
    """
    Restore max-heap property in a[start:end+1], assuming children are already heaps.
    """
    root = start
    while True:
        left = 2 * root + 1
        if left > end:
            return

        right = left + 1
        # Pick the larger child
        child = left
        if right <= end and a[right] > a[left]:
            child = right

        if a[child] > a[root]:
            a[root], a[child] = a[child], a[root]
            root = child
        else:
            return


def _build_max_heap(a: List[int]) -> None:
    """
    Turn list a into a max-heap in-place.
    """
    n = len(a)
    # Last parent index = (n//2) - 1
    for i in range((n // 2) - 1, -1, -1):
        _sift_down(a, i, n - 1)


def heapsort(a: List[int]) -> List[int]:
    """
    Sorts and returns a new list using Heapsort.
    """
    arr = list(a)  # keep original unchanged
    n = len(arr)
    if n <= 1:
        return arr

    _build_max_heap(arr)

    # Repeatedly move max to end and re-heap
    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        _sift_down(arr, 0, end - 1)

    return arr


if __name__ == "__main__":
    data = [5, 1, 8, 3, 2, 9, 4]
    print("Original:", data)
    print("Sorted  :", heapsort(data))
