export type AvailabilitySlot = {
  date: string
  startTime: string
  endTime: string
}

export type StudentSchedule = {
  studentId: string
  availabilitySlots: AvailabilitySlot[]
  lastUpdatedAt: string
}

// Supports FR-SRCH-02 and FR-SRCH-03; this is student-entered availability only.
export const mockStudentSchedule: StudentSchedule = {
  studentId: 'S-001',
  availabilitySlots: [
    {
      date: '2026-11-07',
      startTime: '08:00',
      endTime: '17:00',
    },
    {
      date: '2026-11-14',
      startTime: '08:00',
      endTime: '10:00',
    },
  ],
  lastUpdatedAt: '2026-10-10T12:00:00+07:00',
}
