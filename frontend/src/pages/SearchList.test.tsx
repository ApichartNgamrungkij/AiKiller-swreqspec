import { render, screen } from '@testing-library/react'

import SearchList from './SearchList'

// Supports AC-SRCH-01
test('test_AC_SRCH_01_list_shows_status_and_activity', () => {
  render(<SearchList />)

  expect(screen.getByRole('heading', { name: 'ค่ายอาสาพัฒนาชุมชน' })).toBeTruthy()
  expect(screen.getByRole('heading', { name: 'อบรมทักษะการนำเสนอ' })).toBeTruthy()
  expect(screen.getByText('ยังรับสมัคร')).toBeTruthy()
  expect(screen.getByText('เต็มแล้ว')).toBeTruthy()
})

test('test_TC_SRCH_01_1_list_shows_all_activities_with_status', () => {
  // Given: มีกิจกรรมทั้งหมดที่ผู้จัดสร้างไว้ในระบบ โดยมีทั้งกิจกรรมที่ยังรับสมัครและกิจกรรมที่เต็มแล้ว
  // When: นักศึกษาเปิดหน้ารายการกิจกรรม
  render(<SearchList />)

  // Then: แสดงกิจกรรมทุกรายการ
  expect(screen.getByRole('heading', { name: 'ค่ายอาสาพัฒนาชุมชน' })).toBeTruthy()
  expect(screen.getByRole('heading', { name: 'อบรมทักษะการนำเสนอ' })).toBeTruthy()
  // Then: กำกับแต่ละรายการด้วยสถานะ "เต็มแล้ว" หรือ "ยังรับสมัคร"
  expect(screen.getByText('ยังรับสมัคร')).toBeTruthy()
  expect(screen.getByText('เต็มแล้ว')).toBeTruthy()
})

test('test_TC_SRCH_01_2_list_shows_boundary_statuses', () => {
  // Given: มีกิจกรรมที่ผู้จัดสร้างไว้ 2 รายการ โดยรายการหนึ่งมีสถานะ "ยังรับสมัคร" และอีกรายการมีสถานะ "เต็มแล้ว"
  const activities = [
    {
      id: 101,
      title: 'กิจกรรมยังรับสมัคร',
      category: 'วิชาการ',
      status: 'open' as const,
      startAt: '2026-11-07T09:00:00+07:00',
      endAt: '2026-11-07T12:00:00+07:00',
      hoursAwarded: 3,
      location: 'ห้องเรียน',
      availableSlots: 1,
      bookedSlots: 0,
      googleFormUrl: 'https://forms.google.com/open',
    },
    {
      id: 102,
      title: 'กิจกรรมเต็มแล้ว',
      category: 'กีฬา',
      status: 'full' as const,
      startAt: '2026-11-08T09:00:00+07:00',
      endAt: '2026-11-08T12:00:00+07:00',
      hoursAwarded: 3,
      location: 'สนามกีฬา',
      availableSlots: 1,
      bookedSlots: 1,
      googleFormUrl: 'https://forms.google.com/full',
    },
  ]

  // When: นักศึกษาเปิดหน้ารายการกิจกรรม
  render(<SearchList activities={activities} />)

  // Then: แสดงกิจกรรมทั้ง 2 รายการ
  expect(screen.getByRole('heading', { name: 'กิจกรรมยังรับสมัคร' })).toBeTruthy()
  expect(screen.getByRole('heading', { name: 'กิจกรรมเต็มแล้ว' })).toBeTruthy()
  // Then: แสดงสถานะของแต่ละรายการตรงกับสถานะของกิจกรรมนั้น
  expect(screen.getByText('ยังรับสมัคร')).toBeTruthy()
  expect(screen.getByText('เต็มแล้ว')).toBeTruthy()
})
