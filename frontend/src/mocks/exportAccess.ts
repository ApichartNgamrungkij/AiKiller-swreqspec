export type ExportAccessMock = {
  activityId: number
  canExport: boolean
  hasAccess: boolean
  responseCount: number
  googleSheetUrl: string | null
}

// Supports FR-EXP-01, CON-EXPORT-01, ACC-GSHEET-01, ACC-GSHEET-02.
export const exportAccessMock: ExportAccessMock = {
  activityId: 1,
  canExport: true,
  hasAccess: true,
  responseCount: 12,
  googleSheetUrl: 'https://docs.google.com/spreadsheets/d/mock-sheet-community-service/edit',
}
