# RTM: ดูข้อมูลผู้ลงทะเบียนจาก Google Sheets (ViewInfo)
อ้างอิง: [spec.md](./spec.md) Draft v2 | [tasks.md](./tasks.md) | [test-cases.md](./test-cases.md)
สร้างด้วย `/verify` เมื่อ 2026-10-14 05:08 | test: backend 79 ผ่าน (ชุดเต็ม collection ติด dependency), frontend 51 ผ่าน 1 ไม่ผ่าน

## 1. ตามรอยไปข้างหน้า (requirement ไป โค้ด ไป test)

| ID | AC | task | โค้ด (ไฟล์: ฟังก์ชัน) | test (ผล) | สถานะ |
|---|---|---|---|---|---|
| FR-VIEW-01 | AC-VIEW-01 | T-05, T-06, T-09 | `backend/app/api/registrants.py:get_registrants`, `frontend/src/pages/RegistrantsDetail.tsx:RegistrantsDetail` | `test_TC_VIEW_01_1_owner_sees_registrant_count_and_names` ผ่าน, `test_TC_VIEW_01_2_owner_sees_single_registrant` ผ่าน | ช่องโหว่ F-01 |
| FR-VIEW-02 | AC-VIEW-01, AC-VIEW-02 | T-03, T-05, T-09 | `backend/app/integrations/google_sheets.py`, `backend/app/services/sheets_service.py`, `frontend/src/services/registrantApi.ts:fetchRegistrants` | AC-VIEW-01 ผ่าน; AC-VIEW-02 frontend ผ่าน, backend test รันไม่ได้เพราะ F-03 | ช่องโหว่ F-03 |
| FR-VIEW-03 | AC-VIEW-01, AC-VIEW-02 | T-04, T-06, T-09 | `backend/app/jobs/polling_worker.py:RegistrationPollingWorker`, `frontend/src/hooks/useRegistrants.ts:useRegistrants` | `test_TC_VIEW_02_1_count_updates_after_new_registration` ผ่าน, `test_TC_VIEW_02_2_count_updates_at_two_minute_boundary` ผ่านฝั่ง frontend | ช่องโหว่ F-03 |
| FR-VIEW-04 | AC-VIEW-03 | T-04, T-05, T-07 | `backend/app/services/cache_service.py:RegistrationCache`, `frontend/src/components/CacheWarningAlert.tsx:CacheWarningAlert` | `test_TC_VIEW_03_1_cached_registrants_show_when_sheets_api_fails` ผ่านฝั่ง frontend; backend AC03 รันไม่ได้ | ช่องโหว่ F-02, F-03 |
| FR-VIEW-05 | AC-VIEW-04, AC-VIEW-05 | T-02, T-05, T-08 | `backend/app/api/deps.py:verify_event_owner_or_admin`, `frontend/src/components/AccessDenied.tsx:AccessDenied` | AC-VIEW-04/05 backend 10 ผ่าน และ frontend 6 ผ่าน | ช่องโหว่ F-01 |
| NFR-PERF-01 | AC-VIEW-02 | T-04, T-09 | `backend/app/jobs/polling_worker.py:RegistrationPollingWorker`, `frontend/src/hooks/useRegistrants.ts:REGISTRANT_POLL_INTERVAL_MS` | frontend ตรวจ 120,000 ms ผ่าน; backend polling test รันไม่ได้ | ช่องโหว่ F-03 |
| NFR-SEC-01 | ไม่มี AC | T-10 | `deployment/https-config.yml` | `test_NFR_SEC_01_https_deployment_contract_requires_tls` ผ่าน | ครบ |
| NFR-SEC-02 | AC-VIEW-04, AC-VIEW-05 | T-02, T-05, T-10 | `backend/app/api/deps.py:verify_event_owner_or_admin`, `backend/app/api/registrants.py:get_registrants` | authorization unit tests ผ่าน; endpoint จริงใช้ dependency placeholder | ช่องโหว่ F-01 |
| IF-VIEW-01 | AC-VIEW-01, AC-VIEW-02 | T-03, T-04 | `backend/app/integrations/google_sheets.py`, `backend/app/jobs/polling_worker.py:RegistrationPollingWorker` | polling tests รันไม่ได้เพราะ F-03 | ช่องโหว่ F-03 |
| IF-VIEW-02 | AC-VIEW-03 | T-04, T-05, T-07 | `backend/app/services/cache_service.py:RegistrationCache`, `frontend/src/components/CacheWarningAlert.tsx:CacheWarningAlert` | frontend cache warning ผ่าน; backend cache test รันไม่ได้ | ช่องโหว่ F-02, F-03 |
| ACC-VIEW-01 | AC-VIEW-04, AC-VIEW-05 | T-02, T-05, T-08 | `backend/app/services/access_control.py:is_activity_owner`, `is_admin_user` | access-control tests ผ่าน | ช่องโหว่ F-01 |
| ACC-VIEW-02 | AC-VIEW-04, AC-VIEW-05 | T-02, T-05, T-08, T-10 | `backend/app/api/deps.py:verify_event_owner_or_admin`, `frontend/src/components/AccessDenied.tsx:AccessDenied` | student/non-owner tests ผ่าน; endpoint wiring มี F-01 | ช่องโหว่ F-01 |
| CON-VIEW-01 | AC-VIEW-01 | T-01, T-05, T-08 | `backend/app/api/registrants.py:_empty_summary`, `frontend/src/components/EmptyRegistrantState.tsx:EmptyRegistrantState` | `test_TC_VIEW_01_3_owner_sees_empty_state_without_registrants` ผ่าน | ครบ |

## 2. ตามรอยย้อนกลับ (โค้ด ไป requirement)

| โค้ด (ไฟล์: ฟังก์ชัน หรือ endpoint) | อ้าง ID | ตรงกับข้อความใน spec ไหม | หมายเหตุ |
|---|---|---|---|
| `backend/app/api/registrants.py:GET /api/v1/activities/{activity_id}/registrants` | FR-VIEW-01 ถึง FR-VIEW-05, NFR-SEC-02 | ไม่ตรงทั้งหมด | endpoint มี response และ authorization logic แต่ `get_current_user` และ `get_activity` ยังตอบ `501 NOT_IMPLEMENTED` จึงยังใช้งานจริงไม่ได้ (F-01) |
| `backend/app/jobs/polling_worker.py:RegistrationPollingWorker.poll_activity` | IF-VIEW-01, IF-VIEW-02, FR-VIEW-03, FR-VIEW-04, NFR-PERF-01 | ตรงบางส่วน | รองรับช่วง 60–120 วินาทีและ fallback cache แต่ยังไม่มีหลักฐานรัน test เพราะ dependency หาย (F-03) |
| `backend/app/services/cache_service.py:RegistrationCache.get_failed` | IF-VIEW-02, FR-VIEW-04 | ตรง | คืน snapshot เดิมพร้อมสถานะ `FAILED`; ต้องเชื่อมกับ API/หน้าจอจริงให้ครบ (F-02) |
| `frontend/src/hooks/useRegistrants.ts:useRegistrants` | FR-VIEW-02, FR-VIEW-03, NFR-PERF-01 | ตรงบางส่วน | polling 120 วินาทีและ refresh API มี test แต่หน้า detail ยังไม่แสดงสถานะ/cache จาก summary (F-02) |
| `frontend/src/pages/RegistrantsDetail.tsx:RegistrantsDetail` | FR-VIEW-01, FR-VIEW-03, FR-VIEW-04 | ไม่ตรงทั้งหมด | ใช้จำนวนจากความยาว array และไม่ render `SyncStatusBadge`/`CacheWarningAlert` เมื่อใช้ API จึงไม่แสดงเวลาหรือคำเตือนตาม FR-VIEW-04 (F-02) |
| `backend/app/api/deps.py:verify_event_owner_or_admin` | ACC-VIEW-01, ACC-VIEW-02, FR-VIEW-05 | ตรงใน unit | ตรวจ role/owner ได้ แต่การเรียก endpoint จริงยังติด dependency placeholder (F-01) |
| `frontend/src/components/AccessDenied.tsx:AccessDenied` | ACC-VIEW-02, AC-VIEW-04 | ตรง | แสดง Access Denied และข้อความไม่มีสิทธิ์ตาม AC |

## 3. ข้อค้นพบ

ชนิด: AC ไม่มี test / test อ่อน / โค้ดไม่มี FR / FR ไม่มี AC / เดา Q-xx / ละเมิด Constraint / ตัวเลขไม่ตรง spec / อ้าง ID ผิดเรื่อง  
ทีมตัดสิน: แก้โค้ด / แก้ spec / เพิ่ม Q-xx / ไม่ใช่ปัญหา (พร้อมเหตุผล 1 บรรทัด)

| F-ID | ชนิด | อยู่ที่ | ขัดกับ | รายละเอียด | ทีมตัดสิน |
|---|---|---|---|---|---|
| F-01 | โค้ดทำงานไม่ครบตาม FR / test integration ไม่ถึง | `backend/app/api/registrants.py:19-30,48-54` | FR-VIEW-01, FR-VIEW-05, NFR-SEC-02, ACC-VIEW-01 | dependency หลัก `get_current_user` และ `get_activity` ยังตอบ `501 NOT_IMPLEMENTED`; test ที่ผ่านใช้ dependency override จึงยังไม่ยืนยันว่า endpoint จริงเรียกใช้ authorization และ activity lookup ได้ | แก้โค้ด: เชื่อม authentication และ activity lookup จริงก่อนถือว่า endpoint พร้อมใช้งาน |
| F-02 | test อ่อน / โค้ดไม่ทำตาม FR | `frontend/src/pages/RegistrantsDetail.tsx:22-39` | FR-VIEW-04, IF-VIEW-02, AC-VIEW-03 | หน้า detail เรียก `useRegistrants` แต่ไม่ render `SyncStatusBadge` หรือ `CacheWarningAlert` และไม่ได้ใช้ `syncStatus`, `isCache`, `lastSyncedAt`; test component แยกจึงไม่ยืนยันพฤติกรรมทั้งหน้า | แก้โค้ด: แสดงสถานะ cache และเวลาซิงก์ล่าสุดบนหน้า detail |
| F-03 | environment blocker ทำให้ตรวจไม่ได้ | `backend/app/jobs/polling_worker.py:8`, `backend/tests/test_AC_VIEW_02.py`, `backend/tests/test_AC_VIEW_03.py` | IF-VIEW-01, IF-VIEW-02, NFR-PERF-01 | backend suite collection ไม่ได้เพราะ `googleapiclient` ไม่ติดตั้ง; `googleapiclient` ยังไม่อยู่ใน `backend/requirements.txt` จึงยังยืนยันผล backend ของ polling/cache ไม่ได้ | แก้โค้ด/สภาพแวดล้อม: เพิ่ม dependency ตามที่โค้ดใช้และรัน backend polling/cache ใหม่ |
| F-04 | test ไม่ผ่าน (นอกฟีเจอร์) | `frontend/src/__tests__/TC-DEL-01-1.test.jsx:58` | 007-DeleteActivity | frontend full suite มี 51 ผ่าน 1 ไม่ผ่าน เพราะ test เดิมของ DeleteActivity พบปุ่มลบ/ระงับของ non-admin; ไม่ใช่ข้อบกพร่องของ ViewInfo แต่ทำให้ full suite ไม่เขียว | ไม่ใช่ปัญหา: เป็นขอบเขตของ 007 ให้เจ้าของ 007 ดำเนินการแยก |
## 4. แก้แล้ว

| F-ID | แก้อย่างไร | รู้ได้อย่างไร |
|---|---|---|
| - | ยังไม่มีข้อค้นพบที่ทีมยืนยันว่าแก้แล้วในรอบนี้ | ทีมต้องกรอกช่อง “ทีมตัดสิน” และทำ verify รอบถัดไปหลังปิดข้อค้นพบ |
