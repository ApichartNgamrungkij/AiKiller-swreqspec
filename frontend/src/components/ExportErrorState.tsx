export type ExportErrorStateProps = {
  message?: string
}

// Supports FR-EXP-01, FR-EXP-02, IF-GSHEET-01, IF-EXPORT-01, ASM-05.
export default function ExportErrorState({
  message = 'ไม่สามารถโหลดข้อมูลหรือเปิด Google Sheets ได้ในขณะนี้',
}: ExportErrorStateProps) {
  return (
    <div role="alert" className="border border-red-300 bg-red-50 p-3 text-red-900">
      {message}
    </div>
  )
}
