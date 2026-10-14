import { render, screen } from '@testing-library/react'

import AdminActivityPage from '../pages/AdminActivityPage'

// Given มีกิจกรรมที่เผยแพร่อยู่ในระบบอย่างน้อย 2 รายการ และผู้ใช้งานเป็น Admin ที่เข้าสู่ระบบแล้ว
// When Admin เปิดรายการกิจกรรม
// Then ระบบแสดงกิจกรรมที่เผยแพร่แล้วทั้งหมด และแต่ละรายการมีตัวเลือก/เมนูให้ Admin เลือก “ลบ” หรือ “ระงับ” ได้
test('test_TC_DEL_01_1_admin_can_select_delete_or_suspend_for_published_activities', () => {
  const activities = [
    { id: 1, title: 'กิจกรรม A', status: 'published' },
    { id: 2, title: 'กิจกรรม B', status: 'published' },
    { id: 3, title: 'กิจกรรม C', status: 'hidden' },
  ]

  render(
  <AdminActivityPage activities={activities} isAdmin={true} />
)

  expect(screen.getByText('กิจกรรมที่เผยแพร่แล้ว')).toBeTruthy()
  expect(screen.getByText('กิจกรรม A')).toBeTruthy()
  expect(screen.getByText('กิจกรรม B')).toBeTruthy()
  expect(screen.getAllByRole('button', { name: 'ลบ' })).toHaveLength(2)
  expect(screen.getAllByRole('button', { name: 'ระงับ' })).toHaveLength(2)
})

// Given มีเพียง 1 กิจกรรมที่เผยแพร่ และมีกิจกรรมอีก 1 รายการที่ถูกซ่อน/ถูกลบแล้วอยู่ในระบบ
// When Admin เปิดรายการกิจกรรม
// Then ระบบแสดงเฉพาะกิจกรรมที่เผยแพร่แล้วเท่านั้น และกิจกรรมที่ถูกซ่อนหรือถูกลบแล้วไม่ปรากฏในรายการที่ Admin สามารถเลือกเพื่อลบหรือระงับได้
test('test_TC_DEL_01_2_admin_only_sees_published_activities_for_selection', () => {
  const activities = [
    { id: 1, title: 'กิจกรรม A', status: 'published' },
    { id: 2, title: 'กิจกรรม B', status: 'hidden' },
  ]

const { container } = render(
  <AdminActivityPage activities={activities} isAdmin={true} />
)
  expect(screen.getByText('กิจกรรม A')).toBeTruthy()
  expect(screen.getAllByRole('button', { name: 'ลบ' })).toHaveLength(1)
  expect(screen.getAllByRole('button', { name: 'ระงับ' })).toHaveLength(1)
  expect(screen.getByText(/กิจกรรม B.*ถูกซ่อนอยู่และไม่แสดงให้ Admin เลือกทำงาน/i)).toBeTruthy()
  expect(container.querySelector('[aria-label="actions-2"]')).toBeNull()
})

// Given ผู้ใช้งานไม่มีสิทธิ์ Admin แต่มีกิจกรรมที่เผยแพร่อยู่ในระบบ
// When ผู้ใช้นั้นเปิดรายการกิจกรรม
// Then ระบบไม่ให้ผู้ใช้นั้นเลือกกิจกรรมเพื่อลบหรือระงับ และไม่แสดงเมนู “ลบ” หรือ “ระงับ” สำหรับกิจกรรมใด ๆ ในรายการ
test('test_TC_DEL_01_3_non_admin_cannot_access_delete_or_suspend_actions', () => {
  const activities = [
    { id: 1, title: 'กิจกรรม A', status: 'published' },
    { id: 2, title: 'กิจกรรม B', status: 'published' },
  ]

  render(
  <AdminActivityPage activities={activities} isAdmin={false} />
)

  expect(screen.queryByRole('button', { name: 'ลบ' })).toBeNull()
  expect(screen.queryByRole('button', { name: 'ระงับ' })).toBeNull()
})
