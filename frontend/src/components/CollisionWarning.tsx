export type CollisionWarningProps = {
  message: string
  overlappingPeriodLabels: string[]
  onViewDetails?: () => void
}

// Supports FR-SRCH-02, FR-SRCH-03, IF — shows a red warning without blocking detail access.
export default function CollisionWarning({
  message,
  overlappingPeriodLabels,
  onViewDetails,
}: CollisionWarningProps) {
  return (
    <aside
      role="alert"
      aria-live="polite"
      style={{ border: '2px solid #dc2626', color: '#b91c1c', padding: '0.75rem' }}
    >
      <strong>คำเตือน: กิจกรรมชนกับตารางส่วนตัว</strong>
      <p>{message}</p>
      {overlappingPeriodLabels.length > 0 && (
        <ul>
          {overlappingPeriodLabels.map((label) => (
            <li key={label}>{label}</li>
          ))}
        </ul>
      )}
      <button type="button" onClick={onViewDetails}>
        ดูรายละเอียดกิจกรรมต่อ
      </button>
    </aside>
  )
}
