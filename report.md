# Assignment 4: Heap Data Structures — Implementation, Analysis, and Applications

## Introduction

The objective of this assignment was to implement and analyze heap-based algorithms, specifically Heapsort and a Priority Queue using a binary heap, and compare their behavior with other sorting techniques.

---

# Part I: Heapsort Implementation and Analysis

## Heapsort Implementation

### Design Approach

I implemented Heapsort using an array-based max-heap represented with a Python list. A list was chosen because:

- It allows O(1) index access.
- Parent/child relationships are easy to compute:
  - Parent index = `(i - 1)/ 2`
  - Left child = `2i + 1`
  - Right child = `2i + 2`
- It avoids pointer overhead found in tree-based structures.

The algorithm consists of two main phases:

### Phase 1: Build Max Heap

- Starting from the last non-leaf node `(n/2 - 1)` down to index `0`
- Apply sift_down() to enforce the heap property
- This transforms the array into a valid max-heap

### Phase 2: Extract Maximum Repeatedly

- Swap the root (maximum element) with the last element
- Reduce the heap size
- Restore heap property using sift_down()
- Repeat until fully sorted

This produces the array in ascending order.

---

## Time Complexity Analysis of Heapsort

### Build Heap 

Although it may appear that building the heap requires `n log n`, the bottom-up heap construction actually runs in **O(n)** time.

This happens because:

- Most nodes are near the bottom of the heap.
- Nodes near the bottom require very little shifting.
- The total amount of work forms a converging series.

So: Build Heap = **O(n)**

---

### Extraction Phase 

- We perform `n - 1` extractions.
- Each extraction requires at most `log n` comparisons (heap height).

Therefore:
Extraction Phase = `n × log n`  = **O(n log n)**

---

### Overall Time Complexity

| Case | Complexity |
|------|------------|
| Best Case | O(n log n) |
| Average Case | O(n log n) |
| Worst Case | O(n log n) |

Heapsort’s runtime does not depend on input order, making it very predictable.

---

### Space Complexity

- The heap is stored directly in the array.
- The algorithm can run in-place.
- Auxiliary space complexity: **O(1)** (excluding input copy).

Compared to Merge Sort (which requires O(n) extra memory), Heapsort is more memory-efficient.

---

# Comparison

## Experimental Setup

To compare performance, I implemented:

- Heapsort
- Randomized Quicksort (3-way partition)
- Merge Sort (iterative bottom-up)

For each configuration:

- 7 trials were executed
- Median runtime (milliseconds) was recorded
- Input sizes tested: 1,000 to 20,000
- Data distributions:
  - Random
  - Sorted
  - Reverse Sorted
  - Few Unique (many duplicates)

---

## Results

### Table 1  
**Median Runtime (ms) — Random & Few-Unique Inputs**

| Distribution | n     | Heapsort | Quicksort (3-way) | Merge Sort |
|-------------|------:|---------:|------------------:|-----------:|
| Random      | 1,000  | 2.13 | 1.43 | 1.23 |
| Random      | 5,000  | 6.85 | 5.62 | 5.32 |
| Random      | 10,000 | 22.46 | 19.36 | 16.77 |
| Random      | 20,000 | 52.97 | 40.83 | 37.08 |
| Few Unique  | 1,000  | 1.38 | 0.29 | 1.12 |
| Few Unique  | 5,000  | 8.30 | 1.06 | 5.02 |
| Few Unique  | 10,000 | 18.31 | 3.36 | 15.05 |
| Few Unique  | 20,000 | 38.87 | 5.87 | 31.75 |

---

### Table 2  
**Median Runtime (ms) — Sorted & Reverse Inputs**

| Distribution | n     | Heapsort | Quicksort (3-way) | Merge Sort |
|-------------|------:|---------:|------------------:|-----------:|
| Sorted      | 1,000  | 1.53 | 1.64 | 1.06 |
| Sorted      | 5,000  | 10.65 | 10.15 | 6.99 |
| Sorted      | 10,000 | 24.09 | 21.06 | 9.01 |
| Sorted      | 20,000 | 49.16 | 44.02 | 32.50 |
| Reverse     | 1,000  | 1.39 | 1.56 | 1.05 |
| Reverse     | 5,000  | 9.70 | 9.98 | 6.88 |
| Reverse     | 10,000 | 21.81 | 19.80 | 13.95 |
| Reverse     | 20,000 | 47.21 | 49.35 | 31.66 |

---

## Analysis of Results

### Random Data

Merge Sort performed best for large random inputs. Its predictable splitting strategy and stable merging provide consistent performance.

Heapsort was slightly slower due to repeated heap adjustments and less cache-friendly access patterns.

---

### Sorted and Reverse Inputs

Merge Sort clearly outperformed the others at larger sizes. Since it always divides evenly, input order does not impact its performance.

Heapsort remained consistent but slower overall.

---

### Few Unique (Many Duplicates)

Quicksort dramatically outperformed both Heapsort and Merge Sort.

For example, at n = 20,000:

- Quicksort: **5.87 ms**
- Merge Sort: 31.75 ms
- Heapsort: 38.87 ms

This occurred because the 3-way partition groups duplicate values together, significantly reducing recursive depth and comparisons.

---

## Key Observations

- All three algorithms are theoretically O(n log n).
- Real-world performance depends on:
  - Constant factors
  - Memory access patterns
  - Input distribution
- Merge Sort was the most stable performer.
- Quicksort was fastest when duplicates were present.
- Heapsort was the most consistent but rarely the fastest.

---

# PART II: Priority Queue Implementation and Applications

### Data Structure

I implemented a max-heap priority queue using:

- Python list (array-based heap)
- A position map (`task_id → index`) for efficient key updates

This design allows efficient heap operations while maintaining clean structure.

---

Each task includes:

- `task_id`
- `priority`
- `arrival_time`
- `deadline`
- optional metadata

Higher numeric values represent higher priority.

---

## Core Operations and Complexity

| Operation | Time Complexity |
|------------|----------------|
| insert() | O(log n) |
| extract_max() | O(log n) |
| increase_key() | O(log n) |
| decrease_key() | O(log n) |
| is_empty() | O(1) |

Because the heap height is `log n`, any upward or downward adjustment is bounded by that height.

---

## Scheduler Simulation

I implemented a simple discrete-time scheduler:

- Tasks are inserted at their arrival time.
- At each time step, the highest-priority task is executed.
- The priority queue dynamically manages ordering.

This model simulates real-world systems such as:

- CPU scheduling
- Job dispatch systems
- Event-driven simulators
- Network packet prioritization

The simulation confirmed that tasks with higher priority are always processed first while maintaining efficient runtime.

---

# Conclusion

- Heapsort guarantees O(n log n) performance regardless of input.
- Implementation details significantly affect real performance.
- 3-way partitioning greatly improves Quicksort with duplicates.
- Binary heaps provide an efficient foundation for priority queues.
- Heap-based scheduling models reflect real operating system and system design principles.

