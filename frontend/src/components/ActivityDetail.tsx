import type { MockActivity } from '../mocks/activities'

export type ActivityDetailProps = {
  activity: MockActivity
}

function formatDateTime(value: string): string {
  return new Date(value).toLocaleString('th-TH', {
    dateStyle: 'long',
    timeStyle: 'short',
    timeZone: 'Asia/Bangkok',
  })
}

// Supports FR-SRCH-05 and ASM-02
export default function ActivityDetail({ activity }: ActivityDetailProps) {
  return (
    <article aria-label={`รายละเอียดกิจกรรม ${activity.title}`}>
      <h2>{activity.title}</h2>
      <dl>
        <dt>ชั่วโมงจิตอาสา</dt>
        <dd>{activity.hoursAwarded} ชั่วโมง</dd>
        <dt>วันเวลา</dt>
        <dd>
          {formatDateTime(activity.startAt)} - {formatDateTime(activity.endAt)}
        </dd>
        <dt>สถานที่</dt>
        <dd>{activity.location}</dd>
      </dl>
      <a href={activity.googleFormUrl} target="_blank" rel="noreferrer">
        ไปยัง Google Form สำหรับลงทะเบียนต่อ
      </a>
    </article>
  )
}
