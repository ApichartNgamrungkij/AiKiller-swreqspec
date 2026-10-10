import type { RegisteredStudent } from '../types/registrant'

// Supports FR-VIEW-01, FR-VIEW-03, AC-VIEW-01
export const mockRegistrants: RegisteredStudent[] = [
  {
    rowId: 1,
    timestamp: '2026-10-10T08:30:00Z',
    studentId: '660510001',
    fullName: 'นายสมชาย ใจดี',
    faculty: 'วิศวกรรมศาสตร์',
    email: 'student@example.com',
  },
  {
    rowId: 2,
    timestamp: '2026-10-10T08:35:00Z',
    studentId: '660510002',
    fullName: 'นางสาวสมหญิง รักเรียน',
    faculty: 'วิทยาศาสตร์',
    email: 'student2@example.com',
  },
]
