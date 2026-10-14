import React from 'react'
import { render, screen } from '@testing-library/react'

import CreateActivityPage from '../pages/CreateActivityPage'
import CreateActivityRoute from '../routes/CreateActivityRoute'

test('test_TC_ACT_01_1_page_shows_create_form', () => {
  render(
    <CreateActivityRoute user={{ approved_by_admin: true, can_create_activity: true }}>
      <CreateActivityPage />
    </CreateActivityRoute>,
  )

  expect(screen.getAllByRole('heading', { name: 'สร้างกิจกรรมใหม่' }).length).toBeGreaterThan(0)
  expect(screen.getByLabelText('ชื่อกิจกรรม')).toBeTruthy()
  expect(screen.getByLabelText('ประเภทกิจกรรม')).toBeTruthy()
  expect(screen.getByLabelText('สถานที่จัด')).toBeTruthy()
  expect(screen.getByLabelText('จำนวนรับสมัคร')).toBeTruthy()
  expect(screen.getByLabelText('ชั่วโมงจิตอาสาที่จะได้รับ')).toBeTruthy()
  expect(screen.getByLabelText('ลิงก์ URL สำหรับลงทะเบียน')).toBeTruthy()
  expect(screen.getByText('รอบเวลา')).toBeTruthy()
})

test('test_TC_ACT_01_2_empty_form_is_available_for_authorized_organizer', () => {
  render(
    <CreateActivityRoute user={{ approved_by_admin: true, can_create_activity: true }}>
      <CreateActivityPage />
    </CreateActivityRoute>,
  )

  expect(screen.queryByText('เฉพาะผู้จัดกิจกรรมที่ได้รับสิทธิ์จาก Admin เท่านั้นที่สามารถเข้าถึงหน้า “สร้างกิจกรรมใหม่” ได้')).toBeNull()
  expect(screen.getByRole('button', { name: 'ตรวจสอบก่อนบันทึก' })).toBeTruthy()
  expect(screen.getByLabelText('ชื่อกิจกรรม')).toBeTruthy()
})

test('test_TC_ACT_01_3_unauthorized_or_unapproved_user_cannot_open_form', () => {
  render(
    <CreateActivityRoute user={{ approved_by_admin: false, can_create_activity: false }}>
      <CreateActivityPage />
    </CreateActivityRoute>,
  )

  expect(screen.getByText('เฉพาะผู้จัดกิจกรรมที่ได้รับสิทธิ์จาก Admin เท่านั้นที่สามารถเข้าถึงหน้า “สร้างกิจกรรมใหม่” ได้')).toBeTruthy()
  expect(screen.queryByLabelText('ชื่อกิจกรรม')).toBeNull()
})
