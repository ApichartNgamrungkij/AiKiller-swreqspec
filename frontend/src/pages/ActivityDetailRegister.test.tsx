import { render, screen } from '@testing-library/react'

import ActivityDetailPage from './ActivityDetail'
import { registrationActivity } from '../mocks/registrationActivity'

// Supports AC-REG-01.
test('test_AC_REG_01_embeds_form_for_available_activity', () => {
  render(<ActivityDetailPage activity={registrationActivity} />)

  expect(screen.getByRole('region', { name: 'Google Form สำหรับลงทะเบียน' })).toBeTruthy()
  expect(screen.getByText('พื้นที่ Google Form จำลอง')).toBeTruthy()
})

// Supports CON-REG-01.
test('does_not_embed_form_for_full_activity', () => {
  render(
    <ActivityDetailPage
      activity={{
        ...registrationActivity,
        status: 'full',
      }}
    />,
  )

  expect(screen.queryByRole('region', { name: 'Google Form สำหรับลงทะเบียน' })).toBeNull()
})
