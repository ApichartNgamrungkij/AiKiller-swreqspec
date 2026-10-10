import type { SyncStatus } from '../types/registrant'

type SyncStatusBadgeProps = {
  status: SyncStatus
  lastSyncedAt: string | null
}

// Supports IF-VIEW-02, FR-VIEW-04, AC-VIEW-03
export default function SyncStatusBadge({
  status,
  lastSyncedAt,
}: SyncStatusBadgeProps) {
  const label = status === 'FAILED' ? 'ข้อมูลจาก Cache' : 'ข้อมูลล่าสุด'
  const updatedAt = lastSyncedAt
    ? new Date(lastSyncedAt).toLocaleString('th-TH')
    : 'ยังไม่มีข้อมูล'

  return (
    <span role="status" aria-label="สถานะการอัปเดต">
      {label} • อัปเดตเมื่อ {updatedAt}
    </span>
  )
}
