# Tasks: สร้างกิจกรรมใหม่ (Create Activity)

- Feature: สร้างกิจกรรมใหม่ (Create Activity)
- Spec ID: spec.md
- อ้างอิง plan.md: [plan.md](./plan.md)
- วันที่: 2026-10-06
- สรุป: มี 9 task ทั้งหมด และ 0 task ที่ต้องรอ Open Questions

## รายการ task

### T-01 กำหนดโครงข้อมูลกิจกรรมและรอบเวลา
- รองรับ: FR-ACT-02, IF-ACT-02, ASM-ACT-03, ASM-ACT-05
- ตรวจด้วย: AC-ACT-02, AC-ACT-05
- ไฟล์ที่แตะ: `backend/app/models/activity.py`, `backend/app/models/activity_slot.py`, `backend/tests/test_activity_model.py`
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: รูปแบบข้อมูลกิจกรรมและวันเวลารอบในวันเดียวกันถูกกำหนดชัดเจนให้รองรับชื่อ/ประเภท/วันเวลา/สถานที่/จำนวนรับ/ชั่วโมงจิตอาสา พร้อม slot แบบเช้า-บ่ายได้
- สถานะ: เสร็จ รอทีมตรวจ

### T-02 จำกัดหน้า “สร้างกิจกรรมใหม่” ให้ใช้ได้เฉพาะผู้จัดที่มีสิทธิ์
- รองรับ: CON-ACT-01, FR-ACT-01, DOM-ACT-03
- ตรวจด้วย: AC-ACT-01
- ไฟล์ที่แตะ: `frontend/src/routes/CreateActivityRoute.tsx`, `backend/app/routes/activity.py`, `backend/tests/test_activity_auth.py`
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: ผู้จัดกิจกรรมที่ได้รับสิทธิ์จาก Admin เท่านั้นที่สามารถเปิดหน้า “สร้างกิจกรรมใหม่” ได้ และได้รับสิทธิ์ก่อนสร้างกิจกรรมจริง
- สถานะ: เสร็จ รอทีมตรวจ

### T-03 สร้างฟอร์มกรอกข้อมูลและการยืนยันก่อนบันทึก
- รองรับ: FR-ACT-01, FR-ACT-02, FR-ACT-03, ASM-ACT-02, ASM-ACT-03, ASM-ACT-04, ASM-ACT-05
- ตรวจด้วย: AC-ACT-02, AC-ACT-03, AC-ACT-04, AC-ACT-05
- ไฟล์ที่แตะ: `frontend/src/pages/CreateActivityPage.tsx`, `frontend/src/components/ActivityForm.tsx`, `frontend/src/components/ConfirmCreateDialog.tsx`
- ต้องทำหลัง: T-01, T-02
- เสร็จเมื่อ: ฟอร์มรองรับการกรอกข้อมูลหลักและ URL ลงทะเบียน พร้อมแสดงหน้าตรวจสอบอีกครั้งก่อนบันทึกจริง และมีโครงสร้างสำหรับรอบหลายรอบในวันเดียวกัน
- สถานะ: เสร็จ รอทีมตรวจ

### T-04 เพิ่ม validation สำหรับข้อมูลที่จำเป็นและประเภทที่รับรอง
- รองรับ: DOM-ACT-01, FR-ACT-04, FR-ACT-07, DOM-ACT-02, DOM-ACT-03
- ตรวจด้วย: AC-ACT-04, AC-ACT-05, AC-ACT-07
- ไฟล์ที่แตะ: `backend/app/services/activity_validation.py`, `frontend/src/utils/activityValidators.ts`, `backend/tests/test_activity_validation.py`
- ต้องทำหลัง: T-01, T-03
- เสร็จเมื่อ: ระบบตรวจสอบว่าข้อมูลจำเป็นครบถ้วน ประเภทอยู่ใน 5 ประเภทที่มหาวิทยาลัยรับรอง และไม่ใส่ขั้นตอนอนุมัติใหม่เข้ามาใน workflow
- สถานะ: เสร็จ รอทีมตรวจ

### T-05 สร้าง API บันทึกกิจกรรมและเผยแพร่ให้นักศึกษาเห็น
- รองรับ: FR-ACT-05, FR-ACT-06, FR-ACT-07, DOM-ACT-03
- ตรวจด้วย: AC-ACT-05, AC-ACT-06, AC-ACT-07
- ไฟล์ที่แตะ: `backend/app/routes/activity.py`, `backend/app/services/activity_service.py`, `backend/tests/test_activity_create_flow.py`
- ต้องทำหลัง: T-03, T-04
- เสร็จเมื่อ: เมื่อฟอร์มครบและยืนยันแล้ว ระบบบันทึกกิจกรรมเข้าสู่ระบบและกิจกรรมนั้นปรากฏในรายการกิจกรรมที่นักศึกษาเห็นได้ โดยไม่มีกระบวนการอนุมัติใหม่เพิ่มเติม
- สถานะ: เสร็จ รอทีมตรวจ

### T-06 สร้างระบบบันทึกประวัติการแก้ไขกิจกรรม (edit log)
- รองรับ: FR-ACT-08, ASM-ACT-06
- ตรวจด้วย: AC-ACT-08
- ไฟล์ที่แตะ: `backend/app/models/activity_edit_log.py`, `backend/app/services/activity_edit_history.py`, `backend/tests/test_activity_edit_history.py`
- ต้องทำหลัง: T-05
- เสร็จเมื่อ: ทุกครั้งที่ผู้จัดแก้ไขกิจกรรม ระบบบันทึกประวัติการแก้ไขและสามารถแสดงได้ในประวัติกิจกรรม
- สถานะ: เสร็จ รอทีมตรวจ

### T-07 สร้าง流程ยกเลิกกิจกรรมและแจ้งเตือนผู้ที่ลงทะเบียน
- รองรับ: FR-ACT-09, ASM-ACT-06
- ตรวจด้วย: AC-ACT-09
- ไฟล์ที่แตะ: `backend/app/services/activity_cancellation.py`, `backend/app/routes/activity_cancel.py`, `backend/tests/test_activity_cancellation.py`
- ต้องทำหลัง: T-05
- เสร็จเมื่อ: เมื่อยกเลิกกิจกรรม ระบบคงสถานะยกเลิกไว้และส่งแจ้งเตือนไปยังผู้ที่ลงทะเบียนว่ากิจกรรมถูกยกเลิกแล้ว
- สถานะ: พร้อมทำ

### T-08 ทดสอบ NFR รองรับผู้ใช้งาน 5,000 คนต่อภาคการศึกษา
- รองรับ: NFR-ACT-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-09
- ไฟล์ที่แตะ: `backend/tests/test_activity_load.py`, `docs/activity-load-test-plan.md`
- ต้องทำหลัง: T-05
- เสร็จเมื่อ: สคริปต์ทดสอบโหลดแสดงว่าระบบสามารถรองรับผู้ใช้งานประมาณ 5,000 คนต่อภาคการศึกษาได้และไม่ทำให้หน้า “สร้างกิจกรรมใหม่” ล้มเหลวเมื่อมีความต้องการเข้าถึงพร้อมกัน
- สถานะ: พร้อมทำ

### T-09 ตรวจสอบความครบของ AC และ Traceability
- รองรับ: FR-ACT-01, FR-ACT-02, FR-ACT-03, FR-ACT-04, FR-ACT-05, FR-ACT-06, FR-ACT-07, FR-ACT-08, FR-ACT-09, CON-ACT-01, DOM-ACT-01, DOM-ACT-02, DOM-ACT-03, IF-ACT-01, IF-ACT-02, NFR-ACT-01
- ตรวจด้วย: AC-ACT-01, AC-ACT-02, AC-ACT-03, AC-ACT-04, AC-ACT-05, AC-ACT-06, AC-ACT-07, AC-ACT-08, AC-ACT-09
- ไฟล์ที่แตะ: `backend/tests/`, `frontend/tests/`, `specs/004-NewActivity/tasks.md`
- ต้องทำหลัง: T-01, T-02, T-03, T-04, T-05, T-06, T-07, T-08
- เสร็จเมื่อ: test_AC_ACT_01 ถึง test_AC_ACT_09 ผ่าน และตรวจย้อนกลับกับ traceability ใน spec.md ครบถ้วน
- สถานะ: พร้อมทำ

## ตารางตรวจความครบ

### 1) AC ID | task ที่ตรวจ AC นี้

| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC-ACT-01 | T-02 |
| AC-ACT-02 | T-01, T-03 |
| AC-ACT-03 | T-03 |
| AC-ACT-04 | T-03, T-04 |
| AC-ACT-05 | T-01, T-03, T-04, T-05 |
| AC-ACT-06 | T-05 |
| AC-ACT-07 | T-04, T-05 |
| AC-ACT-08 | T-06 |
| AC-ACT-09 | T-07 |

### 2) Constraint ID | task ที่ทำให้เป็นจริง

| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| CON-ACT-01 | T-02 |
| DOM-ACT-01 | T-04 |
| DOM-ACT-02 | T-04 |
| DOM-ACT-03 | T-02, T-04, T-05 |
| IF-ACT-01 | T-03, T-04 |
| IF-ACT-02 | T-01, T-03 |
| NFR-ACT-01 | T-08 |

## สิ่งที่ยังไม่ทำ

- Open Questions ใน spec: ไม่มี
- ไม่มี task ที่ต้องรอ Q-xx เนื่องจาก spec ถูกชี้แจงครบและไม่มีข้อสงสัยที่ต้องถาม
