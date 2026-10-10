import { act, renderHook } from '@testing-library/react'
import { beforeEach, expect, test, vi } from 'vitest'

import { fetchRegistrants } from '../services/registrantApi'
import { REGISTRANT_POLL_INTERVAL_MS, useRegistrants } from './useRegistrants'

vi.mock('../services/registrantApi', () => ({
  fetchRegistrants: vi.fn(),
}))

const mockedFetchRegistrants = vi.mocked(fetchRegistrants)

beforeEach(() => {
  vi.useFakeTimers()
  mockedFetchRegistrants.mockReset()
})

// Supports AC-VIEW-02
test('AC-VIEW-02: polling อัปเดตข้อมูลใหม่ภายใน 2 นาที', async () => {
  mockedFetchRegistrants
    .mockResolvedValueOnce({
      activityId: 'ACT-001',
      totalRegistered: 1,
      lastSyncedAt: null,
      syncStatus: 'SUCCESS',
      cachedResponses: [],
    })
    .mockResolvedValueOnce({
      activityId: 'ACT-001',
      totalRegistered: 2,
      lastSyncedAt: null,
      syncStatus: 'SUCCESS',
      cachedResponses: [],
    })

  const { result } = renderHook(() => useRegistrants('ACT-001'))
    await act(async () => {
      await Promise.resolve()
    })
    expect(result.current.summary?.totalRegistered).toBe(1)

    expect(REGISTRANT_POLL_INTERVAL_MS).toBeLessThanOrEqual(120_000)
    await act(async () => {
      vi.advanceTimersByTime(REGISTRANT_POLL_INTERVAL_MS)
      await Promise.resolve()
    })
    expect(result.current.summary?.totalRegistered).toBe(2)
})
