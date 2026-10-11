import { useState } from 'react'

import type { ExportAccessMock } from '../mocks/exportAccess'
import { fetchGoogleSheetUrl } from '../services/exportApi'

export type ExportListButtonProps = {
  access: ExportAccessMock
  activityId?: number
}

// Supports FR-EXP-02, IF-EXPORT-01, IF-GSHEET-01, ACC-GSHEET-01, ACC-GSHEET-02.
export default function ExportListButton({
  access,
  activityId = access.activityId,
}: ExportListButtonProps) {
  const [error, setError] = useState<string | null>(null)
  const [isOpening, setIsOpening] = useState(false)

  if (!access.canExport || !access.hasAccess || access.responseCount < 1) {
    return null
  }

  async function openGoogleSheet() {
    setError(null)
    setIsOpening(true)
    try {
      const url = await fetchGoogleSheetUrl(activityId)
      window.open(url, '_blank', 'noopener,noreferrer')
    } catch (reason: unknown) {
      setError(reason instanceof Error ? reason.message : 'ไม่สามารถเปิด Google Sheets ได้')
    } finally {
      setIsOpening(false)
    }
  }

  return (
    <>
      <button
        type="button"
        aria-label="ดาวน์โหลดรายชื่อ"
        disabled={isOpening}
        onClick={openGoogleSheet}
      >
        {isOpening ? 'กำลังเปิด Google Sheets...' : 'ดาวน์โหลดรายชื่อ'}
      </button>
      {error && <p role="alert">{error}</p>}
    </>
  )
}
