import { afterEach, beforeEach, vi } from 'vitest'

import { fetchActivities } from './activityApi'

beforeEach(() => {
  vi.stubGlobal(
    'fetch',
    vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        activities: [
          {
            id: 99,
            title: 'กิจกรรมใหม่จากผู้จัด',
            status: 'published',
            category: 'กีฬา',
            venue: 'สนามกีฬา',
            max_participants: 40,
            bookedSlots: 0,
            volunteer_hours: 5,
            registration_url: 'https://forms.google.com/new-activity',
            slots: [
              {
                slot_date: '2026-12-01',
                start_time: '09:00:00',
                end_time: '14:00:00',
              },
            ],
          },
        ],
      }),
    }),
  )
})

afterEach(() => {
  vi.unstubAllGlobals()
})

// Supports AC-SRCH-06
test('test_AC_SRCH_06_new_activity_from_api_is_available_immediately', async () => {
  const activities = await fetchActivities()

  expect(activities).toHaveLength(1)
  expect(activities[0].title).toBe('กิจกรรมใหม่จากผู้จัด')
  expect(fetch).toHaveBeenCalledWith('/api/activities')
})
