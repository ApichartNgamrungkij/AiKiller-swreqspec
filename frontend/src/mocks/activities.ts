export type MockActivity = {
  id: number
  title: string
  category: string
  status: 'open' | 'full'
  startAt: string
  endAt: string
  hoursAwarded: number
  location: string
  availableSlots: number
  bookedSlots: number
  googleFormUrl: string
}

// Supports FR-SRCH-01 and FR-SRCH-03
export const mockActivities: MockActivity[] = [
  {
    id: 1,
    title: 'ค่ายอาสาพัฒนาชุมชน',
    category: 'บำเพ็ญประโยชน์',
    status: 'open',
    startAt: '2026-11-07T09:00:00+07:00',
    endAt: '2026-11-07T16:00:00+07:00',
    hoursAwarded: 6,
    location: 'ศูนย์ชุมชนคลองสาม',
    availableSlots: 20,
    bookedSlots: 12,
    googleFormUrl: 'https://forms.google.com/community-service',
  },
  {
    id: 2,
    title: 'อบรมทักษะการนำเสนอ',
    category: 'วิชาการ',
    status: 'full',
    startAt: '2026-11-14T09:00:00+07:00',
    endAt: '2026-11-14T12:00:00+07:00',
    hoursAwarded: 3,
    location: 'ห้องประชุมอาคารเรียนรวม',
    availableSlots: 30,
    bookedSlots: 30,
    googleFormUrl: 'https://forms.google.com/presentation',
  },
]
