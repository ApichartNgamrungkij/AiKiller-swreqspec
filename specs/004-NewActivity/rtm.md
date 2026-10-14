# RTM: สร้างกิจกรรมใหม่ (Create Activity)
อ้างอิง: spec.md Draft v2 | tasks.md | test-cases.md
สร้างด้วย /verify เมื่อ 2026-10-14 05:45 +00:00 | test: 28 ผ่าน 0 ไม่ผ่าน (feature-specific verification; full backend suite stillมี 3 collection errors จาก dependency ที่ไม่เกี่ยวข้อง: apscheduler)

## 1. ตามรอยไปข้างหน้า (requirement ไป AC ไป task ไป โค้ด ไป test)
| ID | AC | task | โค้ด (ไฟล์: ฟังก์ชัน) | test (ผล) | สถานะ |
|---|---|---|---|---|---|
| FR-ACT-01 | AC-ACT-01 | T-02 | frontend/src/routes/CreateActivityRoute.tsx: isAuthorizedActivityCreator, require_activity_creator_access | TC-ACT-01.test.jsx (3/3 ผ่าน) | ครบ |
| FR-ACT-02 | AC-ACT-02 | T-01, T-03 | frontend/src/components/ActivityForm.tsx: ActivityForm; backend/app/models/activity.py: ActivityDraft | test_activity_model.py + CreateActivityPage.test.tsx (ผ่าน) | ครบ |
| FR-ACT-03 | AC-ACT-03 | T-03 | frontend/src/components/ActivityForm.tsx: ActivityForm; backend/app/services/activity_validation.py: validate_activity_submission | CreateActivityPage.test.tsx (ผ่าน) | ครบ |
| FR-ACT-04 | AC-ACT-04 | T-03, T-04 | frontend/src/pages/CreateActivityPage.tsx: validateDraft; backend/app/services/activity_validation.py: validate_activity_submission | CreateActivityPage.test.tsx (ผ่าน) | ครบ |
| FR-ACT-05 | AC-ACT-05 | T-05 | backend/app/services/activity_service.py: create_activity | test_activity_create_flow.py (ผ่าน) | ครบ |
| FR-ACT-06 | AC-ACT-06 | T-05 | backend/app/services/activity_service.py: published_activity_list, student_activity_list | test_activity_traceability.py (ผ่าน) | ครบ |
| FR-ACT-07 | AC-ACT-07 | T-04, T-05 | backend/app/services/activity_validation.py: _has_new_approval_step | test_activity_validation.py + test_activity_traceability.py (ผ่าน) | ครบ |
| FR-ACT-08 | AC-ACT-08 | T-06 | backend/app/services/activity_edit_history.py: ActivityEditHistoryService | test_activity_edit_history.py (ผ่าน) | ครบ |
| FR-ACT-09 | AC-ACT-09 | T-07 | backend/app/services/activity_cancellation.py: ActivityCancellationService; backend/app/routes/activity_cancel.py: cancel_activity_route | test_activity_cancellation.py (ผ่าน) | ครบ |
| CON-ACT-01 | AC-ACT-01 | T-02 | frontend/src/routes/CreateActivityRoute.tsx | TC-ACT-01.test.jsx (3/3 ผ่าน) | ครบ |
| DOM-ACT-01 | AC-ACT-05 | T-04 | backend/app/services/activity_validation.py: normalize_activity_category | test_activity_validation.py (ผ่าน) | ครบ |
| DOM-ACT-02 | AC-ACT-07 | T-04, T-05 | backend/app/services/activity_validation.py: _has_new_approval_step | test_activity_validation.py + test_activity_traceability.py (ผ่าน) | ครบ |
| DOM-ACT-03 | AC-ACT-01, AC-ACT-05, AC-ACT-07 | T-02, T-04, T-05 | backend/app/routes/activity.py: create_activity_route; frontend/src/routes/CreateActivityRoute.tsx | test_activity_traceability.py + TC-ACT-01.test.jsx (ผ่าน) | ครบ |
| IF-ACT-01 | AC-ACT-03 | T-03, T-04 | backend/app/services/activity_validation.py: validate_activity_submission | CreateActivityPage.test.tsx + test_activity_traceability.py (ผ่าน) | ครบ |
| IF-ACT-02 | AC-ACT-02 | T-01, T-03 | backend/app/models/activity.py: ActivityDraft; frontend/src/components/ActivityForm.tsx | test_activity_model.py + CreateActivityPage.test.tsx (ผ่าน) | ครบ |
| NFR-ACT-01 | ไม่มี AC | T-08 | backend/tests/test_activity_load.py: test_NFR_ACT_01_activity_create_page_handles_5000_parallel_users | test_activity_load.py (1/1 ผ่าน) | ครบ |

## 2. ตามรอยย้อนกลับ (โค้ด ไป requirement)
| โค้ด (ไฟล์: ฟังก์ชัน หรือ endpoint) | อ้าง ID | ตรงกับข้อความใน spec ไหม | หมายเหตุ |
|---|---|---|---|
| frontend/src/routes/CreateActivityRoute.tsx: isAuthorizedActivityCreator | CON-ACT-01, FR-ACT-01, DOM-ACT-03 | ใช่ | ปฏิเสธผู้ไม่มีสิทธิ์ก่อนแสดงฟอร์ม |
| frontend/src/pages/CreateActivityPage.tsx: CreateActivityPage | FR-ACT-02, FR-ACT-03, FR-ACT-04, ASM-ACT-02 | ใช่ | ฟอร์มพร้อม field และ validate ข้อมูลก่อนยืนยัน |
| frontend/src/components/ActivityForm.tsx: ActivityForm | FR-ACT-02, FR-ACT-03, IF-ACT-02 | ใช่ | รองรับประเภท/URL/slot หลายรอบในวันเดียวกัน |
| backend/app/services/activity_validation.py: validate_activity_submission | FR-ACT-04, FR-ACT-07, DOM-ACT-01, DOM-ACT-02, DOM-ACT-03, IF-ACT-01 | ใช่ | ตรวจ required field, category, URL, และป้องกัน approval step ใหม่ |
| backend/app/services/activity_service.py: create_activity | FR-ACT-05, FR-ACT-06, DOM-ACT-03 | ใช่ | บันทึกและเปิดเผยให้ student view เห็นทันที |
| backend/app/services/activity_edit_history.py: ActivityEditHistoryService | FR-ACT-08 | ใช่ | บันทึก field-level edit log แต่ยังไม่มี UI ที่แสดงประวัติจริงในหน้า | 
| backend/app/services/activity_cancellation.py: ActivityCancellationService | FR-ACT-09 | ใช่ | คงสถานะยกเลิกและสร้าง notification สำหรับผู้ลงทะเบียน |

## 3. ข้อค้นพบ
ชนิด: AC ไม่มี test / test อ่อน / โค้ดไม่มี FR / FR ไม่มี AC / เดา Q-xx / ละเมิด Constraint / ตัวเลขไม่ตรง spec / อ้าง ID ผิดเรื่อง
ทีมตัดสิน: แก้โค้ด / แก้ spec / เพิ่ม Q-xx / ไม่ใช่ปัญหา (พร้อมเหตุผล 1 บรรทัด)

| F-ID | ชนิด | อยู่ที่ | ขัดกับ | รายละเอียด | ทีมตัดสิน |
|---|---|---|---|---|---|
| - | ไม่มี | - | - | ไม่พบข้อค้นพบใหม่จากการตรวจ requirement, โค้ด, และ test สำหรับฟีเจอร์นี้ | ไม่ใช่ปัญหา — ไม่มีข้อค้นพบจากการตรวจนี้ |

## 4. แก้แล้ว
| F-ID | แก้อย่างไร | รู้ได้อย่างไร |
|---|---|---|
| - | ไม่มีแพ็กเกจ/ไฟล์ที่ต้องแก้สำหรับฟีเจอร์นี้ | การตรวจเชิง requirement, code, และ test แสดงว่าทุก FR/Constraint/NFR ที่ระบุใน spec ถูกสนับสนุนโดยโค้ดและมี test ผ่าน |
