# specs/005-ViewInfo/plan.md

# แผนงานฟีเจอร์: ดูข้อมูลผู้ลงทะเบียนจาก Google Sheets (ViewInfo)

---

## 1. สรุปแนวทาง

1. **การควบคุมสิทธิ์ (Access Control)**: จำกัดการเข้าถึงเฉพาะบัญชีผู้จัดกิจกรรม (ตัวแทนองค์การนักศึกษาที่เป็นเจ้าของกิจกรรม) และ Admin เท่านั้น นักศึกษาทั่วไปที่พยายามเข้าถึงจะได้รับข้อความปฏิเสธการเข้าถึง (Access Denied) (ACC-VIEW-01, ACC-VIEW-02, FR-VIEW-05)
2. **การดึงข้อมูลแบบ Near Real-time**: ระบบทำการเชื่อมต่อกับ Google Sheets API ของกิจกรรมเพื่อดึงรายชื่อและจำนวนผู้ตอบกลับ โดยใช้กลไก Polling อัปเดตข้อมูลทุกๆ 1–2 นาที (IF-VIEW-01, FR-VIEW-02, FR-VIEW-03, NFR-PERF-01)
3. **การจัดการกรณีเกิดข้อผิดพลาด (Fallback Strategy)**: หากการเชื่อมต่อ Google Sheets API ล้มเหลว ระบบจะแสดงข้อมูลล่าสุดเท่าที่เคยบันทึกไว้ในระบบ (Cache/Database) พร้อมระบุวันเวลาอัปเดตล่าสุด (Last Updated Time) ให้ผู้จัดกิจกรรมทราบ เพื่อป้องกันการแสดงหน้าจอผิดพลาดหรือหน้าว่างเปล่า (IF-VIEW-02, FR-VIEW-04)
4. **ความคุ้มครองข้อมูลส่วนบุคคล**: ข้อมูลผู้ลงทะเบียนทั้งหมดต้องถูกส่งผ่านโปรโตคอล HTTPS และมีการตรวจสอบ Authorization ทุกครั้งที่มีคำขอข้อมูล (NFR-SEC-01, NFR-SEC-02)

---

## 2. เทคโนโลยีที่ใช้

| สิ่งที่เลือก | มาจาก | หมายเหตุ |
|---|---|---|
| **React (Vite)** | ทีมเลือกเอง ไม่ได้มาจาก spec | ใช้ทำ UI หน้าแสดงผลรายชื่อผู้ลงทะเบียนและสถานะการอัปเดต |
| **Python FastAPI** | ทีมเลือกเอง ไม่ได้มาจาก spec | ใช้ทำ Backend API รับคำขอจาก Frontend และเชื่อมต่อ Google Sheets API |
| **Google Sheets API v4** | IF-VIEW-01, FR-VIEW-02 | ใช้ดึงข้อมูลผู้ลงทะเบียนจาก Google Sheets ของกิจกรรม |
| **APScheduler / Background Worker** | IF-VIEW-01, NFR-PERF-01 | ใช้ทำ Polling Job คอยดึงข้อมูลจาก Google Sheets ทุก 1–2 นาที |
| **Redis / Database Cache** | IF-VIEW-02, FR-VIEW-04 | ใช้เก็บบันทึกข้อมูลผู้ลงทะเบียนรอบล่าสุดสำหรับทำ Fallback เมื่อ API มีปัญหา |
| **HTTPS (TLS Encryption)** | NFR-SEC-01 | ใช้สำหรับการสื่อสารที่ปลอดภัยระหว่าง Client-Server |

---

## 3. โมเดลข้อมูล

### 3.1 RegisteredStudent (ดึงมาจาก Google Sheets & Cached)
| ฟิลด์หลัก | คำอธิบาย | รองรับ FR |
|---|---|---|
| `rowId` | ลำดับแถวใน Google Sheets | FR-VIEW-02 |
| `timestamp` | วันเวลาที่นักศึกษากรอกฟอร์ม | FR-VIEW-02, FR-VIEW-03 |
| `studentId` | รหัสนักศึกษา | FR-VIEW-02, FR-VIEW-03 |
| `fullName` | ชื่อ-นามสกุล | FR-VIEW-02, FR-VIEW-03 |
| `faculty` | คณะ/ภาควิชา (ถ้ามี) | FR-VIEW-02 |
| `email` | อีเมลนักศึกษา | FR-VIEW-02 |

### 3.2 ActivityRegistrationSummary (ข้อมูลสรุปและ Cache State)
| ฟิลด์หลัก | คำอธิบาย | รองรับ FR |
|---|---|---|
| `activityId` | รหัสกิจกรรม | FR-VIEW-01 |
| `totalRegistered` | จำนวนผู้ลงทะเบียนล่าสุด | FR-VIEW-03 |
| `lastSyncedAt` | วันเวลาอัปเดตข้อมูลสำเร็จล่าสุด | FR-VIEW-04 |
| `syncStatus` | สถานะการ Sync (`SUCCESS` / `FAILED`) | IF-VIEW-02, FR-VIEW-04 |
| `cachedResponses` | รายชื่อผู้ลงทะเบียนฉบับ Cache | FR-VIEW-04 |

---

## 4. API / หน้าจอ

### 4.1 หน้าจอ
- **หน้า View Registrants Detail (`/activities/:id/registrants`)**:
  - แสดงจำนวนผู้สมัครทั้งหมดและตารางรายชื่อผู้ลงทะเบียน (FR-VIEW-01, FR-VIEW-03)
  - แสดง Status Badge แจ้งเวลาอัปเดตล่าสุด หรือเตือนเมื่อ API มีปัญหา (FR-VIEW-04)
  - ป้องกันการเข้าถึงหากผู้ใช้ไม่ใช่ Admin หรือเจ้าของกิจกรรม (ACC-VIEW-01, ACC-VIEW-02)

### 4.2 API
- `GET /api/v1/activities/:id/registrants`
  - **Description**: ดึงรายชื่อและจำนวนผู้ลงทะเบียนของกิจกรรม
  - **Input**: `activityId` (Path parameter), Bearer Token (Header)
  - **Response**:
    ```json
    {
      "activityId": "ACT-001",
      "totalCount": 45,
      "lastSyncedAt": "2026-10-04T20:00:00Z",
      "isCache": false,
      "syncStatus": "SUCCESS",
      "data": [
        {
          "studentId": "660510001",
          "fullName": "นายสมชาย ใจดี",
          "timestamp": "2026-10-04T19:30:12Z"
        }
      ]
    }
    ```
  - **Error Responses**:
    - `403 Forbidden`: เมื่อผู้ใช้ไม่ใช่ Admin หรือผู้จัดกิจกรรมเจ้าของกิจกรรม (AC-VIEW-04)
    - `200 OK (with cache warning)`: เมื่อ API ดึง Google Sheets ล้มเหลว แต่มี Cache อยู่ (AC-VIEW-03)

---

## 5. ตารางตรวจ Constraints

| Constraint ID / ข้อความใน spec | ถูกนำไปใช้ที่ไหนใน plan | สถานะ |
|---|---|---|
| **IF-VIEW-01**: ดึงข้อมูลจาก Google Sheets ผ่าน API ด้วย Polling ทุก 1–2 นาที | APScheduler Background Worker + Polling Job | ใช้แล้ว |
| **IF-VIEW-02**: กรณีดึง API ไม่สำเร็จ ให้แสดงข้อมูลล่าสุดที่เคยดึงได้พร้อมเวลาอัปเดต ห้าม Crash | Redis/Database Cache Fallback Strategy + `isCache` Response Flag | ใช้แล้ว |
| **ACC-VIEW-01**: สิทธิ์การเข้าถึงจำกัดเฉพาะ Admin และผู้จัดกิจกรรมที่เป็นเจ้าของกิจกรรม | FastAPI Dependency Injection (`verify_event_owner_or_admin`) | ใช้แล้ว |
| **ACC-VIEW-02**: นักศึกษาทั่วไปห้ามดูข้อมูลผู้ลงทะเบียนคนอื่น | Authorization Check คืนค่า 403 Forbidden | ใช้แล้ว |
| **CON-VIEW-01**: มีผู้ลงทะเบียนอย่างน้อย 1 คน ระบบจึงจะเริ่มแสดงข้อมูล | Validation Check บน API/UI (ถ้า 0 คนให้แสดง Empty State) | ใช้แล้ว |

---

## 6. แผนทดสอบจาก Acceptance Criteria

| AC ID | ชื่อ test | ทดสอบอย่างไร |
|---|---|---|
| **AC-VIEW-01** | `test_AC_VIEW_01_fetch_registrants_success` | ให้ผู้จัดกิจกรรมเปิดดูหน้ารายละเอียด และตรวจสอบว่า API คืนค่ารายชื่อผู้ลงทะเบียนที่ดึงมาจาก Google Sheets ได้ถูกต้อง |
| **AC-VIEW-02** | `test_AC_VIEW_02_polling_updates_within_2_mins` | จำลองการเพิ่มผู้ลงทะเบียนใหม่ใน Google Sheets แล้วรอไม่เกิน 2 นาที ตรวจสอบว่าระบบอัปเดตจำนวนผู้ลงทะเบียนใหม่ |
| **AC-VIEW-03** | `test_AC_VIEW_03_fallback_to_cache_on_api_failure` | จำลองสถานการณ์ Google Sheets API ขัดข้อง (Network Error) แล้วขอดูข้อมูล ตรวจสอบว่าระบบแสดงข้อมูลเดิมใน Cache พร้อมระบุเวลาอัปเดตล่าสุด |
| **AC-VIEW-04** | `test_AC_VIEW_04_student_access_forbidden` | ให้บัญชีนักศึกษาทั่วไปพยายามเรียก API/เข้าหน้าดูรายชื่อ ตรวจสอบว่าระบบตอบกลับด้วย `403 Forbidden` |
| **AC-VIEW-05** | `test_AC_VIEW_05_authorized_user_access_granted` | ให้บัญชี Admin หรือผู้จัดกิจกรรมที่เป็นเจ้าของกิจกรรมเข้าใช้งาน ตรวจสอบว่าสามารถเข้าถึงข้อมูลได้สำเร็จ |

---

## 7. ลำดับงาน

1. **ตั้งค่า Authorization & Middleware**: สร้าง Logic ตรวจสอบสิทธิ์ผู้จัดกิจกรรม (Event Owner) และ Admin ตามข้อกำหนด ACC-VIEW-01, ACC-VIEW-02 และ AC-VIEW-04, AC-VIEW-05
2. **พัฒนาระบบเชื่อมต่อ Google Sheets API**: เขียน Service สำหรับอ่านข้อมูลจาก Google Sheets ผ่าน Google Sheets API v4 ตาม IF-VIEW-01
3. **พัฒนาระบบ Background Polling & Cache**: ตั้งค่า Task Polling ทุก 1–2 นาที บันทึกผลลง Cache/Database และจัดการกรณี Sync Fails เพื่อรองรับ Fallback (IF-VIEW-02, NFR-PERF-01)
4. **พัฒนา API Endpoint**: สร้าง Endpoint `GET /api/v1/activities/:id/registrants` สำหรับส่งข้อมูลรายชื่อ/สรุปยอดให้ Frontend (FR-VIEW-01 - FR-VIEW-04)
5. **พัฒนา Frontend UI ViewInfo**: สร้างหน้าตารางแสดงข้อมูลผู้ลงทะเบียน ยอดสรุปผู้สมัคร และ Alert Component แสดงเวลาอัปเดตล่าสุดหรือสถานะ Cache
6. **ทำ Integration & Security Test**: ทดสอบการเข้าถึงข้าม Role (RBAC) และทดสอบระบบ Fallback กรณี Google Sheets API ล่มตาม AC-VIEW-01 ถึง AC-VIEW-05

---

## 8. สิ่งที่ยังไม่ทำ

- **การดาวน์โหลดไฟล์ Excel/CSV**: จัดอยู่ในฟีเจอร์ UC-11 / `006-ExportList` (Out of Scope)
- **การแก้ไข/ลบข้อมูลผู้ลงทะเบียน**: จัดอยู่นอกขอบเขตการทำงานของระบบ (Out of Scope)
- **การเช็คชื่อหน้างานและการส่งข้อมูลเข้า REG**: จัดอยู่นอกขอบเขตฟีเจอร์ ViewInfo (Out of Scope)
- **Open Questions ใน spec**:
  - *Q-VIEW-01*: รูปแบบคอลัมน์ข้อมูลที่จะแสดง จะแมปตามโครงสร้างมาตรฐาน (รหัส, ชื่อ, คณะ) ไปก่อนจนกว่าผู้ดูแลระบบจะยืนยันเพิ่มเติม
  - *Q-VIEW-02*: ระบบ Pagination จะถูกพิจารณาเพิ่มเติมหากจำนวนผู้ลงทะเบียนเกิน 100 รายการ