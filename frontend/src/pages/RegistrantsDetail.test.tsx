import { render, screen } from '@testing-library/react'

import RegistrantsDetail from './RegistrantsDetail'

// Supports AC-VIEW-01
test('AC-VIEW-01: แสดงจำนวนและรายชื่อผู้ลงทะเบียนล่าสุด', () => {
  render(<RegistrantsDetail />)

  expect(screen.getByRole('status').textContent).toContain('ผู้ลงทะเบียนทั้งหมด: 2')
  expect(screen.getByText('660510001')).toBeTruthy()
  expect(screen.getByText('นายสมชาย ใจดี')).toBeTruthy()
  expect(screen.getByText('660510002')).toBeTruthy()
  expect(screen.getByText('นางสาวสมหญิง รักเรียน')).toBeTruthy()
  expect(screen.getByRole('table')).toBeTruthy()
})
