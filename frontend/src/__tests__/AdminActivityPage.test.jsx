import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, test, vi } from 'vitest'

import App from '../App'
import AdminActivityPage from '../pages/AdminActivityPage'

const activity = { id: 17, title: 'กิจกรรมทดสอบ', status: 'published' }

function openActionDialog(action) {
  render(
    <AdminActivityPage
      activities={[activity]}
      isAdmin
      onConfirmAction={vi.fn()}
    />,
  )

  fireEvent.click(screen.getByRole('button', { name: action === 'delete' ? 'ลบ' : 'ระงับ' }))
  return screen.getByRole('dialog')
}

describe('AC-DEL-01', () => {
  test('test_AC_DEL_01_admin_management_view_renders_activity_selection_page', () => {
    render(<App />)

    fireEvent.click(screen.getByRole('button', { name: /นักศึกษา/ }))
    fireEvent.click(screen.getByRole('button', { name: /Admin/ }))
    fireEvent.click(screen.getByRole('link', { name: 'จัดการกิจกรรมทั้งหมด' }))

    expect(screen.getByRole('heading', { name: 'กิจกรรมที่เผยแพร่แล้ว' })).toBeTruthy()
    expect(screen.getAllByRole('button', { name: 'ลบ' })).toHaveLength(3)
    expect(screen.getAllByRole('button', { name: 'ระงับ' })).toHaveLength(3)
  })

  test('test_AC_DEL_01_selecting_published_activity_opens_delete_dialog_with_context', () => {
    openActionDialog('delete')

    expect(screen.getByRole('heading', { name: 'ยืนยันการลบกิจกรรม' })).toBeTruthy()
    expect(screen.getByText(`กิจกรรม: ${activity.title}`)).toBeTruthy()
  })

  test('test_AC_DEL_01_selecting_published_activity_opens_suspend_dialog_with_context', () => {
    openActionDialog('suspend')

    expect(screen.getByRole('heading', { name: 'ยืนยันการระงับกิจกรรม' })).toBeTruthy()
    expect(screen.getByText(`กิจกรรม: ${activity.title}`)).toBeTruthy()
  })
})

describe('AC-DEL-03', () => {
  test.each(['', '   \n  '])('test_AC_DEL_03_empty_or_whitespace_reason_does_not_confirm', (reason) => {
    const onConfirmAction = vi.fn()
    render(
      <AdminActivityPage
        activities={[activity]}
        isAdmin
        onConfirmAction={onConfirmAction}
      />,
    )

    fireEvent.click(screen.getByRole('button', { name: 'ลบ' }))
    fireEvent.change(screen.getByLabelText('เหตุผล'), { target: { value: reason } })
    fireEvent.click(screen.getByRole('button', { name: 'ยืนยัน' }))

    expect(screen.getByRole('alert').textContent).toMatch(/ระบุเหตุผล/)
    expect(onConfirmAction).not.toHaveBeenCalled()
    expect(screen.getByRole('dialog')).toBeTruthy()
  })
})

describe('AC-DEL-02', () => {
  test('test_AC_DEL_02_cancel_closes_dialog_without_confirming', () => {
    const onConfirmAction = vi.fn()
    render(
      <AdminActivityPage
        activities={[activity]}
        isAdmin
        onConfirmAction={onConfirmAction}
      />,
    )

    fireEvent.click(screen.getByRole('button', { name: 'ระงับ' }))
    fireEvent.click(screen.getByRole('button', { name: 'ยกเลิก' }))

    expect(screen.queryByRole('dialog')).toBeNull()
    expect(onConfirmAction).not.toHaveBeenCalled()
  })

  test('test_AC_DEL_02_confirm_delete_sends_activity_action_and_trimmed_reason', () => {
    const onConfirmAction = vi.fn()
    render(
      <AdminActivityPage
        activities={[activity]}
        isAdmin
        onConfirmAction={onConfirmAction}
      />,
    )

    fireEvent.click(screen.getByRole('button', { name: 'ลบ' }))
    fireEvent.change(screen.getByLabelText('เหตุผล'), {
      target: { value: '  เนื้อหาไม่เหมาะสม  ' },
    })
    fireEvent.click(screen.getByRole('button', { name: 'ยืนยัน' }))

    expect(onConfirmAction).toHaveBeenCalledWith({
      activity,
      action: 'delete',
      reason: 'เนื้อหาไม่เหมาะสม',
    })
    expect(screen.queryByRole('dialog')).toBeNull()
  })

  test('test_AC_DEL_02_confirm_suspend_sends_activity_action_and_trimmed_reason', () => {
    const onConfirmAction = vi.fn()
    render(
      <AdminActivityPage
        activities={[activity]}
        isAdmin
        onConfirmAction={onConfirmAction}
      />,
    )

    fireEvent.click(screen.getByRole('button', { name: 'ระงับ' }))
    fireEvent.change(screen.getByLabelText('เหตุผล'), {
      target: { value: '  ตรวจสอบเพิ่มเติม  ' },
    })
    fireEvent.click(screen.getByRole('button', { name: 'ยืนยัน' }))

    expect(onConfirmAction).toHaveBeenCalledWith({
      activity,
      action: 'suspend',
      reason: 'ตรวจสอบเพิ่มเติม',
    })
    expect(screen.queryByRole('dialog')).toBeNull()
  })
})
