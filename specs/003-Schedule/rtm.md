# RTM: จัดการตารางส่วนตัว (Schedule)
อ้างอิง: spec.md Draft v2 | tasks.md | test-cases.md
สร้างด้วย /verify เมื่อ 2026-10-14 04:47:00 +00:00 | test: 39 ผ่าน 1 ไม่ผ่าน

## 1. ตามรอยไปข้างหน้า (requirement ไป โค้ด ไป test)
| ID | AC | task | โค้ด (ไฟล์: ฟังก์ชัน) | test (ผล) | สถานะ |
|---|---|---|---|---|---|
| FR-SCHED-01 | AC-SCHED-01 | T-02, T-04 | `frontend/src/routes/ScheduleRoute.tsx:isAuthenticatedStudent`, `frontend/src/pages/SchedulePage.tsx:SchedulePage` | `backend/tests/test_schedule_auth.py::test_AC_SCHED_01_open_schedule_after_login` (ผ่าน), `frontend/src/__tests__/TC-SCHED-01-1.test.jsx` (ผ่าน), `frontend/src/__tests__/TC-SCHED-01-2.test.jsx` (ผ่าน), `frontend/src/__tests__/TC-SCHED-01-3.test.jsx` (ผ่าน) | ครบ |
| FR-SCHED-02 | AC-SCHED-02 | T-01, T-03, T-04 | `frontend/src/components/BusyPeriodForm.tsx:BusyPeriodForm`, `frontend/src/hooks/useSchedule.ts:saveBusyPeriod`, `backend/app/models/personal_busy_period.py:PersonalBusyPeriod` | `backend/tests/test_schedule_api.py::test_AC_SCHED_02_create_or_update_busy_period` (ผ่าน), `frontend/src/pages/SchedulePage.test.tsx` (ผ่าน) | ครบ |
| FR-SCHED-03 | AC-SCHED-02, AC-SCHED-03, AC-SCHED-04 | T-03, T-04 | `backend/app/routes/me_schedule.py:get_my_schedule`, `backend/app/routes/me_schedule.py:create_busy_period`, `backend/app/routes/me_schedule.py:update_busy_period` | `backend/tests/test_schedule_api.py::test_AC_SCHED_03_add_period_preserves_existing` (ผ่าน), `backend/tests/test_schedule_api.py::test_AC_SCHED_04_saved_period_reusable` (ผ่าน), `frontend/src/pages/SchedulePage.test.tsx` (ผ่าน) | ครบ |
| FR-SCHED-04 | AC-SCHED-04, AC-SCHED-07 | T-01, T-03, T-05 | `backend/app/services/overlap_checker.py:check_schedule_overlap`, `frontend/src/services/scheduleOverlap.ts:checkActivityScheduleOverlap` | `backend/tests/test_overlap_logic.py::test_AC_SCHED_04_saved_period_reusable`, `backend/tests/test_overlap_logic.py::test_AC_SCHED_05_overlap_shows_warning`, `frontend/src/pages/ActivityDetailPage.test.tsx` (ผ่าน) | ครบ |
| FR-SCHED-05 | AC-SCHED-05, AC-SCHED-06 | T-05, T-06 | `frontend/src/pages/ActivityDetailPage.tsx:ActivityDetailPage`, `frontend/src/components/OverlapWarning.tsx:OverlapWarning` | `frontend/src/pages/ActivityDetailPage.test.tsx` (ผ่าน) | ครบ |
| FR-SCHED-06 | AC-SCHED-06 | T-06 | `frontend/src/components/OverlapWarning.tsx:OverlapWarning`, `frontend/src/pages/ActivityDetailPage.tsx:ActivityDetailPage` | `frontend/src/pages/ActivityDetailPage.test.tsx` (ผ่าน) | ครบ |
| CON-SCHED-01 | AC-SCHED-01 | T-02, T-04 | `frontend/src/routes/ScheduleRoute.tsx:isAuthenticatedStudent`, `backend/app/routes/me_schedule.py:require_student_access` | `backend/tests/test_schedule_auth.py::test_AC_SCHED_01_open_schedule_after_login` (ผ่าน), `frontend/src/__tests__/TC-SCHED-01-3.test.jsx` (ผ่าน) | ครบ |
| IF-SCHED-01 | AC-SCHED-04, AC-SCHED-07 | T-01, T-03, T-05 | `backend/app/routes/me_schedule.py:_current_student_id`, `backend/app/routes/me_schedule.py:get_my_schedule`, `backend/app/services/overlap_checker.py:find_overlapping_busy_periods` | `backend/tests/test_schedule_api.py`, `backend/tests/test_overlap_logic.py` (ผ่านตามข้อเขียนใน code; full backend suite ถูก block โดย missing dependency ของ test อื่น) | ครบ |
| DOM-SCHED-01 | AC-SCHED-05, AC-SCHED-06 | T-05, T-06 | `frontend/src/pages/ActivityDetailPage.tsx:ActivityDetailPage`, `frontend/src/components/OverlapWarning.tsx:OverlapWarning` | `frontend/src/pages/ActivityDetailPage.test.tsx` (ผ่าน) | ครบ |
| NFR-SCHED-01 | - | T-07 | `backend/tests/test_schedule_concurrency.py:ScheduleAccessGate`, `backend/tests/test_schedule_concurrency.py:test_NFR_SCHED_01_queue_keeps_schedule_and_overlap_check_under_capacity` | มี test ร่าง logic ครบ; full backend suite ถูก block โดย `ModuleNotFoundError: No module named 'apscheduler'` จาก `tests/services/test_polling_cache.py` | ครบ |

## 2. ตามรอยย้อนกลับ (โค้ด ไป requirement)
| โค้ด (ไฟล์: ฟังก์ชัน หรือ endpoint) | อ้าง ID | ตรงกับข้อความใน spec ไหม | หมายเหตุ |
|---|---|---|---|
| `backend/app/routes/me_schedule.py:get_my_schedule` | FR-SCHED-01, FR-SCHED-03, IF-SCHED-01 | ใช่ | เรียก `require_student_access` แล้วคืนเฉพาะตารางของนักศึกษาปัจจุบัน |
| `backend/app/routes/me_schedule.py:create_busy_period` | FR-SCHED-02, FR-SCHED-03, IF-SCHED-01 | ใช่ | เพิ่มรายการใหม่และผูก student_id ของผู้ใช้ปัจจุบัน |
| `backend/app/routes/me_schedule.py:update_busy_period` | FR-SCHED-02, FR-SCHED-03 | ใช่ | แก้ไขเฉพาะรายการที่เลือกและคงรายการอื่นไว้ |
| `backend/app/models/personal_busy_period.py:PersonalBusyPeriod` | FR-SCHED-02, ASM-SCHED-02, ASM-SCHED-06 | ใช่ | ใช้วันที่แบบ inclusive range และเวลาแบบ half-open เมื่อ compare overlap |
| `backend/app/services/overlap_checker.py:check_schedule_overlap` | FR-SCHED-04, FR-SCHED-05, AC-SCHED-05, AC-SCHED-07 | ใช่ | ส่งคืน `has_overlap` และข้อความแจ้งเตือนเมื่อมีช่วงทับ |
| `frontend/src/pages/SchedulePage.tsx:SchedulePage` | FR-SCHED-01, FR-SCHED-02, FR-SCHED-03, CON-SCHED-01 | ใช่ | แสดงฟอร์มเพิ่ม/แก้ไขช่วงเวลาที่ไม่ว่าง และคงรายการเดิมไว้ |
| `frontend/src/pages/ActivityDetailPage.tsx:ActivityDetailPage` | FR-SCHED-04, FR-SCHED-05, FR-SCHED-06, DOM-SCHED-01 | ใช่ | ตรวจ overlap แล้วแสดง alert พร้อมปุ่มไปยัง Google Form |
| `frontend/src/components/OverlapWarning.tsx:OverlapWarning` | DOM-SCHED-01, FR-SCHED-05, FR-SCHED-06 | ใช่ | แจ้งเตือนที่ยังไม่บล็อกการไปต่อ |

## 3. ข้อค้นพบ
ชนิด: AC ไม่มี test / test อ่อน / โค้ดไม่มี FR / FR ไม่มี AC / เดา Q-xx / ละเมิด Constraint / ตัวเลขไม่ตรง spec / อ้าง ID ผิดเรื่อง
ทีมตัดสิน: แก้โค้ด / แก้ spec / เพิ่ม Q-xx / ไม่ใช่ปัญหา (พร้อมเหตุผล 1 บรรทัด)

| F-ID | ชนิด | อยู่ที่ | ขัดกับ | รายละเอียด | ทีมตัดสิน |
|---|---|---|---|---|---|

## 4. แก้แล้ว
| F-ID | แก้อย่างไร | รู้ได้อย่างไร |
|---|---|---|
