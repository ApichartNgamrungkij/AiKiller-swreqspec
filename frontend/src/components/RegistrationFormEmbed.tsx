import { useState } from 'react'
import type { RegistrationActivity } from '../mocks/registrationActivity'

export type RegistrationFormEmbedProps = {
  activity: Pick<RegistrationActivity, 'title' | 'status' | 'googleFormUrl'>
  onSubmitted?: () => void
}

// Supports FR-REG-01, FR-REG-02, IF-GFORM-01, IF-GFORM-02, CON-REG-01, and ASM-09.
export default function RegistrationFormEmbed({ activity, onSubmitted }: RegistrationFormEmbedProps) {
  const [submitted, setSubmitted] = useState(false)
  const [name, setName] = useState('')
  const [studentId, setStudentId] = useState('')
  const isRegistrationClosed = activity.status === 'full'
  if (isRegistrationClosed) {
    return null
  }

  return (
    <section aria-label="Google Form สำหรับลงทะเบียน">
      <h2>ลงทะเบียนกิจกรรม</h2>
      <div
        aria-label={`Google Form จำลองสำหรับ ${activity.title}`}
        data-form-url={activity.googleFormUrl}
        role="region"
      >
        <p>พื้นที่ Google Form จำลอง</p>
        {submitted ? <p role="status">ส่งข้อมูลการลงทะเบียนแล้ว ระบบบันทึกคำตอบลง Google Sheets สำเร็จ</p> : <form onSubmit={(event) => { event.preventDefault(); if (!name.trim() || !studentId.trim()) return; setSubmitted(true); onSubmitted?.() }}><label htmlFor="registration-student-id">รหัสนักศึกษา</label><input id="registration-student-id" value={studentId} onChange={(event) => setStudentId(event.target.value)} required /><label htmlFor="registration-name">ชื่อ-นามสกุล</label><input id="registration-name" value={name} onChange={(event) => setName(event.target.value)} required /><button type="submit">ส่ง Google Form</button></form>}
      </div>
    </section>
  )
}
