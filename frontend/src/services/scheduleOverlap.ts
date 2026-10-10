export type SavedBusyPeriod = {
  id?: number | string
  student_id?: number | string
  start_date?: string
  end_date?: string
  start_time?: string
  end_time?: string
}

export type OverlapCheckResult = {
  hasOverlap: boolean
  message: string
  matchingPeriods: SavedBusyPeriod[]
}

function toLocalDateString(date: Date): string {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

function toDate(value: string | Date): Date {
  if (value instanceof Date) {
    return new Date(value.getTime())
  }

  const parsed = new Date(value)
  if (!Number.isNaN(parsed.getTime())) {
    return parsed
  }

  throw new Error(`Invalid date value: ${value}`)
}

function toTimeString(value?: string): string {
  if (!value) {
    return '00:00:00'
  }

  if (value.length === 5) {
    return `${value}:00`
  }

  return value
}

function dateRangeInclusive(start: string, end: string): string[] {
  const startDate = new Date(`${start}T00:00:00`)
  const endDate = new Date(`${end}T00:00:00`)

  if (Number.isNaN(startDate.getTime()) || Number.isNaN(endDate.getTime())) {
    return []
  }

  const dates: string[] = []
  const cursor = new Date(startDate)

  while (cursor <= endDate) {
    dates.push(toLocalDateString(cursor))
    cursor.setDate(cursor.getDate() + 1)
  }

  return dates
}

// Supports FR-SCHED-04, FR-SCHED-05, IF-SCHED-01
export function checkActivityScheduleOverlap(
  activityStart: string | Date,
  activityEnd: string | Date,
  busyPeriods: SavedBusyPeriod[],
): OverlapCheckResult {
  const start = toDate(activityStart)
  const end = toDate(activityEnd)

  if (end <= start) {
    return {
      hasOverlap: false,
      message: 'ไม่มีช่วงเวลาคาบเกี่ยวกับตารางส่วนตัวของคุณ',
      matchingPeriods: [],
    }
  }

  const matchingPeriods: SavedBusyPeriod[] = []

  for (const period of busyPeriods) {
    const periodStartDate = period.start_date ?? toLocalDateString(start)
    const periodEndDate = period.end_date ?? toLocalDateString(end)
    const dates = dateRangeInclusive(periodStartDate, periodEndDate)

    for (const dateLabel of dates) {
      const busyStart = new Date(`${dateLabel}T${toTimeString(period.start_time ?? '09:00')}`)
      const busyEnd = new Date(`${dateLabel}T${toTimeString(period.end_time ?? '10:00')}`)

      if (busyStart < end && start < busyEnd) {
        matchingPeriods.push(period)
        break
      }
    }
  }

  return {
    hasOverlap: matchingPeriods.length > 0,
    message:
      matchingPeriods.length > 0
        ? 'มีช่วงเวลาคาบเกี่ยวกับตารางส่วนตัวของคุณ'
        : 'ไม่มีช่วงเวลาคาบเกี่ยวกับตารางส่วนตัวของคุณ',
    matchingPeriods,
  }
}
