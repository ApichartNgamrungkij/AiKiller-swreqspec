import { useCallback, useEffect, useState } from 'react'

import type { ActivityRegistrationSummary } from '../types/registrant'
import { fetchRegistrants } from '../services/registrantApi'

export const REGISTRANT_POLL_INTERVAL_MS = 120_000

type UseRegistrantsOptions = {
  enabled?: boolean
}

// Supports FR-VIEW-01, FR-VIEW-02, FR-VIEW-03, NFR-PERF-01
export function useRegistrants(
  activityId: string | number,
  options: UseRegistrantsOptions = {},
) {
  const { enabled = true } = options
  const [summary, setSummary] = useState<ActivityRegistrationSummary | null>(null)
  const [error, setError] = useState<Error | null>(null)

  const refresh = useCallback(async () => {
    try {
      const nextSummary = await fetchRegistrants(activityId)
      setSummary(nextSummary)
      setError(null)
    } catch (caughtError) {
      setError(caughtError instanceof Error ? caughtError : new Error('Unable to fetch registrants'))
    }
  }, [activityId])

  useEffect(() => {
    if (!enabled) {
      return undefined
    }

    void refresh()
    const intervalId = window.setInterval(() => {
      void refresh()
    }, REGISTRANT_POLL_INTERVAL_MS)

    return () => window.clearInterval(intervalId)
  }, [enabled, refresh])

  return { summary, error, refresh }
}
