import ActivityDetail from '../components/ActivityDetail'
import { mockActivities, type MockActivity } from '../mocks/activities'

export type ActivityDetailPageProps = {
  activity?: MockActivity
}

// Supports FR-SRCH-05 and ASM-02
export default function ActivityDetailPage({ activity = mockActivities[0] }: ActivityDetailPageProps) {
  return (
    <main>
      <h1>รายละเอียดกิจกรรม</h1>
      <ActivityDetail activity={activity} />
    </main>
  )
}
