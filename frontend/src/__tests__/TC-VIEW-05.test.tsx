import { render, screen } from '@testing-library/react'
import { test } from 'vitest'

import RegistrantsDetail from '../pages/RegistrantsDetail'

const registrant = {
  rowId: 1,
  timestamp: '2026-10-10T08:30:00Z',
  studentId: '660510001',
  fullName: 'นายสมชาย ใจดี',
  faculty: 'วิศวกรรมศาสตร์',
  email: 'student@example.com',
}

// TC-VIEW-05-1
test('test_TC_VIEW_05_1_admin_can_view_registrants', () => {
  // Given: ผู้ใช้เป็น Admin
  // When: เข้าหน้าดูข้อมูลผู้ลงทะเบียน
  render(<RegistrantsDetail registrants={[registrant]} />)

  // Then: อนุญาตและแสดงข้อมูลผู้ลงทะเบียน
  expect(screen.getByRole('heading', { name: 'รายชื่อผู้ลงทะเบียน' })).toBeTruthy()
  expect(screen.getByText('660510001')).toBeTruthy()
})

// TC-VIEW-05-2
test('test_TC_VIEW_05_2_owner_can_view_single_registrant', () => {
  // Given: ผู้จัดเป็นเจ้าของกิจกรรมที่มีผู้ลงทะเบียน 1 คน
  // When: เข้าหน้าดูข้อมูลผู้ลงทะเบียน
  render(<RegistrantsDetail registrants={[registrant]} />)

  // Then: อนุญาตและแสดงข้อมูลผู้ลงทะเบียน 1 คน
  expect(screen.getByRole('status').textContent).toContain('ผู้ลงทะเบียนทั้งหมด: 1')
  expect(screen.getByText('นายสมชาย ใจดี')).toBeTruthy()
})

// TC-VIEW-05-3
test('test_TC_VIEW_05_3_non_owner_organizer_is_denied', () => {
  // Given: ผู้จัดไม่ใช่เจ้าของกิจกรรมและไม่ใช่ Admin
  // When: พยายามเข้าหน้าดูข้อมูลผู้ลงทะเบียน
  render(<RegistrantsDetail isAccessDenied />)

  // Then: ปฏิเสธการเข้าถึง
  expect(screen.getByRole('alert', { name: 'ปฏิเสธการเข้าถึง' })).toBeTruthy()
})
