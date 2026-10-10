import React from 'react'

import { BusyPeriod, EMPTY_BUSY_PERIOD } from '../hooks/useSchedule'

export type BusyPeriodFormProps = {
  value?: BusyPeriod
  onChange: (next: BusyPeriod) => void
  onSubmit: (event: React.FormEvent<HTMLFormElement>) => void
  onCancel?: () => void
  isEditing?: boolean
}

// Supports FR-SCHED-02, FR-SCHED-03
export default function BusyPeriodForm({
  value = EMPTY_BUSY_PERIOD,
  onChange,
  onSubmit,
  onCancel,
  isEditing = false,
}: BusyPeriodFormProps) {
  const updateField = (field: keyof BusyPeriod, nextValue: string) => {
    onChange({
      ...value,
      [field]: nextValue,
    })
  }

  return (
    <form onSubmit={onSubmit} aria-label="busy-period-form">
      <h2>{isEditing ? 'แก้ไขช่วงเวลาที่ไม่ว่าง' : 'เพิ่มช่วงเวลาที่ไม่ว่าง'}</h2>

      <div>
        <label htmlFor="start-date">วันเริ่ม</label>
        <input
          id="start-date"
          name="startDate"
          type="date"
          value={value.startDate}
          onChange={(event) => updateField('startDate', event.target.value)}
          required
        />
      </div>

      <div>
        <label htmlFor="end-date">วันสิ้นสุด</label>
        <input
          id="end-date"
          name="endDate"
          type="date"
          value={value.endDate}
          onChange={(event) => updateField('endDate', event.target.value)}
          required
        />
      </div>

      <div>
        <label htmlFor="start-time">เวลาเริ่ม</label>
        <input
          id="start-time"
          name="startTime"
          type="time"
          value={value.startTime}
          onChange={(event) => updateField('startTime', event.target.value)}
          required
        />
      </div>

      <div>
        <label htmlFor="end-time">เวลาสิ้นสุด</label>
        <input
          id="end-time"
          name="endTime"
          type="time"
          value={value.endTime}
          onChange={(event) => updateField('endTime', event.target.value)}
          required
        />
      </div>

      <button type="submit">บันทึก</button>
      {onCancel ? (
        <button type="button" onClick={onCancel}>
          ยกเลิก
        </button>
      ) : null}
    </form>
  )
}
