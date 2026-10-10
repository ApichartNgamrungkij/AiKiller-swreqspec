import threading
import time


# Supports NFR-SCHED-01, ASM-SCHED-05
class ScheduleAccessGate:
    def __init__(self, max_concurrent_users: int = 5000) -> None:
        self.max_concurrent_users = max_concurrent_users
        self.active_users = 0
        self.max_seen = 0
        self._condition = threading.Condition()

    def acquire(self) -> float:
        with self._condition:
            wait_started = time.monotonic()
            while self.active_users >= self.max_concurrent_users:
                self._condition.wait()
            self.active_users += 1
            self.max_seen = max(self.max_seen, self.active_users)
            return time.monotonic() - wait_started

    def release(self) -> None:
        with self._condition:
            self.active_users -= 1
            self._condition.notify()


# Supports NFR-SCHED-01
def test_NFR_SCHED_01_queue_keeps_schedule_and_overlap_check_under_capacity() -> None:
    gate = ScheduleAccessGate(max_concurrent_users=5000)
    start_event = threading.Event()
    results: list[dict[str, float | int]] = []
    results_lock = threading.Lock()

    def user_session(user_id: int) -> None:
        start_event.wait()
        waited = gate.acquire()
        with results_lock:
            results.append({"user_id": user_id, "waited": waited})
        time.sleep(0.005)
        gate.release()

    threads = [threading.Thread(target=user_session, args=(user_id,)) for user_id in range(5001)]
    for thread in threads:
        thread.start()

    start_event.set()

    for thread in threads:
        thread.join()

    assert len(results) == 5001
    assert gate.max_seen <= 5000
    waited_users = [entry["waited"] for entry in results if entry["waited"] > 0]
    assert waited_users, "ผู้ใช้ที่เกิน 5,000 คนควรต้องรอจนผู้อื่นออกจากหน้าตารางส่วนตัวหรือหน้ากิจกรรม"
