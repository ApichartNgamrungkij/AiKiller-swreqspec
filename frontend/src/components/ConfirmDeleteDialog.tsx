import { useState } from 'react'

// Supports FR-DEL-03, FR-DEL-04, IF-REASON-01, ASM-01
export function validateReason(reason) {
  if (!reason || !reason.trim()) {
    return 'กรุณาระบุเหตุผลก่อนยืนยันการลบ/ระงับกิจกรรม'
  }
  return ''
}

export default function ConfirmDeleteDialog({
  activityTitle = 'กิจกรรม',
  actionType = 'delete',
  onConfirm,
  onCancel,
}) {
  const [reason, setReason] = useState('')
  const [error, setError] = useState('')

  const handleSubmit = () => {
    const nextError = validateReason(reason)
    if (nextError) {
      setError(nextError)
      return
    }

    setError('')
    onConfirm?.(reason.trim())
  }

  return (
    <div aria-label="confirm-delete-dialog">
      <h2>ยืนยันการ{actionType === 'delete' ? 'ลบ' : 'ระงับ'}กิจกรรม</h2>
      <p>กิจกรรม: {activityTitle}</p>

      <label htmlFor="activity-reason">เหตุผล</label>
      <textarea
        id="activity-reason"
        value={reason}
        onChange={(event) => {
          setReason(event.target.value)
          if (error) setError('')
        }}
        placeholder="กรอกเหตุผลก่อนยืนยัน"
      />

      {error ? <p role="alert">{error}</p> : null}

      <button type="button" onClick={handleSubmit}>
        ยืนยัน
      </button>
      <button type="button" onClick={onCancel}>
        ยกเลิก
      </button>
    </div>
  )
}
