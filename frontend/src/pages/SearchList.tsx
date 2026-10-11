import { useEffect, useState } from 'react'

import ActivityCard from '../components/ActivityCard'
import { mockActivities, type MockActivity } from '../mocks/activities'
import { fetchActivities } from '../services/activityApi'

export type SearchListProps = {
  activities?: MockActivity[]
}

// Supports FR-SRCH-01 and FR-SRCH-03
export default function SearchList({ activities = mockActivities }: SearchListProps) {
  const [visibleActivities, setVisibleActivities] = useState(activities)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let active = true
    fetchActivities()
      .then((nextActivities) => {
        if (active) {
          setVisibleActivities(nextActivities)
        }
      })
      .catch((reason: unknown) => {
        if (active) {
          setError(reason instanceof Error ? reason.message : 'ไม่สามารถโหลดกิจกรรมได้')
        }
      })

    return () => {
      active = false
    }
  }, [])

  return (
    <main>
      <h1>ค้นหากิจกรรมจิตอาสา</h1>
      {error && <p role="alert">{error}</p>}
      <section aria-label="รายการกิจกรรม">
        {visibleActivities.map((activity) => (
          <ActivityCard key={activity.id} activity={activity} />
        ))}
      </section>
    </main>
  )
}
