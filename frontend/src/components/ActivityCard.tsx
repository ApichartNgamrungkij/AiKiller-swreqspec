import type { MockActivity } from '../mocks/activities'

export type ActivityCardProps = {
  activity: MockActivity
}

// Supports FR-SRCH-01 and FR-SRCH-03
export default function ActivityCard({ activity }: ActivityCardProps) {
  const isFull = activity.status === 'full'

  return (
    <article aria-label={`กิจกรรม ${activity.title}`}>
      <h2>{activity.title}</h2>
      <p>{activity.category}</p>
      <p>{activity.location}</p>
      <p>
        รับ {activity.availableSlots} คน | ลงทะเบียนแล้ว {activity.bookedSlots} คน
      </p>
      <span role="status">{isFull ? 'เต็มแล้ว' : 'ยังรับสมัคร'}</span>
    </article>
  )
}
