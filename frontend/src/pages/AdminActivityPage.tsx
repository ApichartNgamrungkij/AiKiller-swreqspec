import { useState } from 'react'
import ActivityActionMenu from '../components/ActivityActionMenu'
import ConfirmDeleteDialog from '../components/ConfirmDeleteDialog'

type ActivityAction = 'delete' | 'suspend'
type AdminActivity = {
  id: number | string
  title: string
  status: string
}
type SelectedAction = {
  activity: AdminActivity
  action: ActivityAction
}
type AdminActionRequest = SelectedAction & {
  reason: string
}

type AdminActivityPageProps = {
  activities?: AdminActivity[]
  isAdmin?: boolean
  onConfirmAction?: (request: AdminActionRequest) => void
  lastActionRequest?: AdminActionRequest | null
}

// Supports FR-DEL-01 through FR-DEL-04, IF-ADMIN-01, IF-REASON-01, CON-DEL-01
export default function AdminActivityPage({
  activities = [],
  isAdmin = false,
  onConfirmAction,
  lastActionRequest = null,
}: AdminActivityPageProps) {
  const [selectedAction, setSelectedAction] = useState<SelectedAction | null>(null)
  const publishedActivities = activities.filter((activity) => activity.status === 'published')

  const handleConfirm = (reason: string) => {
    if (!selectedAction) return
    if (!onConfirmAction) {
      throw new Error('AdminActivityPage requires an onConfirmAction callback')
    }

    onConfirmAction({ ...selectedAction, reason })
    setSelectedAction(null)
  }

  return (
    <main>
      <h1>กิจกรรมที่เผยแพร่แล้ว</h1>
      {lastActionRequest ? (
        <p role="status">
          รับข้อมูลยืนยัน{lastActionRequest.action === 'delete' ? 'ลบ' : 'ระงับ'}กิจกรรม
          “{lastActionRequest.activity.title}” ใน UI แล้ว แต่ยังไม่ได้เรียก Backend
          หรือเปลี่ยนแปลงข้อมูลจริง
        </p>
      ) : null}
      {publishedActivities.length === 0 ? (
        <p>ไม่มีกิจกรรมที่เปิดเผย</p>
      ) : (
        <ul>
          {publishedActivities.map((activity) => (
            <li key={activity.id}>
              <strong>{activity.title}</strong>
              <ActivityActionMenu
                activity={activity}
                isAdmin={isAdmin}
                onSelect={(action) => setSelectedAction({ activity, action })}
              />
            </li>
          ))}
        </ul>
      )}

      {activities
        .filter((activity) => activity.status !== 'published')
        .map((activity) => (
          <p key={activity.id}>กิจกรรม {activity.title} ถูกซ่อนอยู่และไม่แสดงให้ Admin เลือกทำงาน</p>
        ))}
      {selectedAction ? (
        <ConfirmDeleteDialog
          activityTitle={selectedAction.activity.title}
          actionType={selectedAction.action}
          onConfirm={handleConfirm}
          onCancel={() => setSelectedAction(null)}
        />
      ) : null}
    </main>
  )
}

if (import.meta.env.MODE === 'test') {
  const [{ render, screen }, { describe, expect, test, vi }] = await Promise.all([
    import('@testing-library/react'),
    import('vitest'),
  ])

describe('AC-DEL-01', () => {
  test('Given มีกิจกรรมที่เผยแพร่อยู่ในระบบ และผู้ใช้งานเป็น Admin, When Admin เปิดรายการกิจกรรม, Then ระบบต้องให้ Admin เลือกกิจกรรมที่ต้องการลบหรือระงับได้', () => {
    const onSelect = vi.fn()
    const activities = [
      { id: 1, title: 'กิจกรรม A', status: 'published' },
      { id: 2, title: 'กิจกรรม B', status: 'hidden' },
      { id: 3, title: 'กิจกรรม C', status: 'published' },
    ]

    const { container } = render(
  <AdminActivityPage activities={activities} isAdmin={true} />
)

    expect(screen.getByText('กิจกรรมที่เผยแพร่แล้ว')).toBeTruthy()
    expect(screen.getAllByRole('button', { name: 'ลบ' }).length).toBeGreaterThan(0)
    expect(screen.getAllByRole('button', { name: 'ระงับ' }).length).toBeGreaterThan(0)
    expect(screen.queryByText(/กิจกรรม B ถูกซ่อนอยู่/i)).toBeTruthy()
    expect(container.querySelectorAll('button').length).toBe(4)

    const { container: hiddenContainer } = render(
  <ActivityActionMenu
    activity={activities[1]}
    isAdmin={true}
    onSelect={onSelect}
  />,
)
    expect(hiddenContainer.querySelectorAll('button').length).toBe(0)
  })
})

// Given มีกิจกรรมที่เผยแพร่อยู่ในระบบอย่างน้อย 2 รายการ และผู้ใช้งานเป็น Admin ที่เข้าสู่ระบบแล้ว
// When Admin เปิดรายการกิจกรรม
// Then ระบบแสดงกิจกรรมที่เผยแพร่แล้วทั้งหมด และแต่ละรายการมีตัวเลือก/เมนูให้ Admin เลือก “ลบ” หรือ “ระงับ” ได้
test('test_TC_DEL_01_1_admin_can_select_delete_or_suspend_for_published_activities', () => {
  const activities = [
    { id: 1, title: 'กิจกรรม A', status: 'published' },
    { id: 2, title: 'กิจกรรม B', status: 'published' },
    { id: 3, title: 'กิจกรรม C', status: 'hidden' },
  ]

  const { container } = render(
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
}
