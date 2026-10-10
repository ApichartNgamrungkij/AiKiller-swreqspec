import type { RegisteredStudent } from '../types/registrant'
import RegistrantTable from '../components/RegistrantTable'
import AccessDenied from '../components/AccessDenied'
import EmptyRegistrantState from '../components/EmptyRegistrantState'
import { mockRegistrants } from '../mocks/registrants'
import { useRegistrants } from '../hooks/useRegistrants'

type RegistrantsDetailProps = {
  activityId?: string | number
  registrants?: RegisteredStudent[]
  isAccessDenied?: boolean
  useApi?: boolean
}

// Supports FR-VIEW-01, FR-VIEW-03, AC-VIEW-01
export default function RegistrantsDetail({
  activityId = 'ACT-001',
  registrants = mockRegistrants,
  isAccessDenied = false,
  useApi = false,
}: RegistrantsDetailProps) {
  const apiResult = useRegistrants(activityId, { enabled: useApi })
  const displayedRegistrants = useApi
    ? apiResult.summary?.cachedResponses ?? []
    : registrants

  if (isAccessDenied) {
    return <AccessDenied />
  }

  return (
    <main>
      <h1>รายชื่อผู้ลงทะเบียน</h1>
      <p>กิจกรรม: {activityId}</p>
      <p role="status">ผู้ลงทะเบียนทั้งหมด: {displayedRegistrants.length}</p>
      {displayedRegistrants.length === 0 ? (
        <EmptyRegistrantState />
      ) : (
        <RegistrantTable registrants={displayedRegistrants} />
      )}
    </main>
  )
}
