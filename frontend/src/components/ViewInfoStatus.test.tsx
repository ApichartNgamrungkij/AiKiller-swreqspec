import { render, screen } from '@testing-library/react'

import CacheWarningAlert from './CacheWarningAlert'
import SyncStatusBadge from './SyncStatusBadge'

// Supports AC-VIEW-03
test('AC-VIEW-03: แสดงเวลาอัปเดตล่าสุดและคำเตือนเมื่อใช้ Cache', () => {
  const lastSyncedAt = '2026-10-10T08:30:00Z'

  render(
    <>
      <SyncStatusBadge status="FAILED" lastSyncedAt={lastSyncedAt} />
      <CacheWarningAlert isCache lastSyncedAt={lastSyncedAt} />
    </>,
  )

  expect(screen.getByRole('status').textContent).toContain('ข้อมูลจาก Cache')
  expect(screen.getByRole('status').textContent).toContain('อัปเดตเมื่อ')
  expect(screen.getByRole('alert').textContent).toContain('แสดงข้อมูลล่าสุดเมื่อ')
})
