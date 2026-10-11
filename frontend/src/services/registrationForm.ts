export type RegistrationFormData = Record<string, string>

export type RegistrationFormResponse = {
  activityId: number
  googleSheetId: string
  submitted: boolean
}

// Supports FR-REG-02, FR-REG-03, IF-GFORM-01, and IF-GSHEET-01.
export async function submitRegistrationForm(
  activityId: number,
  googleSheetId: string,
  formData: RegistrationFormData,
): Promise<RegistrationFormResponse> {
  if (!googleSheetId.trim()) {
    throw new Error('googleSheetId is required')
  }

  const response = await fetch(`/api/activities/${activityId}/registration-form`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ googleSheetId, formData }),
  })

  if (!response.ok) {
    throw new Error(`ไม่สามารถส่งข้อมูลลงทะเบียนได้ (${response.status})`)
  }

  return (await response.json()) as RegistrationFormResponse
}
