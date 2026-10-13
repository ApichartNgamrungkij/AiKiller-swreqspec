import { render, screen } from '@testing-library/react'

import ActivityDetailPage from './ActivityDetail'
import { mockActivities } from '../mocks/activities'

// Supports AC-SRCH-04
test('test_AC_SRCH_04_detail_view_shows_required_fields', () => {
  render(<ActivityDetailPage activity={mockActivities[0]} />)

  expect(screen.getByText('6 ชั่วโมง')).toBeTruthy()
  expect(screen.getByText(/ค่ายอาสาพัฒนาชุมชน/)).toBeTruthy()
  expect(screen.getByText(/วันเวลา/)).toBeTruthy()
  expect(screen.getByText(/7 พฤศจิกายน 2569/)).toBeTruthy()
  expect(screen.getByText(/09:00/)).toBeTruthy()
  expect(screen.getByText(/16:00/)).toBeTruthy()
  expect(screen.getByText(/ศูนย์ชุมชนคลองสาม/)).toBeTruthy()

  const registrationLink = screen.getByRole('link', {
    name: 'ไปยัง Google Form สำหรับลงทะเบียนต่อ',
  })
  expect(registrationLink.getAttribute('href')).toBe('https://forms.google.com/community-service')
})
