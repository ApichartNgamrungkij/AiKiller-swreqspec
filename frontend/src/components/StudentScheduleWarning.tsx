export type StudentScheduleWarningProps = {
  label: string
}

// Supports FR-SRCH-02, FR-SRCH-03, IF — identifies the student-entered schedule period that overlaps.
export default function StudentScheduleWarning({ label }: StudentScheduleWarningProps) {
  return (
    <p role="note" style={{ color: '#b91c1c' }}>
      ตารางส่วนตัวที่ชน: {label}
    </p>
  )
}
