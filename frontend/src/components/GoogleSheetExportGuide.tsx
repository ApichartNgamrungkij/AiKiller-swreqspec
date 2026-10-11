export type GoogleSheetExportGuideProps = {
  googleSheetUrl: string
}

function buildExportUrl(googleSheetUrl: string, format: 'xlsx' | 'csv'): string {
  const url = new URL(googleSheetUrl)
  url.pathname = url.pathname.replace(/\/edit\/?$/, '/export')
  url.searchParams.set('format', format)
  return url.toString()
}

// Supports FR-EXP-03, FR-EXP-04, and ASM-03.
export default function GoogleSheetExportGuide({
  googleSheetUrl,
}: GoogleSheetExportGuideProps) {
  const xlsxUrl = buildExportUrl(googleSheetUrl, 'xlsx')
  const csvUrl = buildExportUrl(googleSheetUrl, 'csv')

  return (
    <section aria-label="ดาวน์โหลดข้อมูลจาก Google Sheets">
      <h2>ดาวน์โหลดรายชื่อ</h2>
      <p>ดาวน์โหลดข้อมูลทุกคอลัมน์จาก Google Sheets โดยไม่ปรับหรือตัดข้อมูล</p>
      <a href={xlsxUrl} target="_blank" rel="noreferrer">
        ดาวน์โหลดเป็น .xlsx
      </a>
      <a href={csvUrl} target="_blank" rel="noreferrer">
        ดาวน์โหลดเป็น .csv
      </a>
    </section>
  )
}
