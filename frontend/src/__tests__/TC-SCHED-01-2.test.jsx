import React from 'react'
import { render, screen } from '@testing-library/react'

import SchedulePage from '../pages/SchedulePage'
import ScheduleRoute from '../routes/ScheduleRoute'

test('test_TC_SCHED_01_2_first_time_user_sees_empty_schedule_form', () => {
  render(
    <ScheduleRoute user={{ logged_in: true }}>
      <SchedulePage />
    </ScheduleRoute>,
  )

  expect(screen.getByRole('heading', { name: 'ตารางของฉัน' })).toBeTruthy()
  expect(screen.getAllByText('เพิ่มช่วงเวลาที่ไม่ว่าง').length).toBeGreaterThan(0)
  expect(screen.getByLabelText('วันเริ่ม')).toBeTruthy()
  expect(screen.getByLabelText('วันสิ้นสุด')).toBeTruthy()
  expect(screen.getByLabelText('เวลาเริ่ม')).toBeTruthy()
  expect(screen.getByLabelText('เวลาสิ้นสุด')).toBeTruthy()
  expect(screen.getByRole('button', { name: 'บันทึก' })).toBeTruthy()
})
