# Tasks: ค้นหาและดูกิจกรรม (Search)

- Feature: ค้นหาและดูกิจกรรม (Search)
- Spec ID: `001-search`
- อ้างอิง: [plan.md](./plan.md)
- วันที่: 2026-10-05

ฟีเจอร์นี้แบ่งเป็น 11 task เรียงตามการพึ่งพาของโมเดลข้อมูล, API, หน้าจอ และการตรวจสอบระบบ  
ไม่มี task ที่ต้องรอ Open Question เนื่องจาก spec ไม่มี Open Question ค้างอยู่

## รายการงาน

### T-01 สร้างโมเดลข้อมูลกิจกรรมและตารางส่วนตัว
- รองรับ: FR-SRCH-01, FR-SRCH-02, FR-SRCH-03, FR-SRCH-05, IF — ใช้เฉพาะตารางที่นักศึกษากรอกเอง, DOM — ประเภทกิจกรรมที่มหาวิทยาลัยรับรอง
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-02, T-04 และ T-07
- ไฟล์ที่แตะ: `backend/app/models/activity.py`, `backend/app/models/student_schedule.py`, `backend/app/models/collision_warning.py`, `frontend/src/types/activity.ts`
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: โมเดลมีฟิลด์ตาม plan.md ข้อ 3 และไม่มีข้อมูลตารางเรียนจากมหาวิทยาลัยหรือข้อมูลส่วนตัวนอก spec
- สถานะ: พร้อมทำ

### T-02 สร้าง API โหลดกิจกรรมและข้อมูลตารางส่วนตัว
- รองรับ: FR-SRCH-01, FR-SRCH-02, FR-SRCH-03, FR-SRCH-05, IF — ใช้เฉพาะตารางที่นักศึกษากรอกเอง, DOM — กรองเฉพาะ 5 ประเภทที่รับรอง
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-08
- ไฟล์ที่แตะ: `backend/app/api/activities.py`, `backend/app/api/student_schedules.py`, `backend/app/services/activity_service.py`
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: endpoint ตาม plan.md ข้อ 4 คืนรายการกิจกรรม, รายละเอียด และตารางส่วนตัวตามบทบาทและตัวกรองได้
- สถานะ: พร้อมทำ

### T-03 สร้างหน้ารายการกิจกรรมด้วยข้อมูลจำลอง
- รองรับ: FR-SRCH-01, FR-SRCH-03
- ตรวจด้วย: AC-SRCH-01
- ไฟล์ที่แตะ: `frontend/src/pages/SearchList.tsx`, `frontend/src/components/ActivityCard.tsx`, `frontend/src/mocks/activities.ts`
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: หน้ารายการแสดง activity card ทุกกิจกรรมและ badge “เต็มแล้ว/ยังรับสมัคร” ด้วยข้อมูลจำลอง
- สถานะ: พร้อมทำ

### T-04 สร้างตัวกรองประเภทและช่วงเวลาว่างด้วยข้อมูลจำลอง
- รองรับ: FR-SRCH-02, FR-SRCH-03, DOM — ประเภทกิจกรรมที่มหาวิทยาลัยรับรอง
- ตรวจด้วย: AC-SRCH-02
- ไฟล์ที่แตะ: `frontend/src/components/ActivityFilters.tsx`, `frontend/src/services/activityFilter.ts`, `frontend/src/mocks/studentSchedule.ts`
- ต้องทำหลัง: T-01, T-03
- เสร็จเมื่อ: เลือกประเภทใดประเภทหนึ่งจาก 5 ประเภทแล้วแสดงเฉพาะกิจกรรมประเภทนั้น และตัวกรองช่วงเวลาใช้ตารางจำลองของนักศึกษา
- สถานะ: พร้อมทำ

### T-05 แสดงผลลัพธ์และข้อความเมื่อไม่พบกิจกรรม
- รองรับ: FR-SRCH-03, FR-SRCH-04
- ตรวจด้วย: AC-SRCH-05
- ไฟล์ที่แตะ: `frontend/src/components/ActivityResults.tsx`, `frontend/src/components/EmptyActivityState.tsx`
- ต้องทำหลัง: T-03, T-04
- เสร็จเมื่อ: เงื่อนไขที่ไม่มีผลลัพธ์แสดงข้อความ “ไม่พบกิจกรรมที่ตรงกับเงื่อนไข” แทนหน้าว่าง
- สถานะ: พร้อมทำ

### T-06 สร้างหน้ารายละเอียดกิจกรรม
- รองรับ: FR-SRCH-05, ASM-02
- ตรวจด้วย: AC-SRCH-04
- ไฟล์ที่แตะ: `frontend/src/pages/ActivityDetail.tsx`, `frontend/src/components/ActivityDetail.tsx`
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: หน้ารายละเอียดแสดงชั่วโมงที่ได้รับ, วันเวลา, สถานที่ และลิงก์ Google Form ก่อนการส่งต่อ
- สถานะ: พร้อมทำ

### T-07 แสดงคำเตือนกิจกรรมที่ชนกับตารางส่วนตัว
- รองรับ: FR-SRCH-02, FR-SRCH-03, IF — แสดงกิจกรรมที่ชนพร้อมคำเตือนสีแดงโดยไม่ block การดูรายละเอียด, ASM-03
- ตรวจด้วย: AC-SRCH-03
- ไฟล์ที่แตะ: `backend/app/services/collision_service.py`, `backend/app/api/collision_status.py`, `frontend/src/components/CollisionWarning.tsx`, `frontend/src/components/StudentScheduleWarning.tsx`
- ต้องทำหลัง: T-01, T-02, T-03, T-04
- เสร็จเมื่อ: กิจกรรมและช่วงตารางที่ทับกันแสดงคำเตือนสีแดง เปิดดูรายละเอียดต่อได้ และไม่มีการตัดสินใจแทนนักศึกษา
- สถานะ: พร้อมทำ

### T-08 ต่อหน้าจอกับ API จริงและแสดงกิจกรรมใหม่ทันที
- รองรับ: FR-SRCH-01, FR-SRCH-03, FR-SRCH-05, AC-SRCH-06
- ตรวจด้วย: AC-SRCH-06
- ไฟล์ที่แตะ: `frontend/src/services/activityApi.ts`, `frontend/src/pages/SearchList.tsx`, `frontend/src/pages/ActivityDetail.tsx`
- ต้องทำหลัง: T-02, T-03, T-04, T-05, T-06, T-07
- เสร็จเมื่อ: หน้าจอใช้ข้อมูลจาก API จริงและกิจกรรมที่ผู้จัดสร้างสำเร็จแล้วปรากฏในรายการนักศึกษาทันทีโดยไม่รอ Admin อนุมัติ
- สถานะ: พร้อมทำ

### T-09 ทำระบบ polling และอัปเดตสถานะกิจกรรม
- รองรับ: FR-SRCH-01, IF — polling Google Sheets ทุก 1–2 นาที, IF — อัปเดตสถานะภายใน 1 นาทีและไม่เกิน 2 นาที
- ตรวจด้วย: AC-SRCH-07
- ไฟล์ที่แตะ: `backend/app/integrations/google_sheets.py`, `backend/app/services/activity_status_sync.py`, `backend/app/jobs/status_polling.py`, `frontend/src/hooks/useActivityStatus.ts`
- ต้องทำหลัง: T-02, T-08
- เสร็จเมื่อ: การจำลองข้อมูล Google Sheets ที่เต็มจำนวนทำให้ badge เปลี่ยนเป็น “เต็มแล้ว” ภายใน 1 นาที และไม่เกิน 2 นาที
- สถานะ: พร้อมทำ

### T-10 ตรวจสอบ responsive และประสิทธิภาพการค้นหา
- รองรับ: AC-SRCH-08, NFR — รองรับผู้ใช้งานประมาณ 5,000 คนต่อภาคการศึกษาและตอบสนองภายใน 2 วินาที, IF — รองรับผู้ใช้งานพร้อมกันประมาณ 5,000 คน
- ตรวจด้วย: AC-SRCH-08
- ไฟล์ที่แตะ: `frontend/src/styles/responsive.css`, `frontend/src/pages/SearchList.tsx`, `backend/tests/performance/test_activity_search.py`
- ต้องทำหลัง: T-04, T-05, T-06, T-08
- เสร็จเมื่อ: ทดสอบบนคอมพิวเตอร์ มือถือ และไอแพดแล้วไม่เกิด horizontal scroll/pinch-zoom และ benchmark คำขอค้นหาผ่านเกณฑ์ 2 วินาที
- สถานะ: พร้อมทำ

### T-11 ตรวจสอบการปฏิบัติตาม NFR ระบบกลางและ HTTPS
- รองรับ: NFR — ส่งข้อมูลผ่าน HTTPS, NFR — เตรียมข้อมูลส่งเข้า REG ภายใน 1 วันทำการ, NFR — มี Audit Log การอนุมัติ/ปฏิเสธเอกสารของ Admin, ASM-08
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานตรวจการเชื่อมต่อกับข้อกำหนดระบบกลาง
- ไฟล์ที่แตะ: `deployment/https-config.yml`, `docs/integration/search-system-nfr.md`
- ต้องทำหลัง: T-02, T-08, T-09, T-10
- เสร็จเมื่อ: มีผลตรวจยืนยันว่า endpoint ของ Search ใช้ HTTPS และมีจุดเชื่อมต่อ/การพึ่งพา REG กับ Audit Log ตามระบบกลาง โดยไม่สร้าง workflow นอก scope ของ Search
- สถานะ: พร้อมทำ

## ตารางตรวจความครบของ Acceptance Criteria

| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC-SRCH-01 | T-03 |
| AC-SRCH-02 | T-04 |
| AC-SRCH-03 | T-07 |
| AC-SRCH-04 | T-06 |
| AC-SRCH-05 | T-05 |
| AC-SRCH-06 | T-08 |
| AC-SRCH-07 | T-09 |
| AC-SRCH-08 | T-10 |

## ตารางตรวจความครบของ Constraints

| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| IF — ห้ามดึงข้อมูลจากระบบตารางเรียนของมหาวิทยาลัยโดยตรง | T-01, T-02, T-07 |
| IF — สถานะ “เต็ม/ว่าง” ไม่รับประกันว่า real-time แบบเป๊ะและใช้ Google Sheets polling | T-09 |
| IF — อัปเดตสถานะภายใน 1 นาทีและไม่เกิน 2 นาที | T-09 |
| DOM — แสดงเฉพาะ 1 ใน 5 ประเภทกิจกรรมที่รับรอง | T-01, T-02, T-04 |
| IF — ตารางชนต้องแสดงคำเตือนสีแดงและไม่ block รายละเอียด | T-07 |
| IF — รองรับผู้ใช้งานพร้อมกันประมาณ 5,000 คนและตอบสนองภายใน 2 วินาที | T-10 |
| NFR — ส่งข้อมูลระหว่างผู้ใช้กับเซิร์ฟเวอร์ผ่าน HTTPS | T-11 |
| NFR — เตรียมข้อมูลส่งเข้า REG ภายใน 1 วันทำการ | T-11 |
| NFR — มี Audit Log การอนุมัติ/ปฏิเสธเอกสารของ Admin | T-11 |

## สิ่งที่ยังไม่ทำ

Spec ปัจจุบันไม่มี Open Question ค้างอยู่ โดย ASM-06 ถึง ASM-08 ระบุว่า Q-01 ถึง Q-03 ได้รับคำตอบแล้วหรือเป็นข้อกำหนดระดับระบบกลาง งานที่เกี่ยวข้องกับ REG และ Audit Log จึงอยู่ใน T-11 ในฐานะการตรวจจุดเชื่อมต่อเท่านั้น ไม่สร้าง workflow การอนุมัติ เอกสาร หรือการลงทะเบียนที่อยู่นอก scope ของ Search
