import { useEffect, useState } from 'react'

import type { MockActivity } from '../mocks/activities'

type ActivityStatus = MockActivity['status']

type ActivityStatusResponse = {
  status?: unknown
  bookedSlots?: unknown
  availableSlots?: unknown
}

type ActivityStatusState = {
  status: ActivityStatus
  bookedSlots: number
  error: string | null
}

function normalizeStatus(payload: ActivityStatusResponse, fallback: ActivityStatusState): ActivityStatusState {
  const bookedSlots = typeof payload.bookedSlots === 'number' ? payload.bookedSlots : fallback.bookedSlots
  const availableSlots =
    typeof payload.availableSlots === 'number' ? payload.availableSlots : bookedSlots
  const status: ActivityStatus =
    payload.status === 'full' || (availableSlots > 0 && bookedSlots >= availableSlots) ? 'full' : 'open'

  return { status, bookedSlots, error: null }
}

// Supports FR-SRCH-01 and the IF status refresh constraint.
export function useActivityStatus(
  activityId: number,
  initialActivity: Pick<MockActivity, 'status' | 'bookedSlots' | 'availableSlots'>,
  pollIntervalMs = 60_000,
): ActivityStatusState {
  const [state, setState] = useState<ActivityStatusState>({
    status: initialActivity.status,
    bookedSlots: initialActivity.bookedSlots,
    error: null,
  })

  useEffect(() => {
    let active = true

    const refresh = async () => {
      try {
        const response = await fetch(`/api/activities/${activityId}`)
        if (!response.ok) {
          throw new Error(`ไม่สามารถอัปเดตสถานะกิจกรรมได้ (${response.status})`)
        }
        const payload = (await response.json()) as ActivityStatusResponse
        if (active) {
          setState((previous) =>
            normalizeStatus(
              { ...payload, availableSlots: payload.availableSlots ?? initialActivity.availableSlots },
              previous,
            ),
          )
        }
      } catch (reason: unknown) {
        if (active) {
          setState((previous) => ({
            ...previous,
            error: reason instanceof Error ? reason.message : 'ไม่สามารถอัปเดตสถานะกิจกรรมได้',
          }))
        }
      }
    }

    const intervalId = window.setInterval(refresh, pollIntervalMs)
    return () => {
      active = false
      window.clearInterval(intervalId)
    }
  }, [activityId, initialActivity.availableSlots, pollIntervalMs])

  return state
}
