import ActivityCard from '../components/ActivityCard'
import { mockActivities, type MockActivity } from '../mocks/activities'

export type SearchListProps = {
  activities?: MockActivity[]
}

// Supports FR-SRCH-01 and FR-SRCH-03
export default function SearchList({ activities = mockActivities }: SearchListProps) {
  return (
    <main>
      <h1>ค้นหากิจกรรมจิตอาสา</h1>
      <section aria-label="รายการกิจกรรม">
        {activities.map((activity) => (
          <ActivityCard key={activity.id} activity={activity} />
        ))}
      </section>
    </main>
  )
}
