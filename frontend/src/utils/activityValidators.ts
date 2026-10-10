export const APPROVED_ACTIVITY_CATEGORIES = [
  'วิชาการ',
  'กีฬา',
  'ศิลปวัฒนธรรม',
  'คุณธรรมจริยธรรม',
  'บำเพ็ญประโยชน์',
] as const

const NEW_APPROVAL_KEYS = new Set([
  'approval_required',
  'approval_status',
  'approval_step',
  'new_approval_step',
  'needs_approval',
])

// Supports DOM-ACT-01, FR-ACT-04, FR-ACT-07, DOM-ACT-02, DOM-ACT-03
export function normalizeActivityCategory(value: unknown): string {
  const category = String(value ?? '').trim()

  if (!category) {
    throw new Error('category is required')
  }

  if (!APPROVED_ACTIVITY_CATEGORIES.includes(category as typeof APPROVED_ACTIVITY_CATEGORIES[number])) {
    throw new Error(`Unsupported activity category: ${String(value)}`)
  }

  return category
}

// Supports FR-ACT-04, FR-ACT-07, DOM-ACT-02, DOM-ACT-03
export function hasNewApprovalStep(payload: Record<string, unknown> | undefined): boolean {
  if (!payload) return false

  return Object.keys(payload).some((key) => {
    const normalized = key.trim().toLowerCase()
    return NEW_APPROVAL_KEYS.has(normalized) || normalized.startsWith('approval')
  })
}

// Supports FR-ACT-04, IF-ACT-01, DOM-ACT-01
export function validateActivitySubmission(payload: Record<string, unknown> | undefined): string[] {
  if (!payload) {
    return ['กรุณากรอกข้อมูลที่จำเป็น']
  }

  const errors: string[] = []

  if (hasNewApprovalStep(payload)) {
    errors.push('ระบบไม่เพิ่มขั้นตอนอนุมัติใหม่เข้ามาใน workflow')
  }

  for (const field of ['title', 'category', 'venue', 'max_participants', 'volunteer_hours']) {
    const rawValue = payload[field]
    if (rawValue === undefined || rawValue === null || String(rawValue).trim() === '') {
      errors.push(`กรุณากรอกข้อมูล ${field}`)
    }
  }

  if (payload.category !== undefined && payload.category !== null && String(payload.category).trim() !== '') {
    try {
      normalizeActivityCategory(payload.category)
    } catch (error) {
      errors.push((error as Error).message)
    }
  }

  const registrationUrl = payload.registration_url
  if (registrationUrl !== undefined && registrationUrl !== null && String(registrationUrl).trim() !== '') {
    try {
      const parsed = new URL(String(registrationUrl))
      if (!parsed.protocol || !parsed.hostname) {
        errors.push('registration_url must be a valid URL')
      }
    } catch {
      errors.push('registration_url must be a valid URL')
    }
  }

  const slots = payload.slots
  if (slots !== undefined) {
    if (!Array.isArray(slots) || slots.length === 0) {
      errors.push('กรุณาเพิ่มรอบเวลาอย่างน้อย 1 รอบ')
    } else {
      slots.forEach((slot, index) => {
        if (!slot || typeof slot !== 'object') {
          errors.push(`slot_${index + 1} must be an object`)
          return
        }

        const normalizedSlot = slot as Record<string, unknown>
        for (const field of ['slot_date', 'start_time', 'end_time']) {
          if (normalizedSlot[field] === undefined || normalizedSlot[field] === null || String(normalizedSlot[field]).trim() === '') {
            errors.push(`slot_${index + 1} ต้องมีข้อมูล ${field}`)
          }
        }
      })
    }
  }

  return errors
}

export function isValidActivitySubmission(payload: Record<string, unknown> | undefined): boolean {
  return validateActivitySubmission(payload).length === 0
}
