# Tasks: ลบ/ระงับกิจกรรม (DeleteActivity)

- Feature: ลบ/ระงับกิจกรรม (DeleteActivity)
- Spec ID: `007-DeleteActivity`
- อ้างอิง: [plan.md](./plan.md)
- วันที่: 2026-10-06

ฟีเจอร์นี้แบ่งเป็น 6 task ตามลำดับสถานะกิจกรรม, การเลือกและยืนยัน, การซ่อนกิจกรรม, Audit Log และตรวจสิทธิ์ของ Admin  
ไม่มี task ที่ต้องรอ Open Question เนื่องจาก spec ไม่มี Open Question ค้างอยู่

## รายการ task

### T-01 สร้างสถานะกิจกรรมและข้อมูลสำหรับการลบ/ระงับ
- รองรับ: FR-DEL-01, FR-DEL-05, IF-HIDE-01, CON-DEL-01, ASM-02, ASM-03
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-02 และ T-04
- ไฟล์ที่แตะ: `backend/app/models/activity.py`, `backend/app/models/activity_audit_log.py`
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: กิจกรรมมีสถานะเผยแพร่และสถานะ hidden/soft-deleted โดยไม่ลบข้อมูลจริง และมีฟิลด์ที่ต้องใช้เก็บเหตุผล เวลา และประเภทการดำเนินการ
- สถานะ: พร้อมทำ

### T-02 สร้างรายการกิจกรรม Admin และเลือกลบ/ระงับ
- รองรับ: FR-DEL-01, FR-DEL-02, IF-ADMIN-01, CON-DEL-01
- ตรวจด้วย: AC-DEL-01
- ไฟล์ที่แตะ: `backend/app/api/admin_activity.py`, `frontend/src/pages/AdminActivityPage.tsx`, `frontend/src/components/ActivityActionMenu.tsx`
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: Admin เปิดรายการกิจกรรมที่เผยแพร่แล้วและสามารถเลือก “ลบ” หรือ “ระงับ” ได้เฉพาะกิจกรรมที่มีสถานะเปิดเผย
- สถานะ: พร้อมทำ

### T-03 ป้องกันการยืนยันโดยไม่มีเหตุผลและตรวจสอบการยืนยัน
- รองรับ: FR-DEL-03, FR-DEL-04, IF-REASON-01, IF-ADMIN-01, ASM-01
- ตรวจด้วย: AC-DEL-02, AC-DEL-03
- ไฟล์ที่แตะ: `backend/app/api/admin_activity.py`, `frontend/src/components/ConfirmDeleteDialog.tsx`
- ต้องทำหลัง: T-02
- เสร็จเมื่อ: ฟอร์มยืนยันบังคับให้ Admin ระบุเหตุผลก่อนกดยืนยัน และแสดงข้อความเมื่อไม่มีเหตุผล
- สถานะ: พร้อมทำ

### T-04 สร้าง API ลบ/ระงับกิจกรรมและซ่อนจากนักศึกษา
- รองรับ: FR-DEL-05, FR-DEL-06, IF-HIDE-01, IF-ADMIN-01, ACC-AUDIT-01, NFR-DEL-01, ASM-02, ASM-03
- ตรวจด้วย: AC-DEL-04, AC-DEL-05
- ไฟล์ที่แตะ: `backend/app/services/activity_delete_service.py`, `backend/app/api/admin_activity.py`, `backend/app/services/activity_visibility_service.py`
- ต้องทำหลัง: T-01, T-03
- เสร็จเมื่อ: การยืนยันสำเร็จเปลี่ยนสถานะกิจกรรมเป็น hidden/soft-deleted และ API สำหรับรายการนักศึกษาตัดกิจกรรมที่ถูกระงับออกแล้ว
- สถานะ: พร้อมทำ

### T-05 บันทึก Audit Log สำหรับการลบ/ระงับ
- รองรับ: FR-DEL-06, NFR-DEL-03, ACC-AUDIT-01, ACC-ADMIN-01, IF-ADMIN-01
- ตรวจด้วย: AC-DEL-05
- ไฟล์ที่แตะ: `backend/app/models/activity_audit_log.py`, `backend/app/services/activity_audit_log_service.py`, `backend/app/api/admin_activity.py`
- ต้องทำหลัง: T-04
- เสร็จเมื่อ: ระบบบันทึก admin_id, action_type, reason, created_at ให้ครบถ้วน และ Admin สามารถเรียกดูประวัติย้อนหลังได้
- สถานะ: พร้อมทำ

### T-06 ป้องกันการใช้งานโดยผู้ไม่มีสิทธิ์ Admin และทดสอบความปลอดภัย
- รองรับ: FR-DEL-07, NFR-DEL-01, NFR-DEL-02, ACC-ADMIN-01, IF-ADMIN-01
- ตรวจด้วย: AC-DEL-06
- ไฟล์ที่แตะ: `backend/app/services/access_control.py`, `backend/tests/api/test_delete_activity_access.py`
- ต้องทำหลัง: T-04, T-05
- เสร็จเมื่อ: ผู้ใช้งานที่ไม่ใช่ Admin ถูกปฏิเสธโดยตรงทั้งก่อนเปิดฟอร์มและก่อนยืนยันการลบ/ระงับ และการเรียก API ถูกส่งผ่าน HTTPS เท่านั้น
- สถานะ: พร้อมทำ

## ตารางตรวจความครบของ Acceptance Criteria

| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC-DEL-01 | T-02 |
| AC-DEL-02 | T-03 |
| AC-DEL-03 | T-03 |
| AC-DEL-04 | T-04 |
| AC-DEL-05 | T-04, T-05 |
| AC-DEL-06 | T-06 |

## ตารางตรวจความครบของ Constraints

| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| IF-ADMIN-01 | T-02, T-03, T-04, T-06 |
| IF-DEL-01 | T-02, T-04 |
| IF-REASON-01 | T-03 |
| IF-HIDE-01 | T-01, T-04 |
| ACC-AUDIT-01 | T-04, T-05 |
| ACC-ADMIN-01 | T-06 |
| CON-DEL-01 | T-01, T-02, T-04 |
| NFR-DEL-01 | T-04, T-06 |
| NFR-DEL-02 | T-06 |
| NFR-DEL-03 | T-05 |

## สิ่งที่ยังไม่ทำ

Spec ปัจจุบันไม่มี Open Question ค้างอยู่ โดย ASM-01 ถึง ASM-04 ระบุความหมายของการลบ/ระงับ สิทธิ์ของ Admin และแผน soft delete ไว้ชัดแล้ว จึงไม่มี task ที่มีสถานะ “รอ Q-xx”

งานต่อไปนี้ยังไม่สร้างเพราะอยู่ใน Out of Scope: การสร้างกิจกรรมใหม่, การแก้ไขรายละเอียดกิจกรรม, การอนุมัติกิจกรรม, การลงทะเบียนกิจกรรม, และการจัดการข้อมูลการลงทะเบียนของนักศึกษา
