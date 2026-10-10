type CacheWarningAlertProps = {
  isCache: boolean
  lastSyncedAt: string | null
}

// Supports IF-VIEW-02, FR-VIEW-04, AC-VIEW-03
export default function CacheWarningAlert({
  isCache,
  lastSyncedAt,
}: CacheWarningAlertProps) {
  if (!isCache) {
    return null
  }

  const updatedAt = lastSyncedAt
    ? new Date(lastSyncedAt).toLocaleString('th-TH')
    : 'ไม่ทราบเวลา'

  return (
    <div role="alert" className="border border-yellow-300 bg-yellow-50 p-3 text-yellow-900">
      แสดงข้อมูลล่าสุดเมื่อ {updatedAt}
    </div>
  )
}
