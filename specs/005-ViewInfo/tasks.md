# Tasks: ดูข้อมูลผู้ลงทะเบียนจาก Google Sheets (ViewInfo)

- Feature: ดูข้อมูลผู้ลงทะเบียนจาก Google Sheets (ViewInfo)
- Spec ID: `005-ViewInfo`
- อ้างอิง: [plan.md](./plan.md)
- วันที่: 2026-10-05

ฟีเจอร์นี้แบ่งเป็น 10 task ตามลำดับโมเดลข้อมูล, การตรวจสิทธิ์, การเชื่อมต่อ Google Sheets API, ระบบ Polling/Cache, API และหน้าจอ  
ไม่มี task ที่ต้องรอ Open Question โดยโครงสร้างคอลัมน์มาตรฐาน (รหัส, ชื่อ, คณะ) ถูกกำหนดในโมเดลแล้ว และ Pagination จะรองรับในขั้นพื้นฐาน

## รายการ task

### T-01 สร้างโมเดลข้อมูลผู้ลงทะเบียนและสรุปสถานะการ Sync
- รองรับ: FR-VIEW-01, FR-VIEW-02, FR-VIEW-03, FR-VIEW-04, CON-VIEW-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-02, T-03 และ T-05
- ไฟล์ที่แตะ: `backend/app/models/registrant.py`, `backend/app/models/registration_summary.py`, `frontend/src/types/registrant.ts`, `backend/tests/test_registrant_models.py`
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: โมเดลมี `rowId`, `timestamp`, `studentId`, `fullName`, `faculty`, `email` และข้อมูลสรุป `activityId`, `totalRegistered`, `lastSyncedAt`, `syncStatus`, `cachedResponses` ตาม plan.md ข้อ 3
- สถานะ: เสร็จ รอทีมตรวจ

### T-02 สร้างระบบตรวจสิทธิ์การเข้าถึงข้อมูลผู้ลงทะเบียน
- รองรับ: ACC-VIEW-01, ACC-VIEW-02, FR-VIEW-05, NFR-SEC-02
- ตรวจด้วย: AC-VIEW-04, AC-VIEW-05
- ไฟล์ที่แตะ: `backend/app/api/deps.py`, `backend/app/services/access_control.py`, `backend/app/models/activity.py`, `backend/tests/api/test_registrant_access.py`
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: ระบบมี Dependency ตรวจสอบว่าผู้ใช้มีบทบาท Admin หรือเป็นเจ้าของกิจกรรมนั้นเท่านั้น หากเป็นนักศึกษาทั่วไปหรือบุคคลอื่นให้ตอบกลับด้วย `403 Forbidden`
- สถานะ: เสร็จ รอทีมตรวจ

### T-03 สร้างตัวเชื่อมต่อและดึงข้อมูลผ่าน Google Sheets API v4
- รองรับ: IF-VIEW-01, FR-VIEW-02, ASM-VIEW-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-04 และ T-05
- ไฟล์ที่แตะ: `backend/app/integrations/google_sheets.py`, `backend/app/services/sheets_service.py`, `backend/tests/test_sheets_service.py`
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: Service สามารถเชื่อมต่อ Google Sheets ของกิจกรรมผ่าน Google Sheets API v4 ด้วย Service Account และอ่านรายชื่อผู้ลงทะเบียนแปลงเป็นโมเดล `RegisteredStudent` ได้ถูกต้อง
- สถานะ: เสร็จ รอทีมตรวจ

### T-04 พัฒนาระบบ Background Polling และ Fallback Cache
- รองรับ: IF-VIEW-01, IF-VIEW-02, FR-VIEW-03, FR-VIEW-04, NFR-PERF-01, ASM-VIEW-02
- ตรวจด้วย: AC-VIEW-02, AC-VIEW-03
- ไฟล์ที่แตะ: `backend/app/jobs/polling_worker.py`, `backend/app/services/cache_service.py`, `backend/tests/services/test_polling_cache.py`
- ต้องทำหลัง: T-01, T-03
- เสร็จเมื่อ: Background Worker ทำงาน Poll ข้อมูลทุก 1–2 นาที บันทึก snapshot ลง Cache และเมื่อ API ล้มเหลว ระบบจะดึงข้อมูลล่าสุดจาก Cache พร้อมสถานะ `FAILED` และวันเวลา `lastSyncedAt` โดยระบบไม่ Crash
- สถานะ: เสร็จ รอทีมตรวจ

### T-05 สร้าง API Endpoint ดึงข้อมูลและสรุปยอดผู้ลงทะเบียน
- รองรับ: FR-VIEW-01, FR-VIEW-02, FR-VIEW-03, FR-VIEW-04, FR-VIEW-05, NFR-SEC-02
- ตรวจด้วย: AC-VIEW-01, AC-VIEW-03, AC-VIEW-04, AC-VIEW-05
- ไฟล์ที่แตะ: `backend/app/api/registrants.py`, `backend/app/schemas/registrant.py`
- ต้องทำหลัง: T-01, T-02, T-03, T-04
- เสร็จเมื่อ: Endpoint `GET /api/v1/activities/{id}/registrants` คืน `activityId`, `totalRegistered`, `lastSyncedAt`, `syncStatus`, `isCache` และ `data` พร้อมตรวจสอบสิทธิ์ผ่าน T-02; กรณีไม่มีผู้ลงทะเบียนคืน `200 OK` และ `data: []`
- สถานะ: เสร็จ รอทีมตรวจ

### T-06 สร้างหน้ารายการผู้ลงทะเบียนด้วยข้อมูลจำลอง
- รองรับ: FR-VIEW-01, FR-VIEW-03
- ตรวจด้วย: AC-VIEW-01
- ไฟล์ที่แตะ: `frontend/src/pages/RegistrantsDetail.tsx`, `frontend/src/components/RegistrantTable.tsx`, `frontend/src/mocks/registrants.ts`
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: หน้ารายละเอียดแสดงตารางรายชื่อผู้ลงทะเบียน (รหัสนักศึกษา, ชื่อ-นามสกุล, เวลาที่ลงทะเบียน) และยอดรวมผู้สมัครด้วยข้อมูลจำลอง
- สถานะ: เสร็จ รอทีมตรวจ

### T-07 สร้าง Status Badge และการแจ้งเตือน Fallback Cache
- รองรับ: IF-VIEW-02, FR-VIEW-04
- ตรวจด้วย: AC-VIEW-03
- ไฟล์ที่แตะ: `frontend/src/components/SyncStatusBadge.tsx`, `frontend/src/components/CacheWarningAlert.tsx`
- ต้องทำหลัง: T-06
- เสร็จเมื่อ: หน้าจอแสดง Badge แจ้งเวลาอัปเดตล่าสุด และแสดงแถบเตือนสีเหลือง/ข้อความแจ้ง "แสดงข้อมูลล่าสุดเมื่อ [วัน/เวลา]" เมื่อข้อมูลถูกดึงมาจาก Cache
- สถานะ: เสร็จ รอทีมตรวจ

### T-08 จัดการเงื่อนไขผู้ลงทะเบียนอย่างน้อย 1 คนและหน้า Access Denied
- รองรับ: CON-VIEW-01, ACC-VIEW-01, ACC-VIEW-02, FR-VIEW-05
- ตรวจด้วย: AC-VIEW-04, AC-VIEW-05
- ไฟล์ที่แตะ: `frontend/src/pages/RegistrantsDetail.tsx`, `frontend/src/components/EmptyRegistrantState.tsx`, `frontend/src/components/AccessDenied.tsx`
- ต้องทำหลัง: T-06
- เสร็จเมื่อ: แสดง Empty State เมื่อยังไม่มีผู้ลงทะเบียน และแสดงหน้าข้อความปฏิเสธการเข้าถึง (Access Denied) ชัดเจนเมื่อนักศึกษาทั่วไปพยายามเข้าถึง
- สถานะ: เสร็จ รอทีมตรวจ

### T-09 ต่อหน้าจอกับ API จริงและตรวจสอบการอัปเดตแบบ Near Real-time
- รองรับ: FR-VIEW-01, FR-VIEW-02, FR-VIEW-03, NFR-PERF-01
- ตรวจด้วย: AC-VIEW-01, AC-VIEW-02
- ไฟล์ที่แตะ: `frontend/src/services/registrantApi.ts`, `frontend/src/pages/RegistrantsDetail.tsx`, `frontend/src/hooks/useRegistrants.ts`
- ต้องทำหลัง: T-02, T-05, T-06, T-07, T-08
- เสร็จเมื่อ: หน้าจอเชื่อมต่อกับ API จริง แสดงข้อมูลถูกต้อง และอัปเดตยอดผู้ลงทะเบียนใหม่ภายใน 2 นาทีเมื่อ Google Sheets มีข้อมูลเพิ่ม
- สถานะ: เสร็จ รอทีมตรวจ

### T-10 ตรวจสอบความปลอดภัย HTTPS และการควบคุมสิทธิ์เข้มงวด
- รองรับ: NFR-SEC-01, NFR-SEC-02
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานตรวจความปลอดภัยระบบ
- ไฟล์ที่แตะ: `deployment/https-config.yml`, `docs/integration/security-nfr.md`, `backend/tests/security/test_registrant_security.py`
- ต้องทำหลัง: T-02, T-05, T-09
- เสร็จเมื่อ: ยืนยันว่าการส่งข้อมูลทั้งหมดผ่าน HTTPS และมีการตรวจสอบ Authorization ทุก Request โดยไม่เปิดเผยข้อมูลส่วนบุคคลของผู้ลงทะเบียนแก่นักศึกษาทั่วไป
- สถานะ: เสร็จ รอทีมตรวจ

## ตารางตรวจความครบของ Acceptance Criteria

| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC-VIEW-01 | T-05, T-06, T-09 |
| AC-VIEW-02 | T-04, T-09 |
| AC-VIEW-03 | T-04, T-05, T-07 |
| AC-VIEW-04 | T-02, T-05, T-08 |
| AC-VIEW-05 | T-02, T-05, T-08 |

## ตารางตรวจความครบของ Constraints

| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| IF-VIEW-01 | T-03, T-04 |
| IF-VIEW-02 | T-04, T-05, T-07 |
| ACC-VIEW-01 | T-02, T-05, T-08 |
| ACC-VIEW-02 | T-02, T-05, T-08, T-10 |
| CON-VIEW-01 | T-01, T-05, T-08 |
| NFR-PERF-01 | T-04, T-09 |
| NFR-SEC-01 | T-10 |
| NFR-SEC-02 | T-02, T-05, T-10 |

## สิ่งที่ยังไม่ทำ

Q-VIEW-01 และ Q-VIEW-02 ได้รับคำตอบแล้วตามบันทึกใน spec.md โดยยังไม่เพิ่ม Pagination หรือการค้นหารายชื่อ

งานต่อไปนี้ยังไม่สร้างเพราะอยู่ใน Out of Scope:
- การลงทะเบียนกิจกรรมของนักศึกษา (อยู่ใน UC-03)
- การดาวน์โหลดหรือส่งออกไฟล์รายชื่อผู้ลงทะเบียนเป็น Excel/CSV (อยู่ใน UC-11 / 006-ExportList)
- การแก้ไข/ลบข้อมูลผู้ลงทะเบียนใน Google Sheets ผ่านหน้าเว็บไซต์
- การเช็คชื่อผู้เข้าร่วมกิจกรรมหน้างาน
- การนำรายชื่อเข้าสู่ระบบ REG ของมหาวิทยาลัย
