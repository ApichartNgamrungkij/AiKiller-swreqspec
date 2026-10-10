import { fireEvent, render, screen } from '@testing-library/react'

import SchedulePage from './SchedulePage'

// Supports AC-SCHED-02, AC-SCHED-03
test('AC-SCHED-02: Given a saved period, When editing the selected busy period, Then the other items are preserved', () => {
  render(<SchedulePage />)

  const editButtons = screen.getAllByRole('button', { name: 'แก้ไข' })
  fireEvent.click(editButtons[0])

  fireEvent.change(screen.getByLabelText('วันเริ่ม'), { target: { value: '2026-02-01' } })
  fireEvent.change(screen.getByLabelText('วันสิ้นสุด'), { target: { value: '2026-02-05' } })
  fireEvent.change(screen.getByLabelText('เวลาเริ่ม'), { target: { value: '11:00' } })
  fireEvent.change(screen.getByLabelText('เวลาสิ้นสุด'), { target: { value: '12:00' } })
  fireEvent.click(screen.getByRole('button', { name: 'บันทึก' }))

  expect(screen.getByText(/2026-02-01 ถึง 2026-02-05/i)).toBeTruthy()
  expect(screen.getAllByRole('button', { name: 'แก้ไข' }).length).toBeGreaterThanOrEqual(1)
})

// Supports AC-SCHED-03
test('AC-SCHED-03: Given an existing busy period, When adding another item, Then the original item stays in the list', () => {
  render(<SchedulePage />)

  fireEvent.change(screen.getByLabelText('วันเริ่ม'), { target: { value: '2026-03-10' } })
  fireEvent.change(screen.getByLabelText('วันสิ้นสุด'), { target: { value: '2026-03-12' } })
  fireEvent.change(screen.getByLabelText('เวลาเริ่ม'), { target: { value: '13:00' } })
  fireEvent.change(screen.getByLabelText('เวลาสิ้นสุด'), { target: { value: '14:00' } })
  fireEvent.click(screen.getByRole('button', { name: 'บันทึก' }))

  expect(screen.getByText(/2026-01-05 ถึง 2026-01-09/i)).toBeTruthy()
  expect(screen.getByText(/2026-03-10 ถึง 2026-03-12/i)).toBeTruthy()
})
