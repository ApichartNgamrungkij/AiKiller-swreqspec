import { useEffect, useMemo, useState } from 'react'

import ActivityFilters from '../components/ActivityFilters'
import ActivityResults from '../components/ActivityResults'
import { mockActivities, type MockActivity } from '../mocks/activities'
import { mockStudentSchedule } from '../mocks/studentSchedule'
import { fetchActivities } from '../services/activityApi'
import { filterActivities, type ActivityFilter } from '../services/activityFilter'
import '../styles/responsive.css'

export type SearchListProps = {
  activities?: MockActivity[]
}

// Supports FR-SRCH-01, FR-SRCH-02, FR-SRCH-03, and FR-SRCH-04
export default function SearchList({ activities = mockActivities }: SearchListProps) {
  const [visibleActivities, setVisibleActivities] = useState(activities)
  const [filters, setFilters] = useState<ActivityFilter>({})
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

  const filteredActivities = useMemo(
    () => filterActivities(visibleActivities, filters, mockStudentSchedule),
    [filters, visibleActivities],
  )

  return (
    <main className="search-page">
      <h1>ค้นหากิจกรรมจิตอาสา</h1>
      {error && <p role="alert">{error}</p>}
      <ActivityFilters value={filters} onChange={setFilters} />
      <ActivityResults activities={filteredActivities} />
    </main>
  )
}
