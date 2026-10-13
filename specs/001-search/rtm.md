# RTM: ค้นหาและดูกิจกรรม (Search)
อ้างอิง: spec.md `Draft v2` | tasks.md | test-cases.md
สร้างด้วย `/verify` เมื่อ 2026-10-13 16:55 | test: 30 ผ่าน, backend เก็บ test ไม่สำเร็จ 11 errors

## 1. ตามรอยไปข้างหน้า (requirement ไป โค้ด ไป test)
| ID | AC | task | โค้ด (ไฟล์: ฟังก์ชัน) | test (ผล) | สถานะ |
|---|---|---|---|---|---|
| FR-SRCH-01 | AC-SRCH-01, AC-SRCH-06, AC-SRCH-07 | T-03, T-08, T-09 | `backend/app/services/activity_service.py:filter_activities_for_role`, `backend/app/api/activities.py:list_activities`, `frontend/src/pages/SearchList.tsx:SearchList`, `frontend/src/components/ActivityCard.tsx:ActivityCard`, `frontend/src/hooks/useActivityStatus.ts:useActivityStatus` | frontend tests ของ AC-SRCH-01 ผ่าน; backend tests ที่เกี่ยวข้องยืนยันผลไม่ได้เพราะ pytest collection error | ช่องโหว่ |
| FR-SRCH-02 | AC-SRCH-02, AC-SRCH-03 | T-04, T-07 | `frontend/src/services/activityFilter.ts:filterActivities`, `frontend/src/components/ActivityFilters.tsx:ActivityFilters`, `backend/app/services/collision_service.py:get_collision_status` | frontend tests ของ AC-SRCH-02 และ AC-SRCH-03 ผ่าน; backend test ยืนยันผลไม่ได้เพราะ pytest collection error | ช่องโหว่ |
| FR-SRCH-03 | AC-SRCH-02, AC-SRCH-03 | T-04, T-07, T-08 | `backend/app/api/activities.py:search_activities`, `frontend/src/services/activityFilter.ts:filterActivities`, `frontend/src/components/ActivityResults.tsx:ActivityResults` | frontend tests ของ AC-SRCH-02 และ AC-SRCH-03 ผ่าน; backend test ยืนยันผลไม่ได้เพราะ pytest collection error | ช่องโหว่ |
| FR-SRCH-04 | AC-SRCH-05 | T-05 | `frontend/src/components/ActivityResults.tsx:ActivityResults`, `frontend/src/components/EmptyActivityState.tsx:EmptyActivityState` | `test_AC_SRCH_05_no_result_message` ผ่าน | ครบ |
| FR-SRCH-05 | AC-SRCH-04 | T-06, T-08 | `frontend/src/pages/ActivityDetail.tsx:ActivityDetailPage`, `frontend/src/components/ActivityDetail.tsx:ActivityDetail`, `backend/app/api/activities.py:get_activity_detail` | `test_AC_SRCH_04_detail_view_shows_required_fields` ผ่าน | ช่องโหว่ |
| NFR-01 (รองรับ ~5,000 คน/ภาคการศึกษา) | AC-SRCH-08 | T-10 | `backend/tests/performance/test_activity_search.py:test_AC_SRCH_08_activity_search_benchmark_under_two_seconds` | test ไม่ได้ถูกรันเนื่องจาก pytest collection error | ช่องโหว่ |
| NFR (เตรียมข้อมูลส่ง REG ภายใน 1 วันทำการ) | ไม่มี AC | T-11 | `deployment/https-config.yml:system_integrations.reg` | ไม่มี test ของ Search | ช่องโหว่ |
| NFR (HTTPS) | ไม่มี AC | T-11 | `deployment/https-config.yml:search_api` | ไม่มี test runtime/deployment | ช่องโหว่ |
| NFR (Audit Log) | ไม่มี AC | T-11 | `deployment/https-config.yml:system_integrations.audit_log` | ไม่มี test ของ Search | ช่องโหว่ |
| IF (ใช้เฉพาะตารางส่วนตัวที่นักศึกษากรอกเอง) | AC-SRCH-03 | T-01, T-02, T-07 | `backend/app/routes/me_schedule.py:get_my_schedule`, `backend/app/api/student_schedules.py:get_student_schedule`, `backend/app/services/collision_service.py:get_collision_status` | มี test แต่ยืนยันผลการรันไม่ได้เพราะ pytest collection error | ครบ |
| IF (poll Google Sheets ทุก 1–2 นาที) | AC-SRCH-07 | T-09 | `backend/app/jobs/status_polling.py:ActivityStatusPolling`, `backend/app/integrations/google_sheets.py:GoogleSheetsClient` | มี test แต่ยืนยันผลการรันไม่ได้เพราะ pytest collection error | ช่องโหว่ |
| IF (อัปเดตสถานะภายใน 1 นาทีและไม่เกิน 2 นาที) | AC-SRCH-07 | T-09 | `backend/app/services/activity_status_sync.py:ActivityStatusSynchronizer`, `frontend/src/hooks/useActivityStatus.ts:useActivityStatus` | `test_AC_SRCH_07_status_updates_within_1_minute` ผ่านเมื่อรันแบบมี import path แต่ไม่ตรวจขอบเขต 2 นาที | ช่องโหว่ |
| DOM (เฉพาะ 5 ประเภทที่รับรอง) | AC-SRCH-02 | T-01, T-02, T-04 | `frontend/src/services/activityFilter.ts:ACTIVITY_CATEGORIES`, `backend/app/models/activity.py:ActivityCategory.normalize` | `test_AC_SRCH_02_filter_by_category` ผ่าน | ครบ |
| IF (ชนต้องเตือนสีแดงและไม่ block รายละเอียด) | AC-SRCH-03 | T-07 | `backend/app/services/collision_service.py:get_collision_status`, `frontend/src/components/CollisionWarning.tsx:CollisionWarning`, `frontend/src/components/StudentScheduleWarning.tsx:StudentScheduleWarning` | frontend test ผ่าน; backend test มีอยู่แต่ยืนยันผลการรันไม่ได้เพราะ pytest collection error | ครบ |
| IF (รองรับ ~5,000 คนและตอบสนองภายใน 2 วินาที) | AC-SRCH-08 | T-10 | `backend/app/api/activities.py:search_activities`, `backend/tests/performance/test_activity_search.py:test_AC_SRCH_08_activity_search_benchmark_under_two_seconds` | ไม่สามารถยืนยันผล backend เพราะ collection error | ช่องโหว่ |

### สถานะ Acceptance Criteria
| ID | task | test | สถานะ |
|---|---|---|---|
| AC-SRCH-01 | T-03 เสร็จ | 3 tests ผ่าน แต่ test ใหม่ไม่ยืนยันความสัมพันธ์ระหว่างกิจกรรมกับ badge และไม่มี test กรณีรายการว่าง | ช่องโหว่ |
| AC-SRCH-02 | T-04 เสร็จ | 2 tests ผ่าน ครอบคลุม category และ availability ใน service | ครบ |
| AC-SRCH-03 | T-07 เสร็จ | frontend/backend tests ผ่านเมื่อมี import path; ครอบคลุม warning และการไปต่อ | ครบ |
| AC-SRCH-04 | T-06 เสร็จ | test ผ่าน แต่ไม่ได้ assert ระยะเวลาเริ่ม-สิ้นสุดโดยตรง | ช่องโหว่ |
| AC-SRCH-05 | T-05 เสร็จ | `test_AC_SRCH_05_no_result_message` ผ่าน | ครบ |
| AC-SRCH-06 | T-08 เสร็จ | ไม่มี test ที่ตรวจว่ากิจกรรมใหม่แสดงทันทีโดยไม่รอ Admin | ช่องโหว่ |
| AC-SRCH-07 | T-09 เสร็จ | test ตรวจการเปลี่ยนเป็น full ที่ 60 วินาที แต่ไม่ตรวจไม่เกิน 120 วินาที | ช่องโหว่ |
| AC-SRCH-08 | T-10 เสร็จ | benchmark มีอยู่แต่ backend รันไม่ได้ และไม่มี test มือถือ/ไอแพดหรือ horizontal scroll | ช่องโหว่ |

## 2. ตามรอยย้อนกลับ (โค้ด ไป requirement)
| โค้ด (ไฟล์: ฟังก์ชัน หรือ endpoint) | อ้าง ID | ตรงกับข้อความใน spec ไหม | หมายเหตุ |
|---|---|---|---|
| `backend/app/api/activities.py:list_activities`, `search_activities` | FR-SRCH-01, FR-SRCH-02, FR-SRCH-03 | ไม่ครบ | กรองสถานะ `PUBLISHED` และ category ได้ แต่ไม่กรองกิจกรรมที่ว่างตาม `registration_status`, `capacity` หรือ `booked_slots` และไม่รับช่วงเวลาว่าง |
| `backend/app/services/activity_service.py:filter_activities_for_role` | FR-SRCH-01, FR-SRCH-02, FR-SRCH-03 | ไม่ครบ | บทบาท organizer/admin ถูกคืนเป็นรายการ published ทั้งหมด ไม่ได้ใช้ขอบเขต “กิจกรรมของตัวเอง” ตาม Scope |
| `frontend/src/pages/SearchList.tsx:SearchList` | FR-SRCH-01, FR-SRCH-03 | ไม่ครบ | หน้าแสดงผลจาก API แต่ไม่มี `ActivityFilters`, ไม่มีการกรอง และไม่มี `ActivityResults`/empty state เชื่อมอยู่ในหน้านี้ |
| `frontend/src/services/activityFilter.ts:filterActivities` | FR-SRCH-02, FR-SRCH-03, DOM | ตรงบางส่วน | กรอง category และช่วงเวลาว่างจาก schedule จำลองได้ แต่ไม่ได้ถูกเรียกจาก `SearchList` |
| `frontend/src/pages/ActivityDetail.tsx:ActivityDetailPage`, `frontend/src/components/ActivityDetail.tsx:ActivityDetail` | FR-SRCH-05, ASM-02 | ตรงบางส่วน | แสดงชั่วโมง วันเวลา สถานที่ และลิงก์ Google Form ตาม spec |
| `backend/app/services/collision_service.py:get_collision_status` | FR-SRCH-02, FR-SRCH-03, IF | ตรง | คืนกิจกรรมพร้อม warning สีแดงและช่วงเวลาที่ทับกัน ไม่ตัดกิจกรรมออก |
| `backend/app/jobs/status_polling.py:ActivityStatusPolling`, `backend/app/services/activity_status_sync.py:ActivityStatusSynchronizer` | FR-SRCH-01, IF | ตรงบางส่วน | ช่วง polling อยู่ใน 60–120 วินาทีและคำนวณสถานะ full/open ได้ แต่ไม่ได้พิสูจน์ SLA จริงจากเวลาข้อมูล Google Sheets เปลี่ยน |
| `frontend/src/components/RegistrationFormEmbed.tsx:RegistrationFormEmbed` | ไม่มี FR ของ Search / Out of Scope | ไม่ตรง | สร้างพื้นที่ Google Form จำลองและข้อความให้กรอกข้อมูลลงทะเบียน ซึ่งเกินการ “แสดงลิงก์เพื่อส่งต่อ” และแตะกระบวนการลงทะเบียนที่อยู่ใน Out of Scope |

## 3. ข้อค้นพบ
ชนิด: AC ไม่มี test / test อ่อน / โค้ดไม่มี FR / FR ไม่มี AC / เดา Q-xx / ละเมิด Constraint / ตัวเลขไม่ตรง spec / อ้าง ID ผิดเรื่อง
ทีมตัดสิน: แก้โค้ด / แก้ spec / เพิ่ม Q-xx / ไม่ใช่ปัญหา (พร้อมเหตุผล 1 บรรทัด)

| F-ID | ชนิด | อยู่ที่ | ขัดกับ | รายละเอียด | ทีมตัดสิน |
|---|---|---|---|---|---|
| F-01 | ละเมิด Constraint / โค้ดไม่มี FR | `backend/app/api/activities.py:list_activities`, `backend/app/services/activity_service.py:filter_activities_for_role` | FR-SRCH-01, Scope นักศึกษา/ผู้ดูแล | รายการกรองเพียง `PUBLISHED`; ไม่มีเงื่อนไขว่างสำหรับนักศึกษา และบทบาทผู้ดูแลไม่ได้จำกัดเป็นกิจกรรมของตนเอง | เพิ่ม Q-xx |
| F-02 | โค้ดไม่มี FR / test อ่อน | `frontend/src/pages/SearchList.tsx:SearchList` | FR-SRCH-02, FR-SRCH-03 | มีตัวกรองใน service แต่หน้า Search ไม่แสดงหรือเรียกตัวกรอง จึงไม่ครบ flow ที่ผู้ใช้เลือกกรองและเห็นผลลัพธ์ | แก้โค้ด |
| F-03 | AC ไม่มี test | `frontend/src/services/activityApi.ts:fetchActivities`, `frontend/src/pages/SearchList.tsx:SearchList` | AC-SRCH-06 | task T-08 ระบุว่ากิจกรรมใหม่ต้องแสดงทันทีโดยไม่รอ Admin แต่ไม่มี test ที่ตรวจเงื่อนไขนี้ | แก้โค้ด |
| F-04 | test อ่อน | `frontend/src/pages/SearchList.test.tsx`, `frontend/src/pages/ActivityDetail.test.tsx` | AC-SRCH-01, AC-SRCH-04 | AC-SRCH-01 ตรวจเพียงว่ามีชื่อและ badge อยู่ แต่ไม่ตรวจ badge ต่อกิจกรรม; AC-SRCH-04 ไม่ assert ระยะเวลาเริ่ม-สิ้นสุดโดยตรง | แก้โค้ด |
| F-05 | test อ่อน | `frontend/src/hooks/useActivityStatus.test.ts`, `backend/tests/test_activity_status_sync.py` | AC-SRCH-07, IF status SLA | ทดสอบที่ 60 วินาที แต่ไม่ทดสอบขอบบน 120 วินาทีหรือเวลาจริงตั้งแต่ Google Sheets อัปเดต | แก้โค้ด |
| F-06 | AC ไม่มี test / test อ่อน | `backend/tests/performance/test_activity_search.py`, frontend responsive surface | AC-SRCH-08, NFR-01 | backend test เก็บไม่ได้จาก import error ในคำสั่งมาตรฐาน และไม่มี test UI สำหรับมือถือ/ไอแพด/no horizontal scroll | แก้โค้ด |
| F-07 | โค้ดไม่มี FR / อยู่ใน Out of Scope | `frontend/src/components/RegistrationFormEmbed.tsx:RegistrationFormEmbed` | Out Scope: การลงทะเบียนจริงภายในฟีเจอร์นี้ | มี Google Form จำลองและข้อความให้กรอกข้อมูลลงทะเบียน แทนการมีเพียงลิงก์ส่งต่อ | แก้โค้ด |
| F-08 | test อ่อน | backend test collection | การตรวจสอบทั้งระบบ | `cd backend && pytest -v` จบที่ 11 collection errors เพราะ test imports `backend` ไม่ได้ จึงยังสรุปผล backend requirement จากการรันมาตรฐานไม่ได้ | แก้โค้ด |

## 4. แก้แล้ว
| F-ID | แก้อย่างไร | รู้ได้อย่างไร |
|---|---|---|
| - | ไม่มี | ไม่มีข้อค้นพบเดิมให้ยืนยันว่าแก้แล้ว |
