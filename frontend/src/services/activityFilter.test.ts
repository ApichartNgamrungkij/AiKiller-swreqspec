import { filterActivities } from './activityFilter'
import { mockActivities } from '../mocks/activities'
import { mockStudentSchedule } from '../mocks/studentSchedule'

// Supports AC-SRCH-02
test('test_AC_SRCH_02_filter_by_category', () => {
  const results = filterActivities(
    mockActivities,
    { category: 'วิชาการ' },
    mockStudentSchedule,
  )

  expect(results).toHaveLength(1)
  expect(results[0].category).toBe('วิชาการ')
})

// Supports AC-SRCH-02
test('test_AC_SRCH_02_filter_by_student_availability', () => {
  const results = filterActivities(
    mockActivities,
    { availableOnly: true },
    mockStudentSchedule,
  )

  expect(results.map((activity) => activity.id)).toEqual([1])
})
