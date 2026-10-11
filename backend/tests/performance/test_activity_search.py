from time import perf_counter
from types import SimpleNamespace

from backend.app.models.activity import ActivityCategory, ActivityStatus
from backend.app.api.activities import search_activities


def _activities(count: int) -> list[SimpleNamespace]:
    return [
        SimpleNamespace(
            id=index,
            title=f"Activity {index}",
            status=ActivityStatus.PUBLISHED,
            category=ActivityCategory.ACADEMIC.value,
            venue="Online",
            max_participants=20,
            volunteer_hours=2,
            registration_url="https://forms.google.com/activity",
            slots=[],
            is_visible_to_students=True,
        )
        for index in range(count)
    ]


# Supports AC-SRCH-08 and the two-second Search response constraint.
def test_AC_SRCH_08_activity_search_benchmark_under_two_seconds() -> None:
    activities = _activities(5_000)

    started_at = perf_counter()
    results = search_activities(
        activities=activities,
        category=ActivityCategory.ACADEMIC.value,
        user={"role": "student"},
    )
    elapsed_seconds = perf_counter() - started_at

    assert len(results) == 5_000
    assert elapsed_seconds < 2
