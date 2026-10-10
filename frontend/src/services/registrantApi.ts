import type { ActivityRegistrationSummary } from '../types/registrant'

const DEFAULT_API_BASE_URL = '/api/v1'

// Supports FR-VIEW-01, FR-VIEW-02, FR-VIEW-03, NFR-PERF-01
export async function fetchRegistrants(
  activityId: string | number,
  apiBaseUrl = DEFAULT_API_BASE_URL,
): Promise<ActivityRegistrationSummary> {
  const response = await fetch(`${apiBaseUrl}/activities/${activityId}/registrants`)
  if (!response.ok) {
    throw new Error(`Unable to fetch registrants: ${response.status}`)
  }

  const payload = (await response.json()) as ActivityRegistrationSummary & {
    isCache: boolean
    data: ActivityRegistrationSummary['cachedResponses']
  }

  return {
    activityId: payload.activityId,
    totalRegistered: payload.totalRegistered,
    lastSyncedAt: payload.lastSyncedAt,
    syncStatus: payload.syncStatus,
    cachedResponses: payload.data,
  }
}
