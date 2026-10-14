import { render, screen } from '@testing-library/react'
import { test } from 'vitest'

import CacheWarningAlert from '../components/CacheWarningAlert'
import SyncStatusBadge from '../components/SyncStatusBadge'

const lastSyncedAt = '2026-10-10T08:30:00Z'

// TC-VIEW-03-1
test('test_TC_VIEW_03_1_cached_registrants_show_when_sheets_api_fails', () => {
  // Given: Google Sheets API ล้มเหลวและมีข้อมูลล่าสุดใน Cache
  // When: ผู้จัดกิจกรรมเข้าดูข้อมูลผู้ลงทะเบียน
  render(
    <>
      <SyncStatusBadge status="FAILED" lastSyncedAt={lastSyncedAt} />
      <CacheWarningAlert isCache lastSyncedAt={lastSyncedAt} />
    </>,
  )

  // Then: แสดงสถานะ Cache และเวลาอัปเดตล่าสุดโดยไม่เป็นหน้าว่าง
  expect(screen.getByRole('status').textContent).toContain('ข้อมูลจาก Cache')
  expect(screen.getByRole('status').textContent).toContain('อัปเดตเมื่อ')
  expect(screen.getByRole('alert').textContent).toContain('แสดงข้อมูลล่าสุดเมื่อ')
})

// TC-VIEW-03-2
test('test_TC_VIEW_03_2_cached_single_registrant_shows_with_last_sync_time', () => {
  // Given: API ล้มเหลวและ Cache มีผู้ลงทะเบียน 1 คน
  // When: ผู้จัดกิจกรรมเข้าดูข้อมูลผู้ลงทะเบียน
  render(<CacheWarningAlert isCache lastSyncedAt={lastSyncedAt} />)

  // Then: แสดงคำเตือนพร้อมเวลาอัปเดตล่าสุดและไม่เป็นหน้าว่าง
  expect(screen.getByRole('alert').textContent).toContain('แสดงข้อมูลล่าสุดเมื่อ')
  expect(screen.getByRole('alert').textContent).not.toBe('')
})
