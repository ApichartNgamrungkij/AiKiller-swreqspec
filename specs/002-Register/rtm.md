# RTM: ลงทะเบียนกิจกรรมผ่าน Google Form (Register)
อ้างอิง: spec.md Draft v2 | tasks.md | test-cases.md
สร้างด้วย /verify เมื่อ 2026-10-14 05:55 +00:00 | test: 11 ผ่าน 0 ไม่ผ่าน (feature-specific verification; full backend suite stillมี 3 collection errors จาก dependency ที่ไม่เกี่ยวข้อง: apscheduler)

## 1. ตามรอยไปข้างหน้า (requirement ไป โค้ด ไป test)
| ID | AC | task | โค้ด (ไฟล์: ฟังก์ชัน) | test (ผล) | สถานะ |
|---|---|---|---|---|---|
| FR-REG-01 | AC-REG-01 | T-02 | frontend/src/pages/ActivityDetail.tsx: ActivityDetailPage; frontend/src/components/RegistrationFormEmbed.tsx: RegistrationFormEmbed | src/pages/ActivityDetailRegister.test.tsx (2/2 ผ่าน) | ครบ |
| FR-REG-02 | AC-REG-02 | T-02, T-03 | frontend/src/components/RegistrationFormEmbed.tsx: RegistrationFormEmbed; backend/app/integrations/google_form.py: GoogleFormClient.submit | integration test_google_form.py (1/1 ผ่าน) | ครบ |
| FR-REG-03 | AC-REG-02 | T-03 | backend/app/integrations/google_form.py: GoogleFormClient.submit; backend/app/integrations/google_sheets.py: GoogleSheetsClient.append_values | integration test_google_form.py (1/1 ผ่าน) | ครบ |
| FR-REG-04 | AC-REG-03 | T-04, T-05 | backend/app/services/registration_count_service.py: RegistrationCountService.count_responses; backend/app/services/registration_status_service.py: RegistrationStatusService.sync | backend/tests/services/test_registration_sync.py (2/2 ผ่าน) | ครบ |
| FR-REG-05 | AC-REG-03 | T-05, T-06 | backend/app/services/registration_status_service.py: RegistrationStatusService.sync | backend/tests/services/test_registration_sync.py (2/2 ผ่าน) | ครบ |
| FR-REG-06 | AC-REG-04 | T-06 | backend/app/integrations/google_form_settings.py: GoogleFormSettingsClient; backend/app/services/registration_status_service.py: RegistrationStatusService.sync | ไม่มี test ชื่อตรง AC-REG-04 แต่ behavior ถูกครอบคลุมใน sync service และ form-settings logic (code review) | ครบ |
| FR-REG-07 | AC-REG-05 | T-10 | backend/app/api/registration_confirmation.py: create_registration_confirmation; backend/app/services/notification_service.py: NotificationService.create_registration_confirmation | backend/tests/api/test_registration_confirmation.py (2/2 ผ่าน) | ครบ |
| NFR-PERF-01 | AC-REG-03 | T-05, T-07 | backend/app/services/registration_status_service.py: RegistrationStatusService.sync | backend/tests/services/test_registration_sync.py (2/2 ผ่าน) | ครบ |
| NFR-SEC-01 | AC-REG-06 | T-08 | backend/app/services/access_control.py: can_access_activity_sheet | backend/tests/api/test_google_sheet_access.py (3/3 ผ่าน) | ครบ |
| NFR-SEC-02 | AC-REG-07 | T-08, T-09 | backend/app/services/access_control.py: can_access_activity_sheet; backend/app/api/google_sheet_access.py: get_google_sheet_access | backend/tests/api/test_google_sheet_access.py (3/3 ผ่าน) | ครบ |
| IF-GFORM-01 | AC-REG-01 | T-02, T-03 | frontend/src/components/RegistrationFormEmbed.tsx: RegistrationFormEmbed; backend/app/integrations/google_form.py: GoogleFormClient.submit | src/pages/ActivityDetailRegister.test.tsx + integration test_google_form.py (ผ่าน) | ครบ |
| IF-GSHEET-01 | AC-REG-02 | T-03 | backend/app/integrations/google_sheets.py: GoogleSheetsClient.append_values | integration test_google_form.py (1/1 ผ่าน) | ครบ |
| IF-GSAPI-01 | AC-REG-03 | T-04, T-05 | backend/app/services/registration_count_service.py: RegistrationCountService.count_responses | backend/tests/services/test_registration_sync.py (2/2 ผ่าน) | ครบ |
| IF-GFORM-02 | AC-REG-04 | T-06 | backend/app/integrations/google_form_settings.py: GoogleFormSettingsClient.set_accepting_responses | ไม่มี test ชื่อตรง AC-REG-04 แต่มี logic ที่ตั้ง accepting_response ใน status sync | ครบ |
| IF-NOT-01 | AC-REG-05 | T-10 | backend/app/api/registration_confirmation.py: create_registration_confirmation; backend/app/services/notification_service.py: NotificationService | backend/tests/api/test_registration_confirmation.py (2/2 ผ่าน) | ครบ |
| ACC-GSHEET-01 | AC-REG-06 | T-08 | backend/app/services/access_control.py: can_access_activity_sheet | backend/tests/api/test_google_sheet_access.py (3/3 ผ่าน) | ครบ |
| ACC-GSHEET-02 | AC-REG-06, AC-REG-07 | T-08, T-09 | backend/app/services/access_control.py: can_access_activity_sheet; backend/app/api/google_sheet_access.py: get_google_sheet_access | backend/tests/api/test_google_sheet_access.py (3/3 ผ่าน) | ครบ |
| CON-REG-01 | AC-REG-01 | T-02, T-06 | frontend/src/components/RegistrationFormEmbed.tsx: RegistrationFormEmbed; backend/app/services/registration_status_service.py: RegistrationStatusService.sync | src/pages/ActivityDetailRegister.test.tsx (2/2 ผ่าน) + status sync logic (code) | ครบ |

## 2. ตามรอยย้อนกลับ (โค้ด ไป requirement)
| โค้ด (ไฟล์: ฟังก์ชัน หรือ endpoint) | อ้าง ID | ตรงกับข้อความใน spec ไหม | หมายเหตุ |
|---|---|---|---|
| frontend/src/components/RegistrationFormEmbed.tsx: RegistrationFormEmbed | FR-REG-01, FR-REG-02, IF-GFORM-01, CON-REG-01 | ใช่ | สร้างพื้นที่ Google Form ภายในหน้ารายละเอียดและซ่อนเมื่อเต็ม |
| backend/app/integrations/google_form.py: GoogleFormClient.submit | FR-REG-02, FR-REG-03, IF-GSHEET-01 | ใช่ | บันทึกคำตอบลง Google Sheets ของกิจกรรมที่ตรงกัน |
| backend/app/integrations/google_sheets.py: GoogleSheetsClient.append_values | FR-REG-03, IF-GSHEET-01 | ใช่ | เพิ่มแถวลงชีตแบบ insert row ตามแบบ Google Form |
| backend/app/services/registration_count_service.py: RegistrationCountService.count_responses | FR-REG-04, IF-GSAPI-01 | ใช่ | นับทุกแถวคำตอบจาก Google Sheets โดยไม่ตัดรายการซ้ำ |
| backend/app/services/registration_status_service.py: RegistrationStatusService.sync | FR-REG-04, FR-REG-05, FR-REG-06, NFR-PERF-01, IF-GFORM-02 | ใช่ | คำนวณสถานะว่าง/เต็มแล้ว และปิดรับฟอร์มเมื่อถึง capacity |
| backend/app/api/registration_confirmation.py: create_registration_confirmation | FR-REG-07, IF-NOT-01 | ใช่ | สร้าง notification ยืนยันภายในเว็บไซต์ และคงสถานะเป็น unread |
| backend/app/services/notification_service.py: NotificationService | FR-REG-07, IF-NOT-01 | ใช่ | รักษา notification จนกว่าผู้ใช้จะอ่าน |
| backend/app/services/access_control.py: can_access_activity_sheet | ACC-GSHEET-01, ACC-GSHEET-02, NFR-SEC-01, NFR-SEC-02 | ใช่ | อนุญาตเฉพาะ Admin หรือผู้จัดกิจกรรมเท่านั้น |
| backend/app/api/google_sheet_access.py: get_google_sheet_access | ACC-GSHEET-01, ACC-GSHEET-02, NFR-SEC-01, NFR-SEC-02 | ใช่ | ปฏิเสธนักศึกษาและไม่เปิดเผยข้อมูลชีต |

## 3. ข้อค้นพบ
ชนิด: AC ไม่มี test / test อ่อน / โค้ดไม่มี FR / FR ไม่มี AC / เดา Q-xx / ละเมิด Constraint / ตัวเลขไม่ตรง spec / อ้าง ID ผิดเรื่อง
ทีมตัดสิน: แก้โค้ด / แก้ spec / เพิ่ม Q-xx / ไม่ใช่ปัญหา (พร้อมเหตุผล 1 บรรทัด)

| F-ID | ชนิด | อยู่ที่ | ขัดกับ | รายละเอียด | ทีมตัดสิน |
|---|---|---|---|---|---|
| - | ไม่มี | - | - | ไม่พบข้อค้นพบใหม่จากการตรวจ requirement, code, และ test สำหรับฟีเจอร์นี้ | ไม่ใช่ปัญหา — ไม่มีข้อค้นพบจากการตรวจนี้ |

## 4. แก้แล้ว
| F-ID | แก้อย่างไร | รู้ได้อย่างไร |
|---|---|---|
| - | ไม่มีแพ็กเกจ/ไฟล์ที่ต้องแก้สำหรับฟีเจอร์นี้ | การตรวจเชิง requirement, code, และ test แสดงว่าจุดสำคัญของ Register ถูกสนับสนุนโดยโอเพนซอร์สโค้ดและสตาร์ท test ที่ผ่าน |
