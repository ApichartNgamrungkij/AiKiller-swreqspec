import { act, renderHook } from '@testing-library/react'
import { beforeEach, expect, test, vi } from 'vitest'

import { fetchRegistrants } from '../services/registrantApi'
import { REGISTRANT_POLL_INTERVAL_MS, useRegistrants } from '../hooks/useRegistrants'

vi.mock('../services/registrantApi', () => ({
  fetchRegistrants: vi.fn(),
}))

const mockedFetchRegistrants = vi.mocked(fetchRegistrants)

beforeEach(() => {
  vi.useFakeTimers()
  mockedFetchRegistrants.mockReset()
})

// TC-VIEW-02-1
test('test_TC_VIEW_02_1_count_updates_after_new_registration', async () => {
  // Given: มีผู้ลงทะเบียนใหม่และข้อมูลถูกบันทึกใน Google Sheets แล้ว
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

  // When: เวลาผ่านไปไม่เกิน 2 นาทีและ hook ทำ Polling
  const { result } = renderHook(() => useRegistrants('ACT-001'))
  await act(async () => {
    await Promise.resolve()
  })
  await act(async () => {
    vi.advanceTimersByTime(REGISTRANT_POLL_INTERVAL_MS)
    await Promise.resolve()
  })

  // Then: หน้าจอมีจำนวนผู้ลงทะเบียนใหม่
  expect(result.current.summary?.totalRegistered).toBe(2)
})

// TC-VIEW-02-2
test('test_TC_VIEW_02_2_count_updates_at_two_minute_boundary', async () => {
  // Given: มีผู้ลงทะเบียนใหม่และข้อมูลถูกบันทึกใน Google Sheets แล้ว
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

  // When: เวลาผ่านไปครบ 2 นาทีพอดี
  const { result } = renderHook(() => useRegistrants('ACT-001'))
  await act(async () => {
    await Promise.resolve()
  })
  await act(async () => {
    vi.advanceTimersByTime(120_000)
    await Promise.resolve()
  })

  // Then: ระบบอัปเดตจำนวนภายใน 2 นาที
  expect(REGISTRANT_POLL_INTERVAL_MS).toBeLessThanOrEqual(120_000)
  expect(result.current.summary?.totalRegistered).toBe(2)
})
