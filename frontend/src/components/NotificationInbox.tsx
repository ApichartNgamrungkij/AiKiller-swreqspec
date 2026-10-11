export type RegistrationNotification = {
  notificationId: number
  activityId: number
  message: string
  isRead: boolean
  createdAt: string
}

export type NotificationInboxProps = {
  notifications: RegistrationNotification[]
}

// Supports FR-REG-07, IF-NOT-01, ASM-05, ASM-10.
export default function NotificationInbox({ notifications }: NotificationInboxProps) {
  return (
    <section aria-label="การแจ้งเตือนภายในเว็บไซต์">
      <h2>การแจ้งเตือน</h2>
      {notifications.length === 0 ? (
        <p>ยังไม่มีการแจ้งเตือน</p>
      ) : (
        <ul>
          {notifications.map((notification) => (
            <li key={notification.notificationId}>
              <p>{notification.message}</p>
              {!notification.isRead && <span>ยังไม่ได้อ่าน</span>}
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}
