import { render, screen } from '@testing-library/react'

import RegistrantsDetail from './RegistrantsDetail'

// Supports AC-VIEW-04
test('AC-VIEW-04: นักศึกษาทั่วไปเห็นข้อความ Access Denied', () => {
  render(<RegistrantsDetail isAccessDenied />)

  expect(screen.getByRole('heading', { name: 'Access Denied' })).toBeTruthy()
  expect(screen.getByText(/ไม่มีสิทธิ์ดูข้อมูลผู้ลงทะเบียน/)).toBeTruthy()
})

// Supports AC-VIEW-05
test('AC-VIEW-05: ผู้มีสิทธิ์ดูข้อมูลผู้ลงทะเบียนได้', () => {
  render(<RegistrantsDetail registrants={[]} />)

  expect(screen.getByRole('heading', { name: 'รายชื่อผู้ลงทะเบียน' })).toBeTruthy()
  expect(screen.getByText('ยังไม่มีผู้ลงทะเบียน')).toBeTruthy()
})
