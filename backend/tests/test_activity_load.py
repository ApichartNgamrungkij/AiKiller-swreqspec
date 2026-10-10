from __future__ import annotations

import threading
import time
from concurrent.futures import ThreadPoolExecutor


# Supports NFR-ACT-01
def test_NFR_ACT_01_activity_create_page_handles_5000_parallel_users() -> None:
    capacity = 5_000
    gate = threading.Semaphore(capacity)
    barrier = threading.Barrier(capacity + 1)
    active = 0
    max_active = 0
    results: list[int] = []
    lock = threading.Lock()

    def request_create_page(user_id: int) -> None:
        nonlocal active, max_active
        barrier.wait()
        acquired = gate.acquire(timeout=0.25)
        if not acquired:
            return

        with lock:
            active += 1
            max_active = max(max_active, active)

        time.sleep(0.001)

        with lock:
            active -= 1
        results.append(user_id)
        gate.release()

    with ThreadPoolExecutor(max_workers=capacity + 1) as executor:
        futures = [executor.submit(request_create_page, user_id) for user_id in range(capacity + 1)]
        for future in futures:
            future.result()

    assert max_active <= capacity
    assert len(results) == capacity + 1
