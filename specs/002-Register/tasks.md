# Tasks: ลงทะเบียนกิจกรรมผ่าน Google Form (Register)

- Feature: ลงทะเบียนกิจกรรมผ่าน Google Form (Register)
- Spec ID: `002-Register`
- อ้างอิง: [plan.md](./plan.md)
- วันที่: 2026-10-05

ฟีเจอร์นี้แบ่งเป็น 10 task ตามลำดับโมเดลข้อมูล, หน้ารายละเอียด, การเชื่อมต่อ Google และบริการประกอบ  
ไม่มี task ที่ต้องรอ Open Question เนื่องจาก spec ไม่มี Open Question ค้างอยู่

## รายการ task

### T-01 สร้างโมเดลกิจกรรมและ snapshot การลงทะเบียน
- รองรับ: FR-REG-01, FR-REG-04, FR-REG-05, FR-REG-06, CON-REG-01, NFR-PERF-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-02, T-04 และ T-05
- ไฟล์ที่แตะ: `backend/app/models/activity.py`, `backend/app/models/registration_count_snapshot.py`
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: โมเดลมี `activity_id`, `capacity`, `registration_status`, `google_form_url`, `google_sheet_id`, `response_count` และ `last_successful_sync_at` ตาม plan.md ข้อ 3
- สถานะ: พร้อมทำ

### T-02 สร้างหน้ารายละเอียดกิจกรรมด้วย Google Form จำลอง
- รองรับ: FR-REG-01, FR-REG-02, CON-REG-01, IF-GFORM-01
- ตรวจด้วย: AC-REG-01
- ไฟล์ที่แตะ: `frontend/src/pages/ActivityDetail.tsx`, `frontend/src/components/RegistrationFormEmbed.tsx`, `frontend/src/mocks/registrationActivity.ts`
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: นักศึกษาที่เข้าสู่ระบบและกิจกรรมยังไม่เต็มเห็นพื้นที่ Google Form จำลองฝังอยู่ในหน้ารายละเอียด
- สถานะ: พร้อมทำ

### T-03 เชื่อม Google Form กับ Google Sheets ของกิจกรรม
- รองรับ: FR-REG-02, FR-REG-03, IF-GFORM-01, IF-GSHEET-01, ASM-01, ASM-04
- ตรวจด้วย: AC-REG-02
- ไฟล์ที่แตะ: `backend/app/integrations/google_form.py`, `backend/app/integrations/google_sheets.py`, `frontend/src/services/registrationForm.ts`
- ต้องทำหลัง: T-01, T-02
- เสร็จเมื่อ: การจำลองการส่ง Google Form สำเร็จสร้างคำตอบใน Google Sheets ที่ผูกกับ `google_sheet_id` ของกิจกรรมนั้นโดยอัตโนมัติ
- สถานะ: พร้อมทำ

### T-04 สร้างตัวอ่านจำนวนผู้ตอบผ่าน Google Sheets API
- รองรับ: FR-REG-03, FR-REG-04, IF-GSAPI-01, ASM-02, ASM-12
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-05
- ไฟล์ที่แตะ: `backend/app/integrations/google_sheets_api.py`, `backend/app/services/registration_count_service.py`
- ต้องทำหลัง: T-01, T-03
- เสร็จเมื่อ: service อ่านและนับทุกแถวคำตอบจาก Google Sheets รวมรายการซ้ำโดยไม่ตัดออกได้
- สถานะ: พร้อมทำ

### T-05 คำนวณและอัปเดตสถานะกิจกรรม
- รองรับ: FR-REG-04, FR-REG-05, NFR-PERF-01, ASM-07, ASM-12
- ตรวจด้วย: AC-REG-03
- ไฟล์ที่แตะ: `backend/app/api/registration_sync.py`, `backend/app/services/registration_status_service.py`
- ต้องทำหลัง: T-01, T-04
- เสร็จเมื่อ: endpoint `POST /activities/{activityId}/registration-sync` อัปเดตจำนวนและสถานะ “ว่าง/เต็มแล้ว” จากทุกแถวภายใน 2 นาที
- สถานะ: พร้อมทำ

### T-06 ปิดรับ Google Form เมื่อกิจกรรมเต็ม
- รองรับ: FR-REG-05, FR-REG-06, IF-GFORM-02, CON-REG-01, ASM-03, ASM-06, ASM-09
- ตรวจด้วย: AC-REG-04
- ไฟล์ที่แตะ: `backend/app/integrations/google_form_settings.py`, `backend/app/services/registration_status_service.py`, `frontend/src/components/RegistrationFormEmbed.tsx`
- ต้องทำหลัง: T-03, T-05
- เสร็จเมื่อ: เมื่อจำนวนผู้ตอบถึง `capacity` ระบบสั่งปิดรับคำตอบตามการตั้งค่าของ Google Form อัปเดตสถานะเป็น “เต็มแล้ว” และไม่แสดงหรือไม่อนุญาตให้ใช้งานฟอร์ม
- สถานะ: พร้อมทำ

### T-07 คง snapshot เดิมเมื่อ Google Sheets API ล้มเหลว
- รองรับ: FR-REG-04, FR-REG-05, NFR-PERF-01, ASM-08
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-05 และ T-10
- ไฟล์ที่แตะ: `backend/app/services/registration_count_service.py`, `backend/app/services/registration_status_service.py`, `backend/tests/services/test_registration_sync.py`
- ต้องทำหลัง: T-01, T-04, T-05
- เสร็จเมื่อ: เมื่อ API ไม่ตอบสนอง ระบบคง `response_count`, สถานะล่าสุด และเวลา sync สำเร็จล่าสุดไว้โดยไม่เขียนค่าจำนวนใหม่
- สถานะ: พร้อมทำ

### T-08 ควบคุมสิทธิ์การเข้าถึง Google Sheets
- รองรับ: ACC-GSHEET-01, ACC-GSHEET-02, NFR-SEC-01, NFR-SEC-02, ASM-11
- ตรวจด้วย: AC-REG-06
- ไฟล์ที่แตะ: `backend/app/models/access_role.py`, `backend/app/api/google_sheet_access.py`, `backend/app/services/access_control.py`
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: endpoint `GET /activities/{activityId}/google-sheet-access` อนุญาตเฉพาะ Admin/ผู้จัดกิจกรรม และปฏิเสธนักศึกษา
- สถานะ: พร้อมทำ

### T-09 ปฏิเสธการเข้าถึง Google Sheets ของนักศึกษาโดยตรง
- รองรับ: ACC-GSHEET-02, NFR-SEC-02
- ตรวจด้วย: AC-REG-07
- ไฟล์ที่แตะ: `backend/app/api/google_sheet_access.py`, `backend/tests/api/test_google_sheet_access.py`
- ต้องทำหลัง: T-08
- เสร็จเมื่อ: คำขอจากนักศึกษาที่พยายามเข้าถึง Google Sheets ผ่านระบบได้รับการปฏิเสธและไม่เผยข้อมูลชีต
- สถานะ: พร้อมทำ

### T-10 สร้างและเก็บ Notification ยืนยันการลงทะเบียน
- รองรับ: FR-REG-07, IF-NOT-01, ASM-05, ASM-10
- ตรวจด้วย: AC-REG-05
- ไฟล์ที่แตะ: `backend/app/models/notification.py`, `backend/app/api/registration_confirmation.py`, `backend/app/services/notification_service.py`, `frontend/src/components/NotificationInbox.tsx`
- ต้องทำหลัง: T-03, T-05
- เสร็จเมื่อ: endpoint `POST /activities/{activityId}/registration-confirmation` สร้าง Notification ภายในเว็บไซต์หลังบันทึกสำเร็จ แสดงเป็นยังไม่อ่าน และเก็บไว้จนกว่านักศึกษาจะอ่าน
- สถานะ: พร้อมทำ

## ตารางตรวจความครบของ Acceptance Criteria

| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC-REG-01 | T-02 |
| AC-REG-02 | T-03 |
| AC-REG-03 | T-05 |
| AC-REG-04 | T-06 |
| AC-REG-05 | T-10 |
| AC-REG-06 | T-08 |
| AC-REG-07 | T-09 |

## ตารางตรวจความครบของ Constraints

| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| IF-GFORM-01 | T-02, T-03 |
| IF-GSHEET-01 | T-03 |
| IF-GSAPI-01 | T-04, T-05 |
| IF-GFORM-02 | T-06 |
| IF-NOT-01 | T-10 |
| ACC-GSHEET-01 | T-08 |
| ACC-GSHEET-02 | T-08, T-09 |
| CON-REG-01 | T-02, T-06 |
| NFR-PERF-01 | T-05, T-07 |
| NFR-SEC-01 | T-08 |
| NFR-SEC-02 | T-08, T-09 |

## สิ่งที่ยังไม่ทำ

Spec ปัจจุบันไม่มี Open Question ค้างอยู่ โดย ASM-01 ถึง ASM-12 เป็นสมมติฐานที่ระบุแนวทางการเชื่อม Google Form, Google Sheets, การยืนยันตัวตน, การคง snapshot และการแจ้งเตือนไว้แล้ว จึงไม่มี task ที่มีสถานะ “รอ Q-xx”

งานต่อไปนี้ยังไม่สร้างเพราะอยู่ใน Out of Scope: การยืนยันตัวตนนักศึกษา, การแก้ไข Google Sheets โดยนักศึกษา, การเช็คชื่อหน้างาน, การนำรายชื่อเข้า REG และการเปลี่ยนขั้นตอนอนุมัติโครงการของมหาวิทยาลัย
