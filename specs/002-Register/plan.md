# แผนการพัฒนาฟีเจอร์ Register

## ปัญหาและแนวทาง

ฟีเจอร์นี้ให้นักศึกษาที่เข้าสู่ระบบแล้วลงทะเบียนกิจกรรมผ่าน Google Form ที่ฝังในหน้ารายละเอียดกิจกรรม โดย Google Form บันทึกคำตอบลง Google Sheets ของกิจกรรม ระบบอ่านจำนวนแถวคำตอบผ่าน Google Sheets API เพื่อคำนวณสถานะ “ว่าง/เต็มแล้ว” และส่ง Notification ยืนยันภายในเว็บไซต์ แนวทางคือแยกหน้ารายละเอียดกิจกรรมกับชั้นเชื่อมต่อ Google Form/Google Sheets และควบคุมสิทธิ์การเข้าถึงข้อมูลตามบทบาท โดยคงจำนวนและสถานะเดิมเมื่อ API อ่านข้อมูลไม่สำเร็จ

## 1. สรุปแนวทาง

1. แสดง Google Form ที่เชื่อมกับกิจกรรมในหน้ารายละเอียดสำหรับนักศึกษาที่เข้าสู่ระบบและกิจกรรมยังไม่เต็ม
2. ให้ Google Form เป็นผู้รับข้อมูลและบันทึกคำตอบลง Google Sheets ของกิจกรรมโดยอัตโนมัติ
3. อ่านจำนวนแถวคำตอบผ่าน Google Sheets API แล้วคำนวณสถานะจากจำนวนจำกัดที่ตรงกับค่าของกิจกรรม
4. คงค่าเดิมเมื่อ API อ่านข้อมูลไม่สำเร็จ และอัปเดตสถานะภายใน 2 นาทีหลัง Google Sheets เปลี่ยนแปลง
5. ส่ง Notification ภายในเว็บไซต์หลังข้อมูลถูกบันทึกสำเร็จ และจำกัดการเข้าถึง Google Sheets ตามบทบาท

## 2. เทคโนโลยีที่ใช้

| สิ่งที่เลือก | มาจาก | หมายเหตุ |
|---|---|---|
| React (Vite) สำหรับหน้าบ้าน | ทีมเลือกเอง ไม่ได้มาจาก spec | ใช้สร้างหน้ารายละเอียดกิจกรรมและพื้นที่ฝัง Google Form |
| Python FastAPI สำหรับหลังบ้าน | ทีมเลือกเอง ไม่ได้มาจาก spec | ใช้เป็นชั้นบริการสถานะ การตรวจสิทธิ์ และ Notification |
| Google Form แบบฝัง | IF-GFORM-01 | ใช้เป็นช่องทางกรอกและส่งข้อมูลการลงทะเบียน |
| Google Sheets API | IF-GSAPI-01 | ใช้อ่านจำนวนผู้ตอบจาก Google Sheets เท่านั้น |
| ระบบ Notification ภายในเว็บไซต์ | IF-NOT-01 | ใช้ส่งและเก็บ Notification ยืนยัน |
| กลไกตรวจสิทธิ์ของระบบเดิม | ACC-GSHEET-01, ACC-GSHEET-02 | ตรวจบทบาท Admin/ผู้จัดกิจกรรมและป้องกันนักศึกษา |

## 3. โมเดลข้อมูล

| Entity | ฟิลด์หลัก | รองรับ |
|---|---|---|
| Activity | `activity_id`, `capacity`, `registration_status`, `google_form_url`, `google_sheet_id` | FR-REG-01, FR-REG-04, FR-REG-05, FR-REG-06, CON-REG-01 |
| RegistrationCountSnapshot | `activity_id`, `response_count`, `last_successful_sync_at` | FR-REG-04, FR-REG-05, NFR-PERF-01, ASM-08 |
| Notification | `notification_id`, `student_id`, `activity_id`, `message`, `is_read`, `created_at` | FR-REG-07, IF-NOT-01, AC-REG-05 |
| AccessRole | `user_id`, `role`, `activity_id` | ACC-GSHEET-01, ACC-GSHEET-02, NFR-SEC-01, NFR-SEC-02 |

ไม่มี entity หรือฟิลด์สำหรับการแก้ไข Google Sheets โดยนักศึกษา การเช็คชื่อหน้างาน หรือการนำรายชื่อเข้าสู่ระบบ REG เนื่องจากอยู่นอก Scope

## 4. API / หน้าจอ

- `GET /activities/{activityId}` — รับรายละเอียดกิจกรรม จำนวนจำกัด สถานะ และ URL สำหรับฝัง Google Form; รองรับ FR-REG-01, CON-REG-01
- `GET /activities/{activityId}/registration-form` — ตรวจว่ายังไม่เต็มและส่งข้อมูลการฝัง Google Form; รองรับ FR-REG-01, FR-REG-02, AC-REG-01
- `POST /activities/{activityId}/registration-sync` — อ่านจำนวนแถวคำตอบผ่าน Google Sheets API และอัปเดต snapshot/สถานะเมื่ออ่านสำเร็จ; รองรับ FR-REG-04, FR-REG-05, FR-REG-06, NFR-PERF-01, AC-REG-03, AC-REG-04
- `POST /activities/{activityId}/registration-confirmation` — สร้าง Notification หลังตรวจว่าข้อมูลถูกบันทึกใน Google Sheets สำเร็จ; รองรับ FR-REG-07, IF-NOT-01, AC-REG-05
- `GET /activities/{activityId}/google-sheet-access` — ตรวจสิทธิ์และอนุญาตเฉพาะ Admin/ผู้จัดกิจกรรม ไม่เปิดข้อมูลให้นักศึกษา; รองรับ ACC-GSHEET-01, ACC-GSHEET-02, NFR-SEC-01, NFR-SEC-02, AC-REG-06, AC-REG-07
- หน้ารายละเอียดกิจกรรม — แสดง Google Form เมื่อสถานะไม่เต็ม และไม่แสดงหรือไม่ให้ใช้งานเมื่อ “เต็มแล้ว”; รองรับ FR-REG-01, FR-REG-02, IF-GFORM-01, IF-GFORM-02, AC-REG-01, AC-REG-04

## 5. ตารางตรวจ Constraints

| Constraint ID | ถูกนำไปใช้ที่ไหนใน plan | สถานะ |
|---|---|---|
| IF-GFORM-01 | หน้ารายละเอียดกิจกรรมและการฝัง Google Form | ใช้แล้ว |
| IF-GSHEET-01 | Google Form เชื่อม Google Sheets ของกิจกรรมใน ASM-01 และ AC-REG-02 | ใช้แล้ว |
| IF-GSAPI-01 | `registration-sync` อ่านจำนวนแถวผ่าน Google Sheets API | ใช้แล้ว |
| IF-GFORM-02 | การตรวจจำนวนถึง capacity และสถานะ “เต็มแล้ว” | ใช้แล้ว |
| IF-NOT-01 | `registration-confirmation` และ entity Notification | ใช้แล้ว |
| ACC-GSHEET-01 | AccessRole และ endpoint ตรวจสิทธิ์ Admin/ผู้จัดกิจกรรม | ใช้แล้ว |
| ACC-GSHEET-02 | endpoint ปฏิเสธการเข้าถึง Google Sheets ของนักศึกษา | ใช้แล้ว |
| CON-REG-01 | ตรวจสถานะก่อนแสดง/ใช้งาน Google Form | ใช้แล้ว |

## 6. แผนทดสอบจาก Acceptance Criteria

| AC ID | ชื่อ test | ทดสอบอย่างไร |
|---|---|---|
| AC-REG-01 | `test_AC_REG_01_embeds_form_for_available_activity` | จำลองนักศึกษาที่เข้าสู่ระบบและกิจกรรมยังไม่เต็ม เปิดหน้ารายละเอียด แล้วตรวจว่ามี Google Form ฝังอยู่ |
| AC-REG-02 | `test_AC_REG_02_google_form_response_is_saved` | จำลองการส่ง Google Form สำเร็จ แล้วตรวจว่าคำตอบถูกบันทึกใน Google Sheets ที่เชื่อมกับกิจกรรม |
| AC-REG-03 | `test_AC_REG_03_syncs_row_count_and_status_within_two_minutes` | เพิ่มแถวคำตอบ รวมแถวซ้ำ เรียก sync และตรวจว่านับทุกแถว ไม่ตัดซ้ำ พร้อมอัปเดตจำนวน/สถานะภายใน 2 นาที |
| AC-REG-04 | `test_AC_REG_04_closes_form_and_marks_activity_full` | ตั้งจำนวนคำตอบเท่ากับ capacity ตรวจการปิดรับของ Google Form และสถานะกิจกรรมเป็น “เต็มแล้ว” |
| AC-REG-05 | `test_AC_REG_05_creates_unread_confirmation_notification` | จำลองข้อมูลถูกบันทึกใน Google Sheets แล้วตรวจ Notification ภายในเว็บไซต์ว่าถูกสร้างและคงอยู่จนอ่าน |
| AC-REG-06 | `test_AC_REG_06_allows_admin_or_activity_organizer_sheet_access` | ทดสอบผู้ใช้บทบาท Admin และผู้จัดกิจกรรมว่าได้รับอนุญาต และบทบาทอื่นไม่ได้รับอนุญาต |
| AC-REG-07 | `test_AC_REG_07_denies_student_sheet_access` | จำลองนักศึกษาที่เข้าสู่ระบบพยายามเข้าถึง Google Sheets แล้วตรวจว่าระบบปฏิเสธ |

## 7. ลำดับงาน

1. สำรวจและเชื่อมข้อมูลกิจกรรมกับ Google Form/Google Sheets ตาม ASM-01, IF-GFORM-01, IF-GSHEET-01
2. สร้างหน้ารายละเอียดกิจกรรมและเงื่อนไขกิจกรรมว่าง/เต็มตาม FR-REG-01, FR-REG-02, CON-REG-01, AC-REG-01
3. สร้าง adapter อ่าน Google Sheets API และนับทุกแถวโดยไม่ตัดซ้ำตาม FR-REG-03, FR-REG-04, AC-REG-02, AC-REG-03
4. สร้างการคำนวณและบันทึกสถานะ “ว่าง/เต็มแล้ว” รวมการปิดรับตาม FR-REG-05, FR-REG-06, IF-GFORM-02, AC-REG-04
5. เพิ่มการคง snapshot เดิมเมื่อ API ไม่ตอบสนองตาม ASM-08
6. เพิ่มการตรวจสิทธิ์ Google Sheets ตาม ACC-GSHEET-01, ACC-GSHEET-02, NFR-SEC-01, NFR-SEC-02, AC-REG-06, AC-REG-07
7. เพิ่มการสร้างและเก็บ Notification หลังบันทึกสำเร็จตาม FR-REG-07, IF-NOT-01, AC-REG-05
8. ทดสอบ Acceptance Criteria ทั้งหมดและทดสอบเงื่อนไขเวลา NFR-PERF-01

## 8. สิ่งที่ยังไม่ทำ

ไม่มี Open Questions ใน spec ฉบับนี้ ส่วนที่เกี่ยวข้องกับคำถามที่ยังไม่มีคำตอบจึงไม่มีรายการที่ต้องระงับการสร้าง
