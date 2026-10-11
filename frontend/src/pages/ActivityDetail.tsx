import { useEffect, useState } from 'react'

import ActivityDetail from '../components/ActivityDetail'
import { mockActivities, type MockActivity } from '../mocks/activities'
import { fetchActivityDetail } from '../services/activityApi'

export type ActivityDetailPageProps = {
  activity?: MockActivity
  activityId?: number
}

// Supports FR-SRCH-05 and ASM-02
export default function ActivityDetailPage({ activity = mockActivities[0], activityId }: ActivityDetailPageProps) {
  const [visibleActivity, setVisibleActivity] = useState(activity)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (activityId === undefined) {
      return
    }

    let active = true
    fetchActivityDetail(activityId)
      .then((nextActivity) => {
        if (active) {
          setVisibleActivity(nextActivity)
        }
      })
      .catch((reason: unknown) => {
        if (active) {
          setError(reason instanceof Error ? reason.message : 'ไม่สามารถโหลดรายละเอียดกิจกรรมได้')
        }
      })

    return () => {
      active = false
    }
  }, [activityId])

  return (
    <main>
      <h1>รายละเอียดกิจกรรม</h1>
      {error && <p role="alert">{error}</p>}
      <ActivityDetail activity={visibleActivity} />
    </main>
  )
}
