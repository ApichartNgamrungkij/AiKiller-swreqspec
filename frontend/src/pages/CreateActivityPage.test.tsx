import { fireEvent, render, screen } from '@testing-library/react'

import CreateActivityPage from './CreateActivityPage'

// Supports AC-ACT-02
test('AC-ACT-02: Given a user is on the create-activity page, When they fill in the required fields and slot details, Then the form accepts the activity metadata and same-day multiple slots', () => {
  render(<CreateActivityPage />)

  fireEvent.change(screen.getByLabelText('ชื่อกิจกรรม'), { target: { value: 'โครงการวันจิตอาสา' } })
  fireEvent.change(screen.getByLabelText('ประเภทกิจกรรม'), { target: { value: 'วิชาการ' } })
  fireEvent.change(screen.getByLabelText('สถานที่จัด'), { target: { value: 'หอประชุมใหญ่' } })
  fireEvent.change(screen.getByLabelText('จำนวนรับสมัคร'), { target: { value: '120' } })
  fireEvent.change(screen.getByLabelText('ชั่วโมงจิตอาสาที่จะได้รับ'), { target: { value: '8' } })
  fireEvent.change(screen.getByLabelText('วันที่'), { target: { value: '2026-02-12' } })
  fireEvent.change(screen.getByLabelText('เวลาเริ่ม'), { target: { value: '09:00' } })
  fireEvent.change(screen.getByLabelText('เวลาสิ้นสุด'), { target: { value: '12:00' } })

  fireEvent.click(screen.getByRole('button', { name: 'เพิ่มรอบเวลา' }))

  expect((screen.getByLabelText('ชื่อกิจกรรม') as HTMLInputElement).value).toBe('โครงการวันจิตอาสา')
  expect((screen.getByLabelText('ประเภทกิจกรรม') as HTMLSelectElement).value).toBe('วิชาการ')
  expect(screen.getAllByLabelText('วันที่')).toHaveLength(2)
})

// Supports AC-ACT-03
test('AC-ACT-03: Given a user adds a registration URL, When they review the draft, Then the URL is kept with the activity', () => {
  render(<CreateActivityPage />)

  fireEvent.change(screen.getByLabelText('ชื่อกิจกรรม'), { target: { value: 'กิจกรรมฝึกอบรม' } })
  fireEvent.change(screen.getByLabelText('สถานที่จัด'), { target: { value: 'อาคารวิจัย' } })
  fireEvent.change(screen.getByLabelText('จำนวนรับสมัคร'), { target: { value: '50' } })
  fireEvent.change(screen.getByLabelText('ชั่วโมงจิตอาสาที่จะได้รับ'), { target: { value: '3' } })
  fireEvent.change(screen.getByLabelText('วันที่'), { target: { value: '2026-03-20' } })
  fireEvent.change(screen.getByLabelText('เวลาเริ่ม'), { target: { value: '08:30' } })
  fireEvent.change(screen.getByLabelText('เวลาสิ้นสุด'), { target: { value: '10:30' } })
  fireEvent.change(screen.getByLabelText('ลิงก์ URL สำหรับลงทะเบียน'), { target: { value: 'https://example.com/register' } })

  fireEvent.click(screen.getByRole('button', { name: 'ตรวจสอบก่อนบันทึก' }))

  expect(screen.getByRole('dialog', { name: 'confirm-create-activity' })).toBeTruthy()
  expect(screen.getByText('https://example.com/register')).toBeTruthy()
})

// Supports AC-ACT-04
test('AC-ACT-04: Given required fields are still missing, When the user submits the form, Then the validation message is shown and confirmation is blocked', () => {
  render(<CreateActivityPage />)

  fireEvent.click(screen.getByRole('button', { name: 'ตรวจสอบก่อนบันทึก' }))

  expect(screen.getByRole('alert').textContent).toMatch(/กรุณากรอกข้อมูลที่จำเป็น/i)
  expect(screen.queryByRole('dialog', { name: 'confirm-create-activity' })).toBeNull()
})

// Supports AC-ACT-05
test('AC-ACT-05: Given the form is complete, When the user confirms the create action, Then the create callback receives the submitted activity payload', () => {
  const handleCreate = vi.fn()
  render(<CreateActivityPage onCreate={handleCreate} />)

  fireEvent.change(screen.getByLabelText('ชื่อกิจกรรม'), { target: { value: 'กิจกรรมบำเพ็ญประโยชน์' } })
  fireEvent.change(screen.getByLabelText('ประเภทกิจกรรม'), { target: { value: 'บำเพ็ญประโยชน์' } })
  fireEvent.change(screen.getByLabelText('สถานที่จัด'), { target: { value: 'ศูนย์บริการชุมชน' } })
  fireEvent.change(screen.getByLabelText('จำนวนรับสมัคร'), { target: { value: '35' } })
  fireEvent.change(screen.getByLabelText('ชั่วโมงจิตอาสาที่จะได้รับ'), { target: { value: '5' } })
  fireEvent.change(screen.getByLabelText('วันที่'), { target: { value: '2026-04-15' } })
  fireEvent.change(screen.getByLabelText('เวลาเริ่ม'), { target: { value: '13:00' } })
  fireEvent.change(screen.getByLabelText('เวลาสิ้นสุด'), { target: { value: '16:00' } })
  fireEvent.change(screen.getByLabelText('ลิงก์ URL สำหรับลงทะเบียน'), { target: { value: 'https://example.com/community' } })

  fireEvent.click(screen.getByRole('button', { name: 'ตรวจสอบก่อนบันทึก' }))
  fireEvent.click(screen.getByRole('button', { name: 'ยืนยันสร้างกิจกรรม' }))

  expect(handleCreate).toHaveBeenCalledTimes(1)
  expect(handleCreate.mock.calls[0][0]).toMatchObject({
    title: 'กิจกรรมบำเพ็ญประโยชน์',
    category: 'บำเพ็ญประโยชน์',
    registrationUrl: 'https://example.com/community',
  })
})
