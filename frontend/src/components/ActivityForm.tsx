import React from 'react'

export type ActivitySlotDraft = {
  slot_date: string
  startTime: string
  endTime: string
  label: string
}

export type ActivityFormValues = {
  title: string
  category: string
  venue: string
  maxParticipants: string
  volunteerHours: string
  registrationUrl: string
  slots: ActivitySlotDraft[]
}

export type ActivityFormProps = {
  value: ActivityFormValues
  onChange: (next: ActivityFormValues) => void
  onSubmit: (event: React.FormEvent<HTMLFormElement>) => void
  onAddSlot: () => void
  onRemoveSlot: (index: number) => void
  submitLabel?: string
}

const ACTIVITY_CATEGORIES = ['วิชาการ', 'กีฬา', 'ศิลปวัฒนธรรม', 'คุณธรรมจริยธรรม', 'บำเพ็ญประโยชน์']

// Supports FR-ACT-01, FR-ACT-02, FR-ACT-03, ASM-ACT-02, ASM-ACT-03, ASM-ACT-04, ASM-ACT-05
export default function ActivityForm({
  value,
  onChange,
  onSubmit,
  onAddSlot,
  onRemoveSlot,
  submitLabel = 'ตรวจสอบก่อนบันทึก',
}: ActivityFormProps) {
  const updateField = (field: keyof ActivityFormValues, nextValue: string | ActivitySlotDraft[]) => {
    onChange({
      ...value,
      [field]: nextValue,
    })
  }

  const updateSlot = (index: number, field: keyof ActivitySlotDraft, nextValue: string) => {
    const nextSlots = value.slots.map((slot, slotIndex) =>
      slotIndex === index ? { ...slot, [field]: nextValue } : slot,
    )
    updateField('slots', nextSlots)
  }

  return (
    <form onSubmit={onSubmit} aria-label="activity-form">
      <h2>สร้างกิจกรรมใหม่</h2>

      <div>
        <label htmlFor="activity-title">ชื่อกิจกรรม</label>
        <input
          id="activity-title"
          name="title"
          value={value.title}
          onChange={(event) => updateField('title', event.target.value)}
        />
      </div>

      <div>
        <label htmlFor="activity-category">ประเภทกิจกรรม</label>
        <select
          id="activity-category"
          name="category"
          value={value.category}
          onChange={(event) => updateField('category', event.target.value)}
        >
          {ACTIVITY_CATEGORIES.map((category) => (
            <option key={category} value={category}>
              {category}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label htmlFor="activity-venue">สถานที่จัด</label>
        <input
          id="activity-venue"
          name="venue"
          value={value.venue}
          onChange={(event) => updateField('venue', event.target.value)}
        />
      </div>

      <div>
        <label htmlFor="activity-max-participants">จำนวนรับสมัคร</label>
        <input
          id="activity-max-participants"
          name="maxParticipants"
          type="number"
          min={1}
          value={value.maxParticipants}
          onChange={(event) => updateField('maxParticipants', event.target.value)}
        />
      </div>

      <div>
        <label htmlFor="activity-volunteer-hours">ชั่วโมงจิตอาสาที่จะได้รับ</label>
        <input
          id="activity-volunteer-hours"
          name="volunteerHours"
          type="number"
          min={0}
          value={value.volunteerHours}
          onChange={(event) => updateField('volunteerHours', event.target.value)}
        />
      </div>

      <div>
        <label htmlFor="activity-registration-url">ลิงก์ URL สำหรับลงทะเบียน</label>
        <input
          id="activity-registration-url"
          name="registrationUrl"
          type="url"
          value={value.registrationUrl}
          onChange={(event) => updateField('registrationUrl', event.target.value)}
          placeholder="https://example.com/register"
        />
      </div>

      <fieldset>
        <legend>รอบเวลา</legend>
        {value.slots.map((slot, index) => (
          <div key={`${slot.label}-${index}`}>
            <label htmlFor={`slot-date-${index}`}>วันที่</label>
            <input
              id={`slot-date-${index}`}
              type="date"
              value={slot.slot_date}
              onChange={(event) => updateSlot(index, 'slot_date', event.target.value)}
            />

            <label htmlFor={`slot-label-${index}`}>ชื่อรอบ</label>
            <input
              id={`slot-label-${index}`}
              type="text"
              value={slot.label}
              onChange={(event) => updateSlot(index, 'label', event.target.value)}
              placeholder="เช้า / บ่าย"
            />

            <label htmlFor={`slot-start-${index}`}>เวลาเริ่ม</label>
            <input
              id={`slot-start-${index}`}
              type="time"
              value={slot.startTime}
              onChange={(event) => updateSlot(index, 'startTime', event.target.value)}
            />

            <label htmlFor={`slot-end-${index}`}>เวลาสิ้นสุด</label>
            <input
              id={`slot-end-${index}`}
              type="time"
              value={slot.endTime}
              onChange={(event) => updateSlot(index, 'endTime', event.target.value)}
            />

            {value.slots.length > 1 ? (
              <button type="button" onClick={() => onRemoveSlot(index)}>
                ลบรอบนี้
              </button>
            ) : null}
          </div>
        ))}

        <button type="button" onClick={onAddSlot}>
          เพิ่มรอบเวลา
        </button>
      </fieldset>

      <button type="submit">{submitLabel}</button>
    </form>
  )
}
