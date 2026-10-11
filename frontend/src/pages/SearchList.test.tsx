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
