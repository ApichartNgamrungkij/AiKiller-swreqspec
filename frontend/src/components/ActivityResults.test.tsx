import { render, screen } from '@testing-library/react'

import ActivityResults from './ActivityResults'

// Supports AC-SRCH-05
test('test_AC_SRCH_05_no_result_message', () => {
  render(<ActivityResults activities={[]} />)

  expect(screen.getByRole('status').textContent).toContain('ไม่พบกิจกรรมที่ตรงกับเงื่อนไข')
})
