import ActivityCard from './ActivityCard'
import EmptyActivityState from './EmptyActivityState'
import type { MockActivity } from '../mocks/activities'

export type ActivityResultsProps = {
  activities: MockActivity[]
}

// Supports FR-SRCH-03 and FR-SRCH-04
export default function ActivityResults({ activities }: ActivityResultsProps) {
  if (activities.length === 0) {
    return <EmptyActivityState />
  }

  return (
    <section aria-label="ผลลัพธ์กิจกรรม">
      {activities.map((activity) => (
        <ActivityCard key={activity.id} activity={activity} />
      ))}
    </section>
  )
}
