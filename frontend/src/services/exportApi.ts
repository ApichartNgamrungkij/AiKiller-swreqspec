export type GoogleSheetResponse = {
  activityId: number
  googleSheetUrl: string
}

export type ExportAccessResponse = {
  activityId: number
  canExport: boolean
  responseCount: number
  googleSheetUrl?: string
}

// Supports FR-EXP-01, ACC-GSHEET-01, ACC-GSHEET-02, NFR-SEC-01, NFR-SEC-02.
export async function fetchExportAccess(activityId: number): Promise<ExportAccessResponse> {
  const response = await fetch(`/activities/${activityId}/export-access`)
  if (!response.ok) {
    throw new Error('ไม่สามารถตรวจสอบสิทธิ์ดาวน์โหลดรายชื่อได้')
  }

  const payload = (await response.json()) as Partial<ExportAccessResponse>
  if (
    payload.activityId !== activityId ||
    typeof payload.canExport !== 'boolean' ||
    typeof payload.responseCount !== 'number'
  ) {
    throw new Error('ข้อมูลสิทธิ์ดาวน์โหลดรายชื่อไม่ถูกต้อง')
  }

  return payload as ExportAccessResponse
}

// Supports FR-EXP-02, IF-EXPORT-01, IF-GSHEET-01, ASM-05.
export async function fetchGoogleSheetUrl(activityId: number): Promise<string> {
  const response = await fetch(`/activities/${activityId}/google-sheet`)
  if (!response.ok) {
    throw new Error('ไม่สามารถเปิด Google Sheets ของกิจกรรมได้')
  }

  const payload = (await response.json()) as Partial<GoogleSheetResponse>
  if (
    payload.activityId !== activityId ||
    typeof payload.googleSheetUrl !== 'string' ||
    payload.googleSheetUrl.trim() === ''
  ) {
    throw new Error('Google Sheets URL ของกิจกรรมไม่พร้อมใช้งาน')
  }

  return payload.googleSheetUrl
}
