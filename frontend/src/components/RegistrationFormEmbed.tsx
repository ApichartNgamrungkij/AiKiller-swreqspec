import type { RegistrationActivity } from '../mocks/registrationActivity'

export type RegistrationFormEmbedProps = {
  activity: Pick<RegistrationActivity, 'title' | 'status' | 'googleFormUrl'>
}

// Supports FR-REG-01, FR-REG-02, IF-GFORM-01, IF-GFORM-02, CON-REG-01, and ASM-09.
export default function RegistrationFormEmbed({ activity }: RegistrationFormEmbedProps) {
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
        <p>นักศึกษาสามารถกรอกข้อมูลการลงทะเบียนในฟอร์มนี้</p>
      </div>
    </section>
  )
}
