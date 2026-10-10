import React from 'react'

export type CreateActivityUser = {
  role?: string
  is_organizer?: boolean
  can_create_activity?: boolean
  approved_by_admin?: boolean
  is_admin?: boolean
}

// Supports CON-ACT-01, FR-ACT-01, DOM-ACT-03
export function isAuthorizedActivityCreator(user?: CreateActivityUser | null): boolean {
  if (!user) return false

  const role = String(user.role ?? '').trim().toLowerCase()
  if (['admin', 'administrator', 'organizer', 'activity_manager'].includes(role)) {
    return true
  }

  if (typeof user.is_organizer === 'boolean') return user.is_organizer
  if (typeof user.can_create_activity === 'boolean') return user.can_create_activity
  if (typeof user.approved_by_admin === 'boolean') return user.approved_by_admin
  if (typeof user.is_admin === 'boolean') return user.is_admin

  return false
}

// Supports CON-ACT-01, FR-ACT-01, DOM-ACT-03
export default function CreateActivityRoute({
  user,
  children,
}: {
  user?: CreateActivityUser | null
  children?: React.ReactNode
}) {
  if (!isAuthorizedActivityCreator(user)) {
    return (
      <main>
        <h1>สร้างกิจกรรมใหม่</h1>
        <p>เฉพาะผู้จัดกิจกรรมที่ได้รับสิทธิ์จาก Admin เท่านั้นที่สามารถเข้าถึงหน้า “สร้างกิจกรรมใหม่” ได้</p>
      </main>
    )
  }

  return <>{children ?? <main><h1>สร้างกิจกรรมใหม่</h1><p>เริ่มกรอกข้อมูลกิจกรรม</p></main>}</>
}
