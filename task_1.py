import random
import time
from functools import lru_cache


def range_sum_no_cache(arr, left, right):
    return sum(arr[left:right + 1])


def update_no_cache(arr, index, value):
    arr[index] = value


class SmartCachedRange:

    def __init__(self, arr, cache_size=1000):
        self.arr = arr
        self._version = 0

        @lru_cache(maxsize=cache_size)
        def _cached_sum(version, left, right):
            return sum(self.arr[left:right + 1])

        self._cached_sum = _cached_sum

    def range_sum(self, left, right):
        if left > right:
            left, right = right, left
        return self._cached_sum(self._version, left, right)

    def update(self, index, value):
        self.arr[index] = value
        self._version += 1


def generate_queries(n, q, seed=0):
    random.seed(seed)
    queries = []

    for _ in range(q):
        if random.choice(["Range", "Update"]) == "Range":
            l = random.randint(0, n - 1)
            r = random.randint(l, n - 1)
            queries.append(("Range", l, r))
        else:
            idx = random.randint(0, n - 1)
            val = random.randint(1, 100)
            queries.append(("Update", idx, val))

    return queries


def main():
    N = 100_000
    Q = 50_000

    base_array = [random.randint(1, 100) for _ in range(N)]
    queries = generate_queries(N, Q)

    # Без кешу
    arr_no_cache = base_array.copy()
    start = time.perf_counter()
    for kind, a, b in queries:
        if kind == "Range":
            range_sum_no_cache(arr_no_cache, a, b)
        else:
            update_no_cache(arr_no_cache, a, b)
    end = time.perf_counter()
    no_cache_time = end - start

    # З кешем
    arr_cache = base_array.copy()
    cached_ops = SmartCachedRange(arr_cache)

    start = time.perf_counter()
    for kind, a, b in queries:
        if kind == "Range":
            cached_ops.range_sum(a, b)
        else:
            cached_ops.update(a, b)
    end = time.perf_counter()
    cache_time = end - start

    print(f"Час виконання без кешування: {no_cache_time:.2f} секунд")
    print(f"Час виконання з LRU-кешем:   {cache_time:.2f} секунд")


if __name__ == "__main__":
    main()
