import type { MockActivity } from '../mocks/activities'
import type { StudentSchedule } from '../mocks/studentSchedule'

export const ACTIVITY_CATEGORIES = [
  'วิชาการ',
  'กีฬา',
  'ศิลปวัฒนธรรม',
  'คุณธรรมจริยธรรม',
  'บำเพ็ญประโยชน์',
] as const

export type ActivityCategory = (typeof ACTIVITY_CATEGORIES)[number]

export type ActivityFilter = {
  category?: ActivityCategory
  availableOnly?: boolean
}

function isSupportedCategory(value: string): value is ActivityCategory {
  return ACTIVITY_CATEGORIES.includes(value as ActivityCategory)
}

function isActivityWithinAvailability(activity: MockActivity, schedule: StudentSchedule): boolean {
  const activityStart = new Date(activity.startAt)
  const activityEnd = new Date(activity.endAt)

  return schedule.availabilitySlots.some((slot) => {
    const slotStart = new Date(`${slot.date}T${slot.startTime}:00+07:00`)
    const slotEnd = new Date(`${slot.date}T${slot.endTime}:00+07:00`)
    return activityStart >= slotStart && activityEnd <= slotEnd
  })
}

// Supports FR-SRCH-02, FR-SRCH-03, DOM — accepts only the five university-approved categories.
export function filterActivities(
  activities: MockActivity[],
  filters: ActivityFilter,
  schedule: StudentSchedule,
): MockActivity[] {
  if (filters.category !== undefined && !isSupportedCategory(filters.category)) {
    return []
  }

  return activities.filter((activity) => {
    const matchesCategory = filters.category === undefined || activity.category === filters.category
    const matchesAvailability =
      filters.availableOnly !== true || isActivityWithinAvailability(activity, schedule)
    return matchesCategory && matchesAvailability
  })
}
