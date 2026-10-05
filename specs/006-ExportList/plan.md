# แผนการพัฒนาฟีเจอร์ ExportList

## ปัญหาและแนวทาง

ฟีเจอร์นี้ให้ผู้จัดกิจกรรมที่มีผู้ลงทะเบียนเข้าถึง Google Sheets ของกิจกรรมและดาวน์โหลดข้อมูลเป็น `.xlsx` หรือ `.csv` เพื่อใช้เช็คชื่อหน้างานและดำเนินการต่อในระบบ REG ด้วยตนเอง แนวทางคืออ่านจำนวนล่าสุดจาก Google Sheets เพื่อควบคุมการแสดงปุ่ม ตรวจสอบสิทธิ์ทุกครั้งก่อนแสดงปุ่มและก่อนเปิด Google Sheets และไม่สร้างการอัปโหลดเข้า REG หรือเปลี่ยนขั้นตอนอนุมัติโครงการ

## 1. สรุปแนวทาง

1. แสดงปุ่ม “ดาวน์โหลดรายชื่อ” เฉพาะกิจกรรมที่มีจำนวนล่าสุดจาก Google Sheets อย่างน้อย 1 คน
2. ตรวจสิทธิ์ผู้ใช้ทุกครั้งก่อนแสดงปุ่มและก่อนเปิด Google Sheets
3. เมื่อกดปุ่ม ให้นำผู้จัดกิจกรรมไปยัง Google Sheets ของกิจกรรมนั้นโดยตรง
4. ให้ผู้จัดกิจกรรมดาวน์โหลดหรือบันทึก `.xlsx` และ `.csv` โดยใช้ทุกคอลัมน์เดิมจาก Google Sheets
5. ไม่อัปโหลดข้อมูลเข้า REG อัตโนมัติ และไม่เปลี่ยนกระบวนการอนุมัติโครงการเดิม

## 2. เทคโนโลยีที่ใช้

| สิ่งที่เลือก | มาจาก | หมายเหตุ |
|---|---|---|
| React (Vite) สำหรับหน้าบ้าน | ทีมเลือกเอง ไม่ได้มาจาก spec | ใช้แสดงปุ่มและข้อความผิดพลาดบนหน้ากิจกรรม |
| Python FastAPI สำหรับหลังบ้าน | ทีมเลือกเอง ไม่ได้มาจาก spec | ใช้ตรวจสิทธิ์ จำนวนล่าสุด และ URL Google Sheets |
| Google Sheets | IF-GSHEET-01 | แหล่งข้อมูลรายชื่อและจุดหมายปลายทางของผู้จัดกิจกรรม |
| ระบบยืนยันตัวตนและบทบาทเดิม | ACC-GSHEET-01, ACC-GSHEET-02 | ใช้ระบุ Admin ผู้จัดกิจกรรม และนักศึกษา |

## 3. โมเดลข้อมูล

| Entity | ฟิลด์หลัก | รองรับ |
|---|---|---|
| ActivityExportSource | `activity_id`, `google_sheet_url`, `last_successful_response_count`, `last_successful_read_at` | IF-GSHEET-01, IF-EXPORT-01, CON-EXPORT-01, FR-EXP-01, FR-EXP-02 |
| AccessRole | `user_id`, `role`, `activity_id` | ACC-GSHEET-01, ACC-GSHEET-02, NFR-SEC-01, NFR-SEC-02, AC-EXP-07, AC-EXP-08 |

ระบบไม่สร้าง entity สำหรับข้อมูลเช็คชื่อหน้างานหรือข้อมูลนำเข้า REG อัตโนมัติ เพราะอยู่นอก Scope และไม่แก้ไขข้อมูลใน Google Sheets

## 4. API / หน้าจอ

- `GET /activities/{activityId}/export-access` — ตรวจบทบาทและจำนวนล่าสุดจาก Google Sheets; ส่ง `can_export`, `response_count`, `google_sheet_url` เมื่อผ่านเงื่อนไข; รองรับ FR-EXP-01, CON-EXPORT-01, NFR-SEC-01, NFR-SEC-02, AC-EXP-01, AC-EXP-07, AC-EXP-08
- `GET /activities/{activityId}/google-sheet` — ตรวจสิทธิ์ซ้ำก่อนส่ง URL เพื่อพาไป Google Sheets; เมื่อแหล่งข้อมูลหรือลิงก์ไม่พร้อมให้ผลผิดพลาดโดยไม่ส่งลิงก์ใช้ไม่ได้; รองรับ IF-GSHEET-01, IF-EXPORT-01, ACC-GSHEET-01, ACC-GSHEET-02, FR-EXP-02, ASM-05, AC-EXP-02
- หน้ากิจกรรม — แสดงปุ่ม “ดาวน์โหลดรายชื่อ” เฉพาะเมื่อ `can_export=true`; แสดงข้อผิดพลาดเมื่อข้อมูลหรือลิงก์ไม่พร้อม; รองรับ FR-EXP-01, FR-EXP-02, AC-EXP-01, AC-EXP-02
- Google Sheets — ให้ผู้จัดกิจกรรมเลือกดาวน์โหลดหรือบันทึก `.xlsx` และ `.csv` โดยไม่ตัดหรือปรับคอลัมน์; รองรับ FR-EXP-03, FR-EXP-04, AC-EXP-03
- ขั้นตอน REG เดิม — ผู้จัดกิจกรรมนำไฟล์ไปดำเนินการต่อเอง ไม่มี endpoint อัปโหลดอัตโนมัติ; รองรับ IF-REG-01, FR-EXP-05, FR-EXP-06, AC-EXP-04, AC-EXP-05

## 5. ตารางตรวจ Constraints

| Constraint ID | ถูกนำไปใช้ที่ไหนใน plan | สถานะ |
|---|---|---|
| IF-GSHEET-01 | ActivityExportSource และ endpoint ตรวจแหล่งข้อมูล/URL Google Sheets | ใช้แล้ว |
| IF-EXPORT-01 | endpoint `google-sheet` และหน้ากิจกรรมที่พาไป Google Sheets โดยตรง | ใช้แล้ว |
| IF-REG-01 | ระบุให้ผู้จัดกิจกรรมดำเนินการต่อใน REG ตามขั้นตอนเดิม | ใช้แล้ว |
| DOM-APP-01 | ไม่มีฟังก์ชันหรือ endpoint เปลี่ยนขั้นตอนอนุมัติโครงการ | ใช้แล้ว |
| ACC-GSHEET-01 | ตรวจบทบาท Admin/ผู้จัดกิจกรรมทุกครั้งก่อนแสดงปุ่มและเปิด Google Sheets | ใช้แล้ว |
| ACC-GSHEET-02 | ปฏิเสธนักศึกษาและไม่ส่ง URL Google Sheets | ใช้แล้ว |
| CON-EXPORT-01 | แสดงปุ่มเมื่อจำนวนล่าสุดที่อ่านสำเร็จอย่างน้อย 1 คน | ใช้แล้ว |

## 6. แผนทดสอบจาก Acceptance Criteria

| AC ID | ชื่อ test | ทดสอบอย่างไร |
|---|---|---|
| AC-EXP-01 | `test_AC_EXP_01_shows_export_button_for_activity_with_registrants` | จำลองกิจกรรมที่จำนวนล่าสุดจาก Google Sheets เท่ากับหรือมากกว่า 1 และผู้จัดกิจกรรมมีสิทธิ์ แล้วตรวจว่าปุ่มแสดง |
| AC-EXP-02 | `test_AC_EXP_02_redirects_organizer_to_google_sheet` | กดปุ่มด้วยผู้จัดกิจกรรมที่ผ่านสิทธิ์ แล้วตรวจว่า URL ปลายทางเป็น Google Sheets ของกิจกรรมนั้น |
| AC-EXP-03 | `test_AC_EXP_03_preserves_all_columns_in_xlsx_and_csv_exports` | จำลองข้อมูลหลายคอลัมน์จาก Google Sheets แล้วตรวจว่าไฟล์ `.xlsx` และ `.csv` มีทุกคอลัมน์โดยไม่ปรับรูปแบบหรือตัดข้อมูล |
| AC-EXP-04 | `test_AC_EXP_04_exported_file_is_usable_in_reg_process` | ตรวจว่าไฟล์ที่ดาวน์โหลดมีรูปแบบที่ REG รองรับ และยืนยันว่าผู้จัดกิจกรรมเป็นผู้ดำเนินการต่อเอง |
| AC-EXP-05 | `test_AC_EXP_05_does_not_upload_to_reg_automatically` | ตรวจว่าไม่มีการเรียก endpoint หรือการส่งข้อมูลอัตโนมัติไปยัง REG หลังดาวน์โหลด |
| AC-EXP-06 | `test_AC_EXP_06_preserves_existing_project_approval_process` | ตรวจว่า feature นี้ไม่แก้ไขหรือแทนที่ขั้นตอนอนุมัติโครงการเดิม |
| AC-EXP-07 | `test_AC_EXP_07_allows_only_admin_or_activity_organizer` | ทดสอบ Admin และผู้จัดกิจกรรมว่าเข้าถึงได้ และบทบาทอื่นถูกปฏิเสธ |
| AC-EXP-08 | `test_AC_EXP_08_denies_student_google_sheet_access` | จำลองนักศึกษาที่เข้าสู่ระบบแล้วพยายามเปิด Google Sheets และตรวจว่าไม่มีสิทธิ์/ไม่มี URL ถูกส่งกลับ |

## 7. ลำดับงาน

1. สำรวจข้อมูลกิจกรรม ลิงก์ Google Sheets และบทบาทผู้ใช้ตาม ASM-01, ASM-02, IF-GSHEET-01
2. สร้างการอ่านจำนวนล่าสุดจาก Google Sheets และเก็บเวลาการอ่านสำเร็จตาม ASM-06, CON-EXPORT-01, FR-EXP-01
3. สร้างการตรวจสิทธิ์ก่อนแสดงปุ่มและก่อนเปิดลิงก์ตาม ACC-GSHEET-01, ACC-GSHEET-02, NFR-SEC-01, NFR-SEC-02
4. สร้างหน้ากิจกรรมและปุ่ม “ดาวน์โหลดรายชื่อ” ตาม FR-EXP-01, FR-EXP-02, AC-EXP-01, AC-EXP-02
5. เชื่อม Google Sheets ให้ผู้จัดกิจกรรมดาวน์โหลด `.xlsx` และ `.csv` โดยคงทุกคอลัมน์ตาม FR-EXP-03, FR-EXP-04, AC-EXP-03
6. เพิ่มการแจ้งข้อผิดพลาดและไม่ส่งลิงก์ที่ใช้ไม่ได้ตาม ASM-05
7. ตรวจขอบเขต REG และขั้นตอนอนุมัติโครงการ ไม่สร้างการอัปโหลดอัตโนมัติหรือการแทนที่ขั้นตอนเดิมตาม IF-REG-01, DOM-APP-01, FR-EXP-05, FR-EXP-06, FR-EXP-07
8. รันทดสอบ AC-EXP-01 ถึง AC-EXP-08 และตรวจ traceability กับ spec

## 8. สิ่งที่ยังไม่ทำ

ไม่มี Open Questions ใน spec ฉบับนี้ ส่วนที่เกี่ยวข้องกับคำถามที่ยังไม่มีคำตอบจึงไม่มีรายการที่ต้องระงับการสร้าง
