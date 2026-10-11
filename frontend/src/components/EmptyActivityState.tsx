// Supports FR-SRCH-04 and AC-SRCH-05
export default function EmptyActivityState() {
  return (
    <p role="status" aria-live="polite">
      ไม่พบกิจกรรมที่ตรงกับเงื่อนไข
    </p>
  )
}
