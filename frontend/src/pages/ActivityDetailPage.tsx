import { useMemo } from 'react'

import { checkActivityScheduleOverlap, SavedBusyPeriod } from '../services/scheduleOverlap'

export type ActivityDetailPageProps = {
  title?: string
  activityStart: string | Date
  activityEnd: string | Date
  busyPeriods?: SavedBusyPeriod[]
}

// Supports FR-SCHED-04, FR-SCHED-05, DOM-SCHED-01
export default function ActivityDetailPage({
  title = 'รายละเอียดกิจกรรม',
  activityStart,
  activityEnd,
  busyPeriods = [],
}: ActivityDetailPageProps) {
  const overlap = useMemo(
    () => checkActivityScheduleOverlap(activityStart, activityEnd, busyPeriods),
    [activityEnd, activityStart, busyPeriods],
  )

  return (
    <main>
      <h1>{title}</h1>
      <p>
        {new Date(activityStart).toLocaleString('th-TH')} - {new Date(activityEnd).toLocaleString('th-TH')}
      </p>

      {overlap.hasOverlap ? (
        <p role="alert" aria-live="polite">
          {overlap.message}
        </p>
      ) : (
        <p role="status" aria-live="polite">
          {overlap.message}
        </p>
      )}

      {overlap.matchingPeriods.length > 0 && (
        <ul>
          {overlap.matchingPeriods.map((period) => (
            <li key={period.id ?? `${period.start_date}-${period.start_time}`}>
              {period.start_date} ถึง {period.end_date} • {period.start_time} - {period.end_time}
            </li>
          ))}
        </ul>
      )}

      <button type="button">ไปยัง Google Form</button>
    </main>
  )
}
