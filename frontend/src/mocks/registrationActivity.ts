import { mockActivities, type MockActivity } from './activities'

export type RegistrationActivity = MockActivity & {
  googleSheetId: string
}

// Supports FR-REG-01, FR-REG-02, and IF-GFORM-01.
export const registrationActivity: RegistrationActivity = {
  ...mockActivities[0],
  googleSheetId: 'mock-sheet-community-service',
}
