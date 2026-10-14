import { render, screen } from '@testing-library/react'

import RegistrantsDetail from '../pages/RegistrantsDetail'

const registrants = [
  {
    rowId: 1,
    timestamp: '2026-10-10T08:30:00Z',
    studentId: '660510001',
    fullName: 'นายสมชาย ใจดี',
    faculty: 'วิศวกรรมศาสตร์',
    email: 'student@example.com',
  },
  {
    rowId: 2,
    timestamp: '2026-10-10T08:35:00Z',
    studentId: '660510002',
    fullName: 'นางสาวสมหญิง รักเรียน',
    faculty: 'วิทยาศาสตร์',
    email: 'student2@example.com',
  },
]

// TC-VIEW-01-1
test('test_TC_VIEW_01_1_owner_sees_registrant_count_and_names', () => {
  // Given: กิจกรรมของผู้จัดมีผู้ลงทะเบียนอย่างน้อย 2 คนและดึงข้อมูลสำเร็จ
  // When: ผู้จัดเปิดหน้ารายละเอียดกิจกรรมของตนเอง
  render(<RegistrantsDetail registrants={registrants} />)

  // Then: แสดงจำนวนและรายชื่อผู้ลงทะเบียนล่าสุด
  expect(screen.getByText('ผู้ลงทะเบียนทั้งหมด: 2').textContent).toContain(
    'ผู้ลงทะเบียนทั้งหมด: 2',
  )
  expect(screen.getByText('นายสมชาย ใจดี')).toBeTruthy()
  expect(screen.getByText('นางสาวสมหญิง รักเรียน')).toBeTruthy()
})

// TC-VIEW-01-2
test('test_TC_VIEW_01_2_owner_sees_single_registrant', () => {
  // Given: กิจกรรมของผู้จัดมีผู้ลงทะเบียนพอดี 1 คนและดึงข้อมูลสำเร็จ
  // When: ผู้จัดเปิดหน้ารายละเอียดกิจกรรมของตนเอง
  render(<RegistrantsDetail registrants={[registrants[0]]} />)

  // Then: แสดงจำนวน 1 และรายชื่อผู้ลงทะเบียนคนนั้น
  expect(screen.getByText('ผู้ลงทะเบียนทั้งหมด: 1').textContent).toContain(
    'ผู้ลงทะเบียนทั้งหมด: 1',
  )
  expect(screen.getByText('นายสมชาย ใจดี')).toBeTruthy()
})

// TC-VIEW-01-3
test('test_TC_VIEW_01_3_owner_sees_empty_state_without_registrants', () => {
  // Given: กิจกรรมของผู้จัดยังไม่มีผู้ลงทะเบียน
  // When: ผู้จัดเปิดหน้ารายละเอียดกิจกรรมของตนเอง
  render(<RegistrantsDetail registrants={[]} />)

  // Then: หน้าจอแสดง Empty State ตาม CON-VIEW-01 และสัญญา API
  expect(screen.getByText('ผู้ลงทะเบียนทั้งหมด: 0').textContent).toContain(
    'ผู้ลงทะเบียนทั้งหมด: 0',
  )
  expect(screen.getByRole('status', { name: 'ไม่มีผู้ลงทะเบียน' })).toBeTruthy()
})
