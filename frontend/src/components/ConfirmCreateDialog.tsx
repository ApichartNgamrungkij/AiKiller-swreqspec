import React from 'react'

import type { ActivityFormValues } from './ActivityForm'

export type ConfirmCreateDialogProps = {
  open: boolean
  draft: ActivityFormValues
  onConfirm: () => void
  onCancel: () => void
}

// Supports FR-ACT-01, FR-ACT-02, FR-ACT-03, ASM-ACT-02, ASM-ACT-03, ASM-ACT-04, ASM-ACT-05
export default function ConfirmCreateDialog({ open, draft, onConfirm, onCancel }: ConfirmCreateDialogProps) {
  if (!open) return null

  return (
    <div role="dialog" aria-modal="true" aria-label="confirm-create-activity">
      <h3>ตรวจสอบข้อมูลก่อนบันทึก</h3>
      <dl>
        <dt>ชื่อกิจกรรม</dt>
        <dd>{draft.title}</dd>

        <dt>ประเภท</dt>
        <dd>{draft.category}</dd>

        <dt>สถานที่จัด</dt>
        <dd>{draft.venue}</dd>

        <dt>จำนวนรับสมัคร</dt>
        <dd>{draft.maxParticipants}</dd>

        <dt>ชั่วโมงจิตอาสา</dt>
        <dd>{draft.volunteerHours}</dd>

        <dt>URL สำหรับลงทะเบียน</dt>
        <dd>{draft.registrationUrl || '—'}</dd>
      </dl>

      <ul>
        {draft.slots.map((slot, index) => (
          <li key={`${slot.slot_date}-${index}`}>
            {slot.label || `รอบ ${index + 1}`} : {slot.slot_date} {slot.startTime} - {slot.endTime}
          </li>
        ))}
      </ul>

      <button type="button" onClick={onConfirm}>ยืนยันสร้างกิจกรรม</button>
      <button type="button" onClick={onCancel}>กลับไปแก้ไข</button>
    </div>
  )
}
