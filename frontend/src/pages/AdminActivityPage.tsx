import { render, screen } from '@testing-library/react'
import { describe, expect, test, vi } from 'vitest'

import ActivityActionMenu from '../components/ActivityActionMenu'

// Supports FR-DEL-01, FR-DEL-02, IF-ADMIN-01, CON-DEL-01
export default function AdminActivityPage({ activities = [] }) {
  const publishedActivities = activities.filter((activity) => activity.status === 'published')

  return (
    <main>
      <h1>กิจกรรมที่เผยแพร่แล้ว</h1>
      {publishedActivities.length === 0 ? (
        <p>ไม่มีกิจกรรมที่เปิดเผย</p>
      ) : (
        <ul>
          {publishedActivities.map((activity) => (
            <li key={activity.id}>
              <strong>{activity.title}</strong>
              <ActivityActionMenu activity={activity} onSelect={() => {}} />
            </li>
          ))}
        </ul>
      )}

      {activities
        .filter((activity) => activity.status !== 'published')
        .map((activity) => (
          <p key={activity.id}>กิจกรรม {activity.title} ถูกซ่อนอยู่และไม่แสดงให้ Admin เลือกทำงาน</p>
        ))}
    </main>
  )
}

describe('AC-DEL-01', () => {
  test('Given มีกิจกรรมที่เผยแพร่อยู่ในระบบ และผู้ใช้งานเป็น Admin, When Admin เปิดรายการกิจกรรม, Then ระบบต้องให้ Admin เลือกกิจกรรมที่ต้องการลบหรือระงับได้', () => {
    const onSelect = vi.fn()
    const activities = [
      { id: 1, title: 'กิจกรรม A', status: 'published' },
      { id: 2, title: 'กิจกรรม B', status: 'hidden' },
      { id: 3, title: 'กิจกรรม C', status: 'published' },
    ]

    const { container } = render(<AdminActivityPage activities={activities} />)

    expect(screen.getByText('กิจกรรมที่เผยแพร่แล้ว')).toBeTruthy()
    expect(screen.getAllByRole('button', { name: 'ลบ' }).length).toBeGreaterThan(0)
    expect(screen.getAllByRole('button', { name: 'ระงับ' }).length).toBeGreaterThan(0)
    expect(screen.queryByText(/กิจกรรม B ถูกซ่อนอยู่/i)).toBeTruthy()
    expect(container.querySelectorAll('button').length).toBe(4)

    const { container: hiddenContainer } = render(
      <ActivityActionMenu activity={activities[1]} onSelect={onSelect} />,
    )
    expect(hiddenContainer.querySelectorAll('button').length).toBe(0)
  })
})
