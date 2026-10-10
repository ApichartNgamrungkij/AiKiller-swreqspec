import React, { useState } from 'react'

import BusyPeriodForm from '../components/BusyPeriodForm'
import { BusyPeriod, EMPTY_BUSY_PERIOD, useSchedule } from '../hooks/useSchedule'

// Supports FR-SCHED-01, FR-SCHED-02, FR-SCHED-03, CON-SCHED-01
export default function SchedulePage() {
  const [initialSchedule] = useState<BusyPeriod[]>([
    {
      id: 1,
      startDate: '2026-01-05',
      endDate: '2026-01-09',
      startTime: '09:00',
      endTime: '10:00',
    },
  ])

  const { schedule, draft, handleEdit, handleSave, resetDraft, setDraft } = useSchedule(initialSchedule)

  const onSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!draft.startDate || !draft.endDate || !draft.startTime || !draft.endTime) {
      return
    }
    handleSave(draft)
  }

  return (
    <main>
      <h1>ตารางของฉัน</h1>
      <p>เพิ่มช่วงเวลาที่ไม่ว่าง</p>

      <section aria-label="schedule-list">
        {schedule.length === 0 ? (
          <p>ยังไม่มีรายการช่วงเวลาที่ไม่ว่าง</p>
        ) : (
          <ul>
            {schedule.map((period) => (
              <li key={period.id ?? `${period.startDate}-${period.startTime}`}>
                {period.startDate} ถึง {period.endDate} • {period.startTime} - {period.endTime}
                <button type="button" onClick={() => handleEdit(period)}>
                  แก้ไข
                </button>
              </li>
            ))}
          </ul>
        )}
      </section>

      <BusyPeriodForm
        value={draft}
        isEditing={draft.id != null}
        onChange={setDraft}
        onSubmit={onSubmit}
        onCancel={resetDraft}
      />
    </main>
  )
}

export const __sampleBusyPeriod = EMPTY_BUSY_PERIOD
