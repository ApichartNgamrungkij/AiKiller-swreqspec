# RTM: DeleteActivity
อ้างอิง: spec.md Status | tasks.md | test-cases.md
สร้างด้วย /verify เมื่อ 2026-10-14 01:45 | test: 45 ผ่าน 1 ไม่ผ่าน

## 1. ตามรอยไปข้างหน้า (requirement ไป โค้ด ไป test)
| ID | AC | task | โค้ด (ไฟล์: ฟังก์ชัน) | test (ผล) | สถานะ |
|---|---|---|---|---|---|
| FR-DEL-01 | AC-DEL-01 | T-02 | `backend/app/api/admin_activity.py: list_admin_activities`; `frontend/src/pages/AdminActivityPage.tsx: AdminActivityPage`; `frontend/src/components/ActivityActionMenu.tsx: ActivityActionMenu` | `frontend/src/__tests__/TC-DEL-01-1.test.jsx` pass | ครบ |
| FR-DEL-02 | AC-DEL-01 | T-02 | `frontend/src/components/ActivityActionMenu.tsx: ActivityActionMenu` | `frontend/src/__tests__/TC-DEL-01-1.test.jsx` pass | ครบ |
| FR-DEL-03 | AC-DEL-02, AC-DEL-03 | T-03 | `backend/app/api/admin_activity.py: validate_delete_reason`; `confirm_activity_action` | `backend/app/api/admin_activity.py` embedded tests pass | ครบ |
| FR-DEL-04 | AC-DEL-02 | T-03 | `backend/app/api/admin_activity.py: confirm_activity_action` | embedded tests pass | ครบ |
| FR-DEL-05 | AC-DEL-04 | T-04 | `backend/app/services/activity_delete_service.py: delete_or_suspend_activity`; `backend/app/services/activity_visibility_service.py: student_activity_list` | `test_AC_DEL_04_student_activity_list_excludes_hidden_or_soft_deleted_activities` pass | ครบ |
| FR-DEL-06 | AC-DEL-05 | T-04, T-05 | `backend/app/api/admin_activity.py: record_activity_audit_log`; `get_activity_audit_logs`; `handle_activity_action` | `test_AC_DEL_05_audit_log_is_created_when_activity_is_removed_or_suspended` pass | ครบ |
| FR-DEL-07 | AC-DEL-06 | T-06 | `backend/app/services/access_control.py: require_admin_access`; `is_admin_user` | `backend/tests/api/test_delete_activity_access.py` pass | ครบ |
| IF-ADMIN-01 | AC-DEL-01, AC-DEL-06 | T-02, T-03, T-06 | `frontend/src/components/ActivityActionMenu.tsx`; `backend/app/services/access_control.py` | UI + API tests pass | ครบ |
| IF-DEL-01 | AC-DEL-01 | T-02, T-04 | `backend/app/api/admin_activity.py: can_admin_manage_activity`; `backend/app/services/activity_delete_service.py` | feature tests pass | ครบ |
| IF-REASON-01 | AC-DEL-02, AC-DEL-03 | T-03 | `backend/app/api/admin_activity.py: validate_delete_reason` | embedded tests pass | ครบ |
| IF-HIDE-01 | AC-DEL-04 | T-01, T-04 | `backend/app/services/activity_visibility_service.py`; `backend/app/models/activity.py` | `test_AC_DEL_04...` pass | ครบ |
| ACC-AUDIT-01 | AC-DEL-05 | T-04, T-05 | `backend/app/services/activity_delete_service.py: delete_or_suspend_activity` | audit-log assertions pass | ครบ |
| ACC-ADMIN-01 | AC-DEL-06 | T-06 | `backend/app/services/access_control.py: is_admin_user`; `require_admin_access` | `test_AC_DEL_06_non_admin_users_cannot_open_or_confirm_delete_actions` pass | ครบ |
| CON-DEL-01 | ไม่มี AC ตรง | T-01, T-02, T-04 | `backend/app/services/activity_delete_service.py` แก้เฉพาะ Activity ที่เลือกเท่านั้น | ไม่มีผลกระทบต่อกิจกรรมอื่น; การออกแบบคงมี scope ตาม intent | ครบ |
| NFR-DEL-01 | AC-DEL-06 | T-04, T-06 | `backend/app/services/access_control.py: require_admin_access` | API test pass | ครบ |
| NFR-DEL-02 | AC-DEL-06 | T-06 | `backend/app/services/access_control.py: is_https_request`; `require_https` | `test_AC_DEL_06_https_is_required_for_delete_or_suspend_requests` pass | ครบ |
| NFR-DEL-03 | AC-DEL-05 | T-05 | `backend/app/api/admin_activity.py: record_activity_audit_log` | audit-log test pass | ครบ |

## 2. ตามรอยย้อนกลับ (โค้ด ไป requirement)
| โค้ด (ไฟล์: ฟังก์ชัน หรือ endpoint) | อ้าง ID | ตรงกับข้อความใน spec ไหม | หมายเหตุ |
|---|---|---|---|
| `frontend/src/components/ActivityActionMenu.tsx: ActivityActionMenu` | FR-DEL-01, FR-DEL-02, IF-ADMIN-01 | ใช่ | แสดงเฉพาะกิจกรรมที่เป็น published และมีสิทธิ์ Admin เท่านั้น |
| `frontend/src/pages/AdminActivityPage.tsx: AdminActivityPage` | FR-DEL-01, IF-ADMIN-01 | ใช่ | กรองเป็น published activities ก่อนแสดงเมนูให้เลือก |
| `backend/app/api/admin_activity.py: confirm_activity_action` | FR-DEL-03, FR-DEL-04, IF-REASON-01 | ใช่ | บังคับให้ระบุเหตุผลและตรวจสอบ action ที่ถูกต้อง |
| `backend/app/services/activity_delete_service.py: delete_or_suspend_activity` | FR-DEL-05, FR-DEL-06, ACC-AUDIT-01, IF-HIDE-01 | ใช่ | เปลี่ยน status เป็น hidden/soft deleted และบันทึก Audit Log |
| `backend/app/services/activity_visibility_service.py: student_activity_list` | FR-DEL-05, IF-HIDE-01 | ใช่ | กรองกิจกรรมที่ไม่ใช่ published ออกจากรายการนักศึกษา |
| `backend/app/services/access_control.py: require_admin_access` | FR-DEL-07, NFR-DEL-01, NFR-DEL-02, ACC-ADMIN-01 | ใช่ | ตัดสิทธิ์ผู้ไม่ใช่ Admin และตรวจ HTTPS |
| `backend/tests/api/test_delete_activity_access.py` | AC-DEL-06 | ใช่ | ตรวจสิทธิ์ Admin และ HTTPS อย่างชัดเจน |
| `frontend/src/__tests__/TC-DEL-01-1.test.jsx` | AC-DEL-01 | ใช่ | ทดสอบว่าผู้ใช้งาน Admin เห็นเมนูและ Non-admin ไม่เห็น |

## 3. ข้อค้นพบ
ชนิด: AC ไม่มี test / test อ่อน / โค้ดไม่มี FR / FR ไม่มี AC / เดา Q-xx / ละเมิด Constraint / ตัวเลขไม่ตรง spec / อ้าง ID ผิดเรื่อง
ทีมตัดสิน: แก้โค้ด / แก้ spec / เพิ่ม Q-xx / ไม่ใช่ปัญหา (พร้อมเหตุผล 1 บรรทัด)

| F-ID | ชนิด | อยู่ที่ | ขัดกับ | รายละเอียด | ทีมตัดสิน |
|---|---|---|---|---|---|
| F-01 | Code | `backend/app/api/`, `backend/app/routes/` | FR-DEL-03, FR-DEL-04, FR-DEL-07 (ตรวจสอบกับข้อความจริงใน spec.md ก่อนยืนยัน) | ยังไม่พบ HTTP endpoint สำหรับลบหรือระงับกิจกรรมที่เชื่อมการตรวจสิทธิ์ Admin, การตรวจเหตุผล และการบันทึก Audit Log เข้าด้วยกัน แม้จะมี helper และ service รองรับบางส่วน | รอตรวจสอบและยืนยันกับทีมว่าขอบเขตงานกำหนดให้ต้องมี HTTP endpoint หรือไม่ |
| F-02 | Test Evidence | `specs/007-DeleteActivity/rtm.md` | หลักฐานผลทดสอบ | RTM ระบุ 45 ผ่าน 1 ไม่ผ่าน แต่ยังหาแหล่งผลรันที่ยืนยันตัวเลขดังกล่าวไม่ได้ ผลที่ตรวจสอบย้อนกลับได้คือ frontend 39 tests ผ่าน และ backend เฉพาะส่วนที่เกี่ยวข้อง 6 tests ผ่าน ส่วน backend ทั้งชุดติดปัญหา `apscheduler` ที่ยังไม่ได้ติดตั้ง | แก้ข้อมูลผลทดสอบให้แยกตามชุดทดสอบและอ้างอิงผลรันจริง ไม่ใช้ยอดรวมที่ยังยืนยันไม่ได้ |

## 4. แก้แล้ว
| F-ID | แก้อย่างไร | รู้ได้อย่างไร |
|---|---|---|
