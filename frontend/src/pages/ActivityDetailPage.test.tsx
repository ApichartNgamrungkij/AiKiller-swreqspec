import { render, screen } from '@testing-library/react'

import ActivityDetailPage from './ActivityDetailPage'

// Supports AC-SCHED-05
test('AC-SCHED-05: Given a saved personal schedule, When the activity time overlaps, Then a warning is shown', () => {
  render(
    <ActivityDetailPage
      title="กิจกรรมที่มีช่วงเวลาชน"
      activityStart="2026-01-05T15:30"
      activityEnd="2026-01-05T16:30"
      busyPeriods={[
        {
          id: 7,
          start_date: '2026-01-02',
          end_date: '2026-01-08',
          start_time: '14:00',
          end_time: '16:00',
        },
      ]}
    />,
  )

  const alert = screen.getByRole('alert')
  expect(alert.textContent).toMatch(/มีช่วงเวลาคาบเกี่ยว/)
})

// Supports AC-SCHED-06
test('AC-SCHED-06: Given a scheduling conflict warning, When the student proceeds to Google Form, Then the action remains available without blocking', () => {
  render(
    <ActivityDetailPage
      title="กิจกรรมที่มีวันเวลาเกิน"
      activityStart="2026-01-05T09:30"
      activityEnd="2026-01-05T10:30"
      busyPeriods={[
        {
          id: 12,
          start_date: '2026-01-05',
          end_date: '2026-01-05',
          start_time: '09:00',
          end_time: '10:00',
        },
      ]}
    />,
  )

  const warning = screen.getByRole('alert')
  expect(warning.textContent).toMatch(/มีช่วงเวลาคาบเกี่ยว/)

  const continueButton = screen.getByRole('button', { name: 'ไปยัง Google Form' })
  expect((continueButton as HTMLButtonElement).disabled).toBe(false)
})

// Supports AC-SCHED-07
test('AC-SCHED-07: Given saved busy periods, When checking activity timings, Then the saved schedule is used for the comparison', () => {
  render(
    <ActivityDetailPage
      title="กิจกรรมที่ตรวจซ้ำ"
      activityStart="2026-03-04T08:45"
      activityEnd="2026-03-04T09:15"
      busyPeriods={[
        {
          id: 9,
          start_date: '2026-03-01',
          end_date: '2026-03-10',
          start_time: '08:30',
          end_time: '09:30',
        },
      ]}
    />,
  )

  expect(screen.getByRole('alert').textContent).toMatch(/มีช่วงเวลาคาบเกี่ยว/)
  expect(screen.getByText(/2026-03-01 ถึง 2026-03-10/i)).toBeTruthy()
})
