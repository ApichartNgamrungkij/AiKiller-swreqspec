import { act, renderHook } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

import { useActivityStatus } from './useActivityStatus'

describe('useActivityStatus', () => {
  beforeEach(() => {
    vi.useFakeTimers()
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        new Response(
          JSON.stringify({ status: 'full', bookedSlots: 10, availableSlots: 10 }),
          { status: 200, headers: { 'Content-Type': 'application/json' } },
        ),
      ),
    )
  })

  afterEach(() => {
    vi.useRealTimers()
    vi.unstubAllGlobals()
  })

  it('test_AC_SRCH_07_status_updates_within_1_minute', async () => {
    const { result } = renderHook(() =>
      useActivityStatus(1, { status: 'open', bookedSlots: 9, availableSlots: 10 }),
    )

    await act(async () => {
      await vi.advanceTimersByTimeAsync(60_000)
    })

    expect(result.current.status).toBe('full')
    expect(result.current.bookedSlots).toBe(10)
    expect(fetch).toHaveBeenCalledWith('/api/activities/1')
  })

  it('test_AC_SRCH_07_status_polling_accepts_two_minute_upper_bound', async () => {
    const { result } = renderHook(() =>
      useActivityStatus(1, { status: 'open', bookedSlots: 9, availableSlots: 10 }, 120_000),
    )

    await act(async () => {
      await vi.advanceTimersByTimeAsync(120_000)
    })

    expect(result.current.status).toBe('full')
    expect(fetch).toHaveBeenCalledWith('/api/activities/1')
  })
})
