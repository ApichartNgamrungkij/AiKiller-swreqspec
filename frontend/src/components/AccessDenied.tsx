// Supports ACC-VIEW-01, ACC-VIEW-02, FR-VIEW-05
export default function AccessDenied() {
  return (
    <section role="alert" aria-label="ปฏิเสธการเข้าถึง">
      <h1>Access Denied</h1>
      <p>คุณไม่มีสิทธิ์ดูข้อมูลผู้ลงทะเบียนของกิจกรรมนี้</p>
    </section>
  )
}
