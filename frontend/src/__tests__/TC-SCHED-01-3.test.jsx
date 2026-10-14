import React from 'react'
import { render, screen } from '@testing-library/react'

import ScheduleRoute from '../routes/ScheduleRoute'

test('test_TC_SCHED_01_3_guest_cannot_access_schedule_page', () => {
  render(<ScheduleRoute user={null} />)

  expect(screen.getByText(/กรุณาเข้าสู่ระบบก่อนใช้งานฟีเจอร์ตารางของฉัน/i)).toBeTruthy()
  expect(screen.queryByText('เพิ่มช่วงเวลาที่ไม่ว่าง')).toBeNull()
  expect(screen.queryByLabelText('วันเริ่ม')).toBeNull()
})
