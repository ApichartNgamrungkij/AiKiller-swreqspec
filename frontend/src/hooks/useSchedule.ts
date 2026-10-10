import { useMemo, useState } from 'react'

export type BusyPeriod = {
  id?: number
  startDate: string
  endDate: string
  startTime: string
  endTime: string
}

export const EMPTY_BUSY_PERIOD: BusyPeriod = {
  startDate: '',
  endDate: '',
  startTime: '09:00',
  endTime: '10:00',
}

// Supports FR-SCHED-02, FR-SCHED-03, CON-SCHED-01
export function saveBusyPeriod(schedule: BusyPeriod[], draft: BusyPeriod): BusyPeriod[] {
  const nextDraft = {
    ...draft,
    id: draft.id ?? Date.now(),
  }

  if (draft.id != null) {
    return schedule.map((period) => (period.id === draft.id ? nextDraft : period))
  }

  return [...schedule, nextDraft]
}

// Supports FR-SCHED-02, FR-SCHED-03
export function useSchedule(initialSchedule: BusyPeriod[] = []) {
  const [schedule, setSchedule] = useState<BusyPeriod[]>(initialSchedule)
  const [draft, setDraft] = useState<BusyPeriod>(EMPTY_BUSY_PERIOD)
  const [selectedId, setSelectedId] = useState<number | undefined>(undefined)

  const selectedPeriod = useMemo(
    () => schedule.find((period) => period.id === selectedId),
    [schedule, selectedId],
  )

  const resetDraft = () => {
    setSelectedId(undefined)
    setDraft(EMPTY_BUSY_PERIOD)
  }

  const handleSave = (nextPeriod: BusyPeriod) => {
    setSchedule((current) => saveBusyPeriod(current, nextPeriod))
    resetDraft()
  }

  const handleEdit = (period: BusyPeriod) => {
    setSelectedId(period.id)
    setDraft({ ...period })
  }

  return {
    schedule,
    draft,
    selectedId,
    selectedPeriod,
    setDraft,
    handleSave,
    handleEdit,
    resetDraft,
  }
}
