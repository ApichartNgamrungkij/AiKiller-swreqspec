export interface RegisteredStudent {
  rowId: number | string;
  timestamp: string;
  studentId: string;
  fullName: string;
  faculty?: string | null;
  email?: string | null;
}

export type SyncStatus = "SUCCESS" | "FAILED";

export interface ActivityRegistrationSummary {
  activityId: number | string;
  totalRegistered: number;
  lastSyncedAt: string | null;
  syncStatus: SyncStatus;
  cachedResponses: RegisteredStudent[];
}
