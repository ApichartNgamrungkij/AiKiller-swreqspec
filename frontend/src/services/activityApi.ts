import type { MockActivity } from '../mocks/activities'

type ApiActivity = Record<string, unknown>

function asString(value: unknown, fallback: string): string {
  return typeof value === 'string' ? value : fallback
}

function asNumber(value: unknown, fallback: number): number {
  return typeof value === 'number' && Number.isFinite(value) ? value : fallback
}

function normalizeActivity(payload: ApiActivity): MockActivity {
  const slots = Array.isArray(payload.slots) ? payload.slots : []
  const firstSlot = (slots[0] ?? {}) as ApiActivity
  const availableSlots = asNumber(
    payload.availableSlots ?? payload.max_participants ?? payload.maxParticipants,
    0,
  )
  const bookedSlots = asNumber(payload.bookedSlots ?? payload.booked ?? 0, 0)
  const status = payload.status === 'full' || bookedSlots >= availableSlots && availableSlots > 0 ? 'full' : 'open'

  return {
    id: asNumber(payload.id, 0),
    title: asString(payload.title, 'กิจกรรมไม่มีชื่อ'),
    category: asString(payload.category, ''),
    status,
    startAt: asString(
      payload.startAt,
      `${asString(firstSlot.slot_date, '1970-01-01')}T${asString(firstSlot.start_time, '00:00:00')}+07:00`,
    ),
    endAt: asString(
      payload.endAt,
      `${asString(firstSlot.slot_date, '1970-01-01')}T${asString(firstSlot.end_time, '00:00:00')}+07:00`,
    ),
    hoursAwarded: asNumber(payload.hoursAwarded ?? payload.volunteer_hours, 0),
    location: asString(payload.location ?? payload.venue, ''),
    availableSlots,
    bookedSlots,
    googleFormUrl: asString(payload.googleFormUrl ?? payload.registration_url, ''),
  }
}

async function getJson(url: string): Promise<unknown> {
  const response = await fetch(url)
  if (!response.ok) {
    throw new Error(`ไม่สามารถโหลดข้อมูลกิจกรรมได้ (${response.status})`)
  }
  return response.json()
}

// Supports FR-SRCH-01, FR-SRCH-03, FR-SRCH-05, AC-SRCH-06.
export async function fetchActivities(): Promise<MockActivity[]> {
  const payload = await getJson('/api/activities')
  const items = Array.isArray(payload)
    ? payload
    : Array.isArray((payload as ApiActivity).activities)
      ? (payload as ApiActivity).activities
      : []
  return items.map((item) => normalizeActivity(item as ApiActivity))
}

// Supports FR-SRCH-05 and AC-SRCH-06.
export async function fetchActivityDetail(activityId: number): Promise<MockActivity> {
  const payload = await getJson(`/api/activities/${activityId}`)
  return normalizeActivity(payload as ApiActivity)
}
