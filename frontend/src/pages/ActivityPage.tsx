import { useEffect, useState } from 'react'

import ActivityDetail from '../components/ActivityDetail'
import ExportErrorState from '../components/ExportErrorState'
import ExportListButton from '../components/ExportListButton'
import type { MockActivity } from '../mocks/activities'
import { mockActivities } from '../mocks/activities'
import type { ExportAccessMock } from '../mocks/exportAccess'
import { fetchExportAccess } from '../services/exportApi'

export type ActivityPageProps = {
  activity?: MockActivity
  activityId?: number
  exportAccess?: ExportAccessMock
}

// Supports FR-EXP-01, FR-EXP-02, ACC-GSHEET-01, ACC-GSHEET-02, NFR-SEC-01, NFR-SEC-02.
export default function ActivityPage({
  activity = mockActivities[0],
  activityId = activity.id,
  exportAccess,
}: ActivityPageProps) {
  const [access, setAccess] = useState<ExportAccessMock | undefined>(exportAccess)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (exportAccess) {
      setAccess(exportAccess)
      return
    }

    let active = true
    fetchExportAccess(activityId)
      .then((response) => {
        if (active) {
          setAccess({
            activityId: response.activityId,
            canExport: response.canExport,
            hasAccess: response.canExport,
            responseCount: response.responseCount,
            googleSheetUrl: response.googleSheetUrl ?? null,
          })
        }
      })
      .catch((reason: unknown) => {
        if (active) {
          setError(reason instanceof Error ? reason.message : 'ไม่สามารถโหลดสิทธิ์การดาวน์โหลดได้')
        }
      })

    return () => {
      active = false
    }
  }, [activityId, exportAccess])

  return (
    <main>
      <h1>รายละเอียดกิจกรรม</h1>
      <ActivityDetail activity={activity} />
      {error && <ExportErrorState message={error} />}
      {access && <ExportListButton access={access} activityId={activityId} />}
    </main>
  )
}
