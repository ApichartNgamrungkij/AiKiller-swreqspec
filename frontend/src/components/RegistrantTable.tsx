import type { RegisteredStudent } from '../types/registrant'

type RegistrantTableProps = {
  registrants: RegisteredStudent[]
}

// Supports FR-VIEW-01, FR-VIEW-03, AC-VIEW-01
export default function RegistrantTable({ registrants }: RegistrantTableProps) {
  return (
    <table>
      <caption className="sr-only">รายชื่อผู้ลงทะเบียน</caption>
      <thead>
        <tr>
          <th scope="col">รหัสนักศึกษา</th>
          <th scope="col">ชื่อ-นามสกุล</th>
          <th scope="col">เวลาที่ลงทะเบียน</th>
        </tr>
      </thead>
      <tbody>
        {registrants.map((registrant) => (
          <tr key={registrant.rowId}>
            <td>{registrant.studentId}</td>
            <td>{registrant.fullName}</td>
            <td>{new Date(registrant.timestamp).toLocaleString('th-TH')}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
