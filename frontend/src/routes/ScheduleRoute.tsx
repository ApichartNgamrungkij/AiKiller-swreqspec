import React from 'react'

export type ScheduleUser = {
  is_authenticated?: boolean
  logged_in?: boolean
  role?: string
  student_id?: string | number
  id?: string | number
}

// Supports CON-SCHED-01, FR-SCHED-01
export function isAuthenticatedStudent(user?: ScheduleUser | null): boolean {
  if (!user) return false

  if (typeof user.is_authenticated === 'boolean') return user.is_authenticated
  if (typeof user.logged_in === 'boolean') return user.logged_in

  const role = String(user.role ?? '').trim().toLowerCase()
  if (role === 'student') return true

  return user.student_id != null || user.id != null
}

// Supports CON-SCHED-01, FR-SCHED-01
export default function ScheduleRoute({
  user,
  children,
}: {
  user?: ScheduleUser | null
  children?: React.ReactNode
}) {
  if (!isAuthenticatedStudent(user)) {
    return (
      <main>
        <h1>ตารางของฉัน</h1>
        <p>กรุณาเข้าสู่ระบบก่อนใช้งานฟีเจอร์ตารางของฉัน</p>
      </main>
    )
  }

  return <>{children ?? <main><h1>ตารางของฉัน</h1><p>เพิ่มช่วงเวลาที่ไม่ว่าง</p></main>}</>
}
