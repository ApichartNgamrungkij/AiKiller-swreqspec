import { render, screen } from '@testing-library/react'

import CollisionWarning from './CollisionWarning'
import StudentScheduleWarning from './StudentScheduleWarning'

// Supports AC-SRCH-03
test('test_AC_SRCH_03_overlap_shows_red_warning_and_keeps_detail_action', () => {
  render(
    <>
      <CollisionWarning
        message="มีช่วงเวลาคาบเกี่ยวกับตารางส่วนตัวของคุณ"
        overlappingPeriodLabels={['2026-11-07 09:00-10:00']}
      />
      <StudentScheduleWarning label="2026-11-07 09:00-10:00" />
    </>,
  )

  expect(screen.getByRole('alert').textContent).toContain('กิจกรรมชนกับตารางส่วนตัว')
  expect(screen.getByRole('button', { name: 'ดูรายละเอียดกิจกรรมต่อ' })).toBeTruthy()
  expect(screen.getByRole('note').textContent).toContain('2026-11-07 09:00-10:00')
})
