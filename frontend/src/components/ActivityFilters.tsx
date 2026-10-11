import { ACTIVITY_CATEGORIES, type ActivityCategory, type ActivityFilter } from '../services/activityFilter'

export type ActivityFiltersProps = {
  value: ActivityFilter
  onChange: (next: ActivityFilter) => void
}

// Supports FR-SRCH-02 and DOM — exposes only the five university-approved activity categories.
export default function ActivityFilters({ value, onChange }: ActivityFiltersProps) {
  return (
    <fieldset aria-label="ตัวกรองกิจกรรม">
      <legend>ตัวกรองกิจกรรม</legend>
      <label htmlFor="activity-category-filter">ประเภทกิจกรรม</label>
      <select
        id="activity-category-filter"
        value={value.category ?? ''}
        onChange={(event) => {
          const category = event.target.value
          onChange({
            ...value,
            category: category === '' ? undefined : (category as ActivityCategory),
          })
        }}
      >
        <option value="">ทุกประเภท</option>
        {ACTIVITY_CATEGORIES.map((category) => (
          <option key={category} value={category}>
            {category}
          </option>
        ))}
      </select>

      <label>
        <input
          type="checkbox"
          checked={value.availableOnly === true}
          onChange={(event) => onChange({ ...value, availableOnly: event.target.checked })}
        />
        แสดงเฉพาะกิจกรรมในช่วงเวลาว่าง
      </label>
    </fieldset>
  )
}
