export type OverlapWarningProps = {
  message: string
  matchingItems?: Array<{ label: string }>
  onContinue?: () => void
}

// Supports DOM-SCHED-01, FR-SCHED-05, FR-SCHED-06
export default function OverlapWarning({
  message,
  matchingItems = [],
  onContinue,
}: OverlapWarningProps) {
  return (
    <aside role="alert" aria-live="polite" data-testid="overlap-warning">
      <h2>คำเตือน: มีช่วงเวลาคาบเกี่ยว</h2>
      <p>{message}</p>

      {matchingItems.length > 0 && (
        <ul>
          {matchingItems.map((item, index) => (
            <li key={`${item.label}-${index}`}>{item.label}</li>
          ))}
        </ul>
      )}

      <button type="button" onClick={onContinue}>
        ไปยัง Google Form
      </button>
    </aside>
  )
}
