export type ExportAccessRole = "admin" | "organizer" | "student";

// Supports ACC-GSHEET-01, ACC-GSHEET-02, NFR-SEC-01, NFR-SEC-02.
export interface AccessRoleAssignment {
  userId: string;
  role: ExportAccessRole;
  activityId: number | string;
}

// Supports FR-EXP-01, FR-EXP-02, IF-GSHEET-01, CON-EXPORT-01.
export interface ActivityExportSource {
  activityId: number | string;
  googleSheetUrl: string;
  lastSuccessfulResponseCount: number;
  lastSuccessfulReadAt: string | null;
}
