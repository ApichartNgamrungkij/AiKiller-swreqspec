# Tasks: จัดการตารางส่วนตัว (Schedule)

- Feature: จัดการตารางส่วนตัว (Schedule)
- Spec ID: spec.md
- อ้างอิง plan.md: [plan.md](./plan.md)
- วันที่: 2026-10-06
- สรุป: มี 8 task ทั้งหมด และ 0 task ที่ต้องรอ Open Questions

## รายการ task

### T-01 กำหนดกติกาการซ้ำทุกวันและการคาบเกี่ยว
- รองรับ: FR-SCHED-02, FR-SCHED-03, IF-SCHED-01, ASM-SCHED-02, ASM-SCHED-06
- ตรวจด้วย: AC-SCHED-02, AC-SCHED-04, AC-SCHED-05, AC-SCHED-07
- ไฟล์ที่แตะ: `backend/app/models/personal_busy_period.py`, `backend/app/services/overlap_checker.py`, `backend/tests/test_overlap_logic.py`
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: ตัวตรวจช่วงเวลาทับซ้อนและการเกิดซ้ำทุกวันทำงานตามกติกา โดย 09:00-10:00 กับ 10:00-11:00 ถือว่าไม่คาบเกี่ยว
- สถานะ: พร้อมทำ

### T-02 จำกัดหน้าและ API ให้ใช้ได้หลังเข้าสู่ระบบ
- รองรับ: CON-SCHED-01, FR-SCHED-01
- ตรวจด้วย: AC-SCHED-01
- ไฟล์ที่แตะ: `frontend/src/routes/ScheduleRoute.tsx`, `backend/app/routes/me_schedule.py`, `backend/tests/test_schedule_auth.py`
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: ผู้ใช้ที่ยังไม่ได้เข้าสู่ระบบถูกปฏิเสธการเปิดหน้า “ตารางของฉัน” และเรียก API ตามสิทธิ์ของผู้ใช้ที่เข้าสู่ระบบแล้ว
- สถานะ: เสร็จ รอทีมตรวจ

### T-03 สร้าง API อ่านและบันทึกตารางส่วนตัว
- รองรับ: FR-SCHED-01, FR-SCHED-03, IF-SCHED-01
- ตรวจด้วย: AC-SCHED-02, AC-SCHED-03, AC-SCHED-04
- ไฟล์ที่แตะ: `backend/app/routes/me_schedule.py`, `backend/app/models/personal_busy_period.py`, `backend/tests/test_schedule_api.py`
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: GET/POST/PUT สำหรับ `/me/schedule` คืนข้อมูลของนักศึกษาผู้ใช้ปัจจุบันและคงรายการอื่นไว้เมื่อแก้ไขรายการที่เลือก
- สถานะ: เสร็จ รอทีมตรวจ

### T-04 สร้างหน้า “ตารางของฉัน” สำหรับเพิ่มและแก้ไขรายการ
- รองรับ: FR-SCHED-01, FR-SCHED-02, FR-SCHED-03, CON-SCHED-01
- ตรวจด้วย: AC-SCHED-01, AC-SCHED-02, AC-SCHED-03
- ไฟล์ที่แตะ: `frontend/src/pages/SchedulePage.tsx`, `frontend/src/components/BusyPeriodForm.tsx`, `frontend/src/hooks/useSchedule.ts`
- ต้องทำหลัง: T-02, T-03
- เสร็จเมื่อ: นักศึกษาเปิดหน้า “ตารางของฉัน” แล้วสามารถเพิ่มรายการใหม่หรือแก้ไขรายการที่เลือกและกดบันทึกได้โดยไม่ทำให้รายการอื่นหาย
- สถานะ: พร้อมทำ

### T-05 เชื่อมหน้ารายละเอียดกิจกรรมกับการตรวจคาบเกี่ยว
- รองรับ: FR-SCHED-04, FR-SCHED-05, IF-SCHED-01
- ตรวจด้วย: AC-SCHED-05, AC-SCHED-07
- ไฟล์ที่แตะ: `frontend/src/pages/ActivityDetailPage.tsx`, `frontend/src/services/scheduleOverlap.ts`, `backend/app/services/overlap_checker.py`
- ต้องทำหลัง: T-01, T-03
- เสร็จเมื่อ: ข้อมูลวันและเวลาของกิจกรรมถูกส่งไปตรวจกับข้อมูลตารางส่วนตัวที่นักศึกษาบันทึกไว้ และแสดงผลเตือนเมื่อมีช่วงทับกัน
- สถานะ: พร้อมทำ

### T-06 แสดงคำเตือนที่ไม่บล็อกการลงทะเบียน
- รองรับ: DOM-SCHED-01, FR-SCHED-05, FR-SCHED-06
- ตรวจด้วย: AC-SCHED-06
- ไฟล์ที่แตะ: `frontend/src/components/OverlapWarning.tsx`, `frontend/src/pages/ActivityDetailPage.tsx`, `frontend/tests/test_overlap_warning.py`
- ต้องทำหลัง: T-05
- เสร็จเมื่อ: ระบบแสดงคำเตือนว่ามีเวลาคาบเกี่ยว แต่ยังอนุญาตให้นักศึกษายังไปต่อได้ที่ขั้นตอนลงทะเบียน Google Form โดยไม่ติดบล็อก
- สถานะ: พร้อมทำ

### T-07 ทดสอบ NFR ที่รองรับผู้ใช้งานพร้อมกัน 5,000 คน
- รองรับ: NFR-SCHED-01, ASM-SCHED-05
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-08
- ไฟล์ที่แตะ: `backend/tests/test_schedule_concurrency.py`, `docs/schedule-load-test-plan.md`
- ต้องทำหลัง: T-03, T-05
- เสร็จเมื่อ: สคริปต์ทดสอบโหลดแสดงว่า 5,000 ผู้ใช้พร้อมกันสามารถเข้าถึงหน้าและฟังก์ชันตรวจคาบเกี่ยวได้ และผู้ใช้ที่เกินจำนวนจะต้องรอจนผู้ใช้ออกจากหน้าตารางส่วนตัวหรือหน้ากิจกรรม
- สถานะ: พร้อมทำ

### T-08 ทดสอบและตรวจสอบความครบของ AC และ Traceability
- รองรับ: FR-SCHED-01, FR-SCHED-02, FR-SCHED-03, FR-SCHED-04, FR-SCHED-05, FR-SCHED-06, CON-SCHED-01, IF-SCHED-01, DOM-SCHED-01, NFR-SCHED-01
- ตรวจด้วย: AC-SCHED-01, AC-SCHED-02, AC-SCHED-03, AC-SCHED-04, AC-SCHED-05, AC-SCHED-06, AC-SCHED-07
- ไฟล์ที่แตะ: `backend/tests/`, `frontend/tests/`, `specs/003-Schedule/tasks.md`
- ต้องทำหลัง: T-01, T-02, T-03, T-04, T-05, T-06, T-07
- เสร็จเมื่อ: test_AC_SCHED_01 ถึง test_AC_SCHED_07 และการทดสอบ NFR-SCHED-01 ผ่านตาม Traceability ใน spec.md
- สถานะ: พร้อมทำ

## ตารางตรวจความครบ

### 1) AC ID | task ที่ตรวจ AC นี้

| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC-SCHED-01 | T-02, T-04 |
| AC-SCHED-02 | T-01, T-03, T-04 |
| AC-SCHED-03 | T-03, T-04 |
| AC-SCHED-04 | T-01, T-03 |
| AC-SCHED-05 | T-01, T-05 |
| AC-SCHED-06 | T-06 |
| AC-SCHED-07 | T-01, T-05 |

### 2) Constraint ID | task ที่ทำให้เป็นจริง

| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| CON-SCHED-01 | T-02, T-04 |
| IF-SCHED-01 | T-01, T-03, T-05 |
| DOM-SCHED-01 | T-05, T-06 |
| NFR-SCHED-01 | T-07 |

## สิ่งที่ยังไม่ทำ

- Open Questions ใน spec: ไม่มี
- ไม่มี task ที่ต้องรอ Q-xx เนื่องจาก spec ถูกชี้แจงครบและไม่มีข้อสงสัยที่ต้องถาม
