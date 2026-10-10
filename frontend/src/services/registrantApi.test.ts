import { beforeEach, expect, test, vi } from 'vitest'

import { fetchRegistrants } from './registrantApi'

beforeEach(() => {
  vi.restoreAllMocks()
})

// Supports AC-VIEW-01
test('AC-VIEW-01: แปลง response จาก API เป็น summary สำหรับหน้าแสดงผล', async () => {
  vi.stubGlobal(
    'fetch',
    vi.fn().mockResolvedValue(
      new Response(
        JSON.stringify({
          activityId: 'ACT-001',
          totalRegistered: 1,
          lastSyncedAt: '2026-10-10T08:30:00Z',
          syncStatus: 'SUCCESS',
          isCache: false,
          data: [
            {
              rowId: 1,
              timestamp: '2026-10-10T08:30:00Z',
              studentId: '660510001',
              fullName: 'นายสมชาย ใจดี',
            },
          ],
        }),
        { status: 200, headers: { 'Content-Type': 'application/json' } },
      ),
    ),
  )

  await expect(fetchRegistrants('ACT-001')).resolves.toMatchObject({
    activityId: 'ACT-001',
    totalRegistered: 1,
    cachedResponses: [{ studentId: '660510001' }],
  })
})

// Supports FR-VIEW-02
test('FR-VIEW-02: API error is surfaced to the caller', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response(null, { status: 403 })))

  await expect(fetchRegistrants('ACT-001')).rejects.toThrow('403')
})
