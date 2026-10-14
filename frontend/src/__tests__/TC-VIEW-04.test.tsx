import { render, screen } from '@testing-library/react'
import { test } from 'vitest'

import RegistrantsDetail from '../pages/RegistrantsDetail'

// TC-VIEW-04-1
test('test_TC_VIEW_04_1_student_is_denied_without_personal_data', () => {
  // Given: นักศึกษาทั่วไปพยายามเข้าถึงข้อมูลที่มีผู้ลงทะเบียน
  // When: เปิดหน้าดูข้อมูลผู้ลงทะเบียน
  render(<RegistrantsDetail isAccessDenied />)

  // Then: แสดง Access Denied และไม่แสดงข้อมูลส่วนตัว
  expect(screen.getByRole('heading', { name: 'Access Denied' })).toBeTruthy()
  expect(screen.queryByText('660510001')).toBeNull()
})

// TC-VIEW-04-2
test('test_TC_VIEW_04_2_student_is_denied_for_single_registrant', () => {
  // Given: นักศึกษาทั่วไปพยายามดูกิจกรรมที่มีผู้ลงทะเบียน 1 คน
  // When: เปิดหน้าดูข้อมูลผู้ลงทะเบียน
  render(<RegistrantsDetail isAccessDenied />)

  // Then: แสดง Access Denied และไม่แสดงข้อมูลผู้ลงทะเบียน
  expect(screen.getByRole('alert', { name: 'ปฏิเสธการเข้าถึง' })).toBeTruthy()
  expect(screen.queryByText('นายสมชาย ใจดี')).toBeNull()
})

// TC-VIEW-04-3
test('test_TC_VIEW_04_3_authorized_user_follows_view_access_rule', () => {
  // Given: ผู้ใช้เป็น Admin หรือเจ้าของกิจกรรม
  // When: เข้าหน้าดูข้อมูลผู้ลงทะเบียน
  render(<RegistrantsDetail registrants={[]} />)

  // Then: ไม่แสดง Access Denied และแสดงหน้าข้อมูล
  expect(screen.getByRole('heading', { name: 'รายชื่อผู้ลงทะเบียน' })).toBeTruthy()
  expect(screen.queryByRole('alert', { name: 'ปฏิเสธการเข้าถึง' })).toBeNull()
})
