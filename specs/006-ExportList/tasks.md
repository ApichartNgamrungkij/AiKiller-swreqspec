# Tasks: ดาวน์โหลดรายชื่อจาก Google Sheets (ExportList)

- Feature: ดาวน์โหลดรายชื่อจาก Google Sheets (ExportList)
- Spec ID: `006-ExportList`
- อ้างอิง: [plan.md](./plan.md)
- วันที่: 2026-10-05

ฟีเจอร์นี้แบ่งเป็น 9 task ตามลำดับโมเดลข้อมูล, การอ่าน Google Sheets, สิทธิ์, หน้ากิจกรรม และการตรวจขอบเขต REG  
ไม่มี task ที่ต้องรอ Open Question เนื่องจาก spec ไม่มี Open Question ค้างอยู่

## รายการ task

### T-01 สร้างโมเดลแหล่งข้อมูลรายชื่อและสิทธิ์
- รองรับ: FR-EXP-01, FR-EXP-02, IF-GSHEET-01, CON-EXPORT-01, ACC-GSHEET-01, ACC-GSHEET-02, NFR-SEC-01, NFR-SEC-02
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-02 และ T-03
- ไฟล์ที่แตะ: `backend/app/models/activity_export_source.py`, `backend/app/models/access_role.py`, `frontend/src/types/export.ts`
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: โมเดลมี `activity_id`, `google_sheet_url`, `last_successful_response_count`, `last_successful_read_at` และข้อมูลบทบาทตาม plan.md ข้อ 3 โดยไม่มีฟิลด์สำหรับการเช็คชื่อหรืออัปโหลดเข้า REG
- สถานะ: พร้อมทำ

### T-02 อ่านจำนวนผู้ลงทะเบียนล่าสุดจาก Google Sheets
- รองรับ: FR-EXP-01, IF-GSHEET-01, CON-EXPORT-01, ASM-01, ASM-06
- ตรวจด้วย: AC-EXP-01
- ไฟล์ที่แตะ: `backend/app/integrations/google_sheets.py`, `backend/app/services/export_source_service.py`, `backend/app/api/export_access.py`
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: endpoint `GET /activities/{activityId}/export-access` คืน `can_export=true` เฉพาะเมื่อจำนวนล่าสุดที่อ่านสำเร็จมีอย่างน้อย 1 คน
- สถานะ: พร้อมทำ

### T-03 สร้างการตรวจสิทธิ์เข้าถึง Google Sheets
- รองรับ: ACC-GSHEET-01, ACC-GSHEET-02, NFR-SEC-01, NFR-SEC-02, ASM-02
- ตรวจด้วย: AC-EXP-07
- ไฟล์ที่แตะ: `backend/app/services/access_control.py`, `backend/app/api/export_access.py`, `backend/app/api/google_sheet.py`
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: ระบบตรวจบทบาททุกครั้งก่อนแสดงสิทธิ์และก่อนเปิด Google Sheets โดยอนุญาตเฉพาะ Admin/ผู้จัดกิจกรรม
- สถานะ: พร้อมทำ

### T-04 สร้างหน้ากิจกรรมและปุ่มดาวน์โหลดรายชื่อด้วย API จำลอง
- รองรับ: FR-EXP-01, FR-EXP-02, CON-EXPORT-01
- ตรวจด้วย: AC-EXP-01
- ไฟล์ที่แตะ: `frontend/src/pages/ActivityPage.tsx`, `frontend/src/components/ExportListButton.tsx`, `frontend/src/mocks/exportAccess.ts`
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: หน้ากิจกรรมแสดงปุ่ม “ดาวน์โหลดรายชื่อ” เมื่อข้อมูลจำลองระบุว่ามีผู้ลงทะเบียนและผู้ใช้มีสิทธิ์
- สถานะ: พร้อมทำ

### T-05 พาผู้จัดกิจกรรมไปยัง Google Sheets โดยตรง
- รองรับ: FR-EXP-02, IF-EXPORT-01, IF-GSHEET-01, ACC-GSHEET-01, ACC-GSHEET-02, ASM-05
- ตรวจด้วย: AC-EXP-02
- ไฟล์ที่แตะ: `backend/app/api/google_sheet.py`, `frontend/src/services/exportApi.ts`, `frontend/src/components/ExportListButton.tsx`
- ต้องทำหลัง: T-02, T-03, T-04
- เสร็จเมื่อ: endpoint `GET /activities/{activityId}/google-sheet` ตรวจสิทธิ์ซ้ำและนำผู้จัดกิจกรรมไปยัง URL Google Sheets ที่ถูกต้องโดยตรง
- สถานะ: พร้อมทำ

### T-06 รองรับการดาวน์โหลดและบันทึกข้อมูลทุกคอลัมน์
- รองรับ: FR-EXP-03, FR-EXP-04, ASM-03
- ตรวจด้วย: AC-EXP-03
- ไฟล์ที่แตะ: `frontend/src/components/GoogleSheetExportGuide.tsx`, `backend/tests/integrations/test_google_sheets_export.py`
- ต้องทำหลัง: T-05
- เสร็จเมื่อ: การทดสอบข้อมูลจำลองหลายคอลัมน์ยืนยันว่า Google Sheets รองรับ `.xlsx` และ `.csv` โดยไม่มีการตัดหรือปรับรูปแบบคอลัมน์
- สถานะ: พร้อมทำ

### T-07 ตรวจสอบความสอดคล้องกับกระบวนการ REG เดิม
- รองรับ: FR-EXP-05, FR-EXP-06, IF-REG-01, DOM-APP-01, ASM-04, ASM-07
- ตรวจด้วย: AC-EXP-04, AC-EXP-05, AC-EXP-06
- ไฟล์ที่แตะ: `docs/integration/export-reg-process.md`, `backend/tests/api/test_export_scope.py`
- ต้องทำหลัง: T-05, T-06
- เสร็จเมื่อ: มีผลทดสอบยืนยันว่าไฟล์ถูกนำไปใช้ต่อโดยผู้จัดกิจกรรมเอง ไม่มี endpoint อัปโหลดเข้า REG และไม่มีการเปลี่ยนขั้นตอนอนุมัติโครงการเดิม
- สถานะ: พร้อมทำ

### T-08 แสดงข้อผิดพลาดเมื่อแหล่งข้อมูลหรือลิงก์ไม่พร้อม
- รองรับ: FR-EXP-01, FR-EXP-02, IF-GSHEET-01, IF-EXPORT-01, ASM-05
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-05
- ไฟล์ที่แตะ: `backend/app/services/export_source_service.py`, `backend/app/api/google_sheet.py`, `frontend/src/components/ExportErrorState.tsx`
- ต้องทำหลัง: T-02, T-03, T-04
- เสร็จเมื่อ: เมื่อ Google Sheets หรือลิงก์ไม่พร้อม ระบบแสดงข้อผิดพลาดที่เห็นได้และไม่ส่ง URL ที่ใช้งานไม่ได้
- สถานะ: พร้อมทำ

### T-09 เชื่อมหน้ากิจกรรมกับ API จริงและทดสอบสิทธิ์นักศึกษา
- รองรับ: FR-EXP-01, FR-EXP-02, ACC-GSHEET-02, NFR-SEC-01, NFR-SEC-02
- ตรวจด้วย: AC-EXP-07, AC-EXP-08
- ไฟล์ที่แตะ: `frontend/src/services/exportApi.ts`, `frontend/src/pages/ActivityPage.tsx`, `backend/tests/api/test_student_google_sheet_access.py`
- ต้องทำหลัง: T-03, T-04, T-05, T-08
- เสร็จเมื่อ: หน้าจอใช้ API จริง แสดงปุ่มและเปิดลิงก์ได้เฉพาะ Admin/ผู้จัดกิจกรรม และคำขอจากนักศึกษาถูกปฏิเสธโดยไม่ส่ง URL หรือข้อมูล Google Sheets
- สถานะ: พร้อมทำ

## ตารางตรวจความครบของ Acceptance Criteria

| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC-EXP-01 | T-02, T-04 |
| AC-EXP-02 | T-05 |
| AC-EXP-03 | T-06 |
| AC-EXP-04 | T-07 |
| AC-EXP-05 | T-07 |
| AC-EXP-06 | T-07 |
| AC-EXP-07 | T-03, T-09 |
| AC-EXP-08 | T-09 |

## ตารางตรวจความครบของ Constraints

| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| IF-GSHEET-01 | T-01, T-02, T-05, T-08 |
| IF-EXPORT-01 | T-05, T-08 |
| IF-REG-01 | T-07 |
| DOM-APP-01 | T-07 |
| ACC-GSHEET-01 | T-03, T-05, T-09 |
| ACC-GSHEET-02 | T-03, T-05, T-09 |
| CON-EXPORT-01 | T-02, T-04 |
| NFR-SEC-01 | T-03, T-09 |
| NFR-SEC-02 | T-03, T-09 |

## สิ่งที่ยังไม่ทำ

Spec ปัจจุบันไม่มี Open Question ค้างอยู่ โดย ASM-01 ถึง ASM-07 ระบุเงื่อนไขของ Google Sheets, สิทธิ์, รูปแบบไฟล์ และการดำเนินการต่อใน REG ไว้แล้ว จึงไม่มี task ที่มีสถานะ “รอ Q-xx”

งานต่อไปนี้ยังไม่สร้างเพราะอยู่ใน Out of Scope: การลงทะเบียน, การเช็คชื่อหน้างาน, การอัปโหลดรายชื่อเข้า REG โดยอัตโนมัติ, การแก้ไขข้อมูลผู้ลงทะเบียนใน Google Sheets, การจัดการสิทธิ์ของ Google Sheets โดยนักศึกษา และการเปลี่ยนขั้นตอนอนุมัติโครงการเดิม
