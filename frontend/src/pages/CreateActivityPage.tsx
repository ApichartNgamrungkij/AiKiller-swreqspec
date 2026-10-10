import React, { useMemo, useState } from 'react'

import ActivityForm, { type ActivityFormValues } from '../components/ActivityForm'
import ConfirmCreateDialog from '../components/ConfirmCreateDialog'

export type CreateActivityPageProps = {
  onCreate?: (payload: ActivityFormValues) => void
}

const EMPTY_SLOT = {
  slot_date: '',
  startTime: '09:00',
  endTime: '12:00',
  label: 'เช้า',
}

const createEmptyDraft = (): ActivityFormValues => ({
  title: '',
  category: 'วิชาการ',
  venue: '',
  maxParticipants: '',
  volunteerHours: '',
  registrationUrl: '',
  slots: [EMPTY_SLOT],
})

// Supports FR-ACT-01, FR-ACT-02, FR-ACT-03, ASM-ACT-02, ASM-ACT-03, ASM-ACT-04, ASM-ACT-05
export default function CreateActivityPage({ onCreate }: CreateActivityPageProps) {
  const [draft, setDraft] = useState<ActivityFormValues>(createEmptyDraft)
  const [isConfirmOpen, setIsConfirmOpen] = useState(false)
  const [validationMessage, setValidationMessage] = useState('')

  const hasRequiredFields = useMemo(() => {
    return Boolean(
      draft.title.trim()
      && draft.category.trim()
      && draft.venue.trim()
      && draft.maxParticipants.trim()
      && draft.volunteerHours.trim()
      && draft.slots.length > 0
      && draft.slots.every((slot) => slot.slot_date && slot.startTime && slot.endTime),
    )
  }, [draft])

  const validateDraft = () => {
    const missingFields: string[] = []

    if (!draft.title.trim()) missingFields.push('ชื่อกิจกรรม')
    if (!draft.category.trim()) missingFields.push('ประเภทกิจกรรม')
    if (!draft.venue.trim()) missingFields.push('สถานที่จัด')
    if (!draft.maxParticipants.trim()) missingFields.push('จำนวนรับสมัคร')
    if (!draft.volunteerHours.trim()) missingFields.push('ชั่วโมงจิตอาสาที่จะได้รับ')
    if (draft.slots.length === 0) missingFields.push('รอบเวลา')

    const invalidSlot = draft.slots.find((slot) => !slot.slot_date || !slot.startTime || !slot.endTime)
    if (invalidSlot) missingFields.push('วันและเวลาในรอบกิจกรรม')

    if (draft.registrationUrl && !/^https?:\/\//i.test(draft.registrationUrl)) {
      return 'URL สำหรับลงทะเบียนต้องเป็นลิงก์ที่ถูกต้อง'
    }

    if (missingFields.length > 0) {
      return `กรุณากรอกข้อมูลที่จำเป็น: ${missingFields.join(', ')}`
    }

    return ''
  }

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()

    const message = validateDraft()
    if (message) {
      setValidationMessage(message)
      setIsConfirmOpen(false)
      return
    }

    setValidationMessage('')
    setIsConfirmOpen(true)
  }

  const handleConfirm = () => {
    setIsConfirmOpen(false)
    if (onCreate) {
      onCreate(draft)
    }
  }

  const addSlot = () => {
    setDraft((current) => ({
      ...current,
      slots: [...current.slots, { ...EMPTY_SLOT, label: `รอบ ${current.slots.length + 1}` }],
    }))
  }

  const removeSlot = (index: number) => {
    setDraft((current) => ({
      ...current,
      slots: current.slots.filter((_, slotIndex) => slotIndex !== index),
    }))
  }

  return (
    <main>
      <h1>สร้างกิจกรรมใหม่</h1>

      <ActivityForm
        value={draft}
        onChange={setDraft}
        onSubmit={handleSubmit}
        onAddSlot={addSlot}
        onRemoveSlot={removeSlot}
      />

      {validationMessage ? <p role="alert">{validationMessage}</p> : null}

      <ConfirmCreateDialog
        open={isConfirmOpen}
        draft={draft}
        onConfirm={handleConfirm}
        onCancel={() => setIsConfirmOpen(false)}
      />
    </main>
  )
}
