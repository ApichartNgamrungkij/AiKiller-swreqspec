import { afterEach, beforeEach, vi } from 'vitest'

import { submitRegistrationForm } from './registrationForm'

beforeEach(() => {
  vi.stubGlobal(
    'fetch',
    vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        activityId: 1,
        googleSheetId: 'sheet-activity-1',
        submitted: true,
      }),
    }),
  )
})

afterEach(() => {
  vi.unstubAllGlobals()
})

// Supports AC-REG-02.
test('test_AC_REG_02_google_form_response_is_saved', async () => {
  const result = await submitRegistrationForm(
    1,
    'sheet-activity-1',
    { studentId: '660510001', fullName: 'นายสมชาย ใจดี' },
  )

  expect(result.submitted).toBe(true)
  expect(fetch).toHaveBeenCalledWith(
    '/api/activities/1/registration-form',
    expect.objectContaining({
      method: 'POST',
      body: JSON.stringify({
        googleSheetId: 'sheet-activity-1',
        formData: { studentId: '660510001', fullName: 'นายสมชาย ใจดี' },
      }),
    }),
  )
})
