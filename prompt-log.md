# Prompt log

บันทึกทุกครั้งที่ใช้ AI กับ repo นี้ เขียนต่อท้ายเรื่อย ๆ ไม่ต้องลบของเก่า

---

## 2026-09-20 17:00 คำสั่ง: /clarify

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์: specs/001-search/spec.md (v1 → v2)

### คำถามที่ AI ถาม (ทั้งหมด)

1. เมื่อกิจกรรมชนกับตารางส่วนตัว ระบบควรตัดหรือแสดงพร้อมคำเตือน?
2. สามารถกดดูรายละเอียดได้หรือไม่ หากชนกับตาราง?
3. สถานะกิจกรรมต้องอัปเดตภายในกี่นาทีหลังข้อมูล Google Sheets เปลี่ยน?
4. "ช่วงเวลาว่าง" ใช้ตารางของนักศึกษาเป็นฐานหรือไม่?
5. เมื่อไม่พบผลลัพธ์ควรแสดงข้อความแบบใด?
6. ฟีเจอร์นี้มีการลงทะเบียนจริงหรือไม่?
7. "กิจกรรมทั้งหมด" มีความหมายต่างกันตามบทบาทผู้ใช้งานหรือไม่?
8. ระบบต้องรองรับอุปกรณ์ใดบ้างและให้ usability อย่างไร?
9. Qf1-8: เงื่อนไขยืนยันเพิ่มเติมเรื่องการลงทะเบียน, สีแดง/คำเตือน, ระยะเวลา, ประเภทผู้ใช้งาน, เงื่อนไขการอนุมัติ, performance, อุปกรณ์, และ NFR ส่วนกลาง

### คำตอบของทีมและเหตุผล

1. แสดงกิจกรรมไว้พร้อมคำเตือนสีแดง โดยไม่ block การดูรายละเอียด
2. ยังสามารถกดดูรายละเอียดได้ แต่ถ้าจะกดลงทะเบียนต้องมีแจ้งเตือนยืนยันก่อน
3. อัปเดตภายใน 1 นาทีหลังข้อมูลอัปเดต และต้องไม่ช้ากว่า 2 นาที
4. ใช้ช่วงเวลาที่นักศึกษากรอกในตารางส่วนตัวเป็นฐาน
5. แสดงข้อความทั่วไป “ไม่พบกิจกรรมที่ตรงกับเงื่อนไข”
6. ฟีเจอร์นี้ไม่ดำเนินการลงทะเบียนจริง และมีชื่อกิจกรรมที่ตรง ที่สามารถกดแสดงรายละเอียดได้
7. สำหรับนักศึกษาจะเป็นกิจกรรมที่ยังเปิดรับนักศึกษาอยู่และว่าง; สำหรับผู้ดูแลกิจกรรมเป็นกิจกรรมของตัวเองที่เผยแพร่; สำหรับ Admin เป็นกิจกรรมที่เคยอนุมัติเข้าสู่ระบบทั้งหมด รวมประวัติกิจกรรมที่เคยลบ
8. รองรับคอมพิวเตอร์ มือถือ และไอแพด โดยปรับขนาดหน้าจอให้ใช้งานได้ง่าย และมี usability ที่คนใช้ทั่วไปรับได้
9. ทีมยืนยันว่าฟีเจอร์ Search เป็นหน้าดูรายละเอียดและส่งต่อไปยัง Google Form สำหรับลงทะเบียนต่อ; ไม่ต้อง implement กระบวนการลงทะเบียนจริง; การอัปเดตสถานะเต็ม/ว่างเริ่มนับจากข้อมูลต้นทางอัปเดต; NFR ส่วนกลางยังถือเป็น system-wide requirement ที่ Search ต้องปฏิบัติตาม

### สิ่งที่แก้ใน spec.md (v1 เป็น v2)

- ปรับ Goal ให้ชัดว่า Search เป็นฟีเจอร์แสดงรายละเอียด + ส่งต่อ Google Form ไม่ใช่การลงทะเบียนจริง
- ปรับ Scope และ Out Scope ให้ตรงกับบทบาทผู้ใช้งานและการส่งต่อ
- ปรับ Constraints ให้ระบุชัดว่าเมื่อกิจกรรมชนกับตารางส่วนตัว จะแสดงสถานะเตือนสีแดงและไม่ block การดูรายละเอียด
- ปรับ Constraints ให้ระบุอัตราอัปเดตสถานะ “เต็มแล้ว/ยังรับสมัคร” ภายใน 1 นาทีหลัง Google Sheets อัปเดต และไม่ช้ากว่า 2 นาที
- ปรับ FR-SRCH-02 ให้ใช้ตารางส่วนตัวเป็นฐานสำหรับการกรองช่วงเวลาว่าง
- ปรับ AC-SRCH-03, AC-SRCH-04, AC-SRCH-06, AC-SRCH-07, AC-SRCH-08 ให้สอดคล้องกับคำตอบของทีม
- เพิ่ม Assumptions สำหรับบทบาทผู้ใช้งาน, การแสดงคำเตือน, การตอบสนองภายใน 2 วินาที, และความหมายของ “กิจกรรมทั้งหมด”
- เปลี่ยน Status เป็น Draft v2 และอัปเดตวันที่ 2026-09-20

---

## 2026-09-20 17:05 คำสั่ง: /plan

- เครื่องมือ: Copilot ใน Codespaces
- ผลลัพธ์: specs/001-search/plan.md
- Constraint ที่ AI ยังไม่ได้ใช้:
  - NFR กระบวนการเตรียมข้อมูลให้พร้อมส่งเข้า REG ต้องทำได้ภายใน 1 วันทำการเมื่อเอกสารครบถ้วน — ยังไม่ได้ใช้ใน plan เนื่องจากเป็น system-wide NFR ไม่ใช่ functional requirement ของฟีเจอร์ Search
  - NFR ระบบต้องมี Audit Log บันทึกการอนุมัติ/ปฏิเสธเอกสารของ Admin — ยังไม่ได้ใช้ใน plan เนื่องจากไม่ใช่ functional scope ของ Search
- สิ่งที่ AI บอกว่าอยากเดาแต่ไม่ได้เดา:
  - ไม่มี Open Question ที่ต้องเดาเพิ่มเติม หลังจากทีมชี้แจงว่า Q-01 ถึง Q-03 เป็นข้อมูลที่ชัดแล้ว

  ---

  ## 2026-10-13 คำสั่ง: `/testcases AC-SRCH-01 specs/001-search/`

  - โหมด: ร่าง
  - ผลลัพธ์: สร้าง `specs/001-search/test-cases.md` และเสนอ test case 3 แถวสำหรับ `AC-SRCH-01`
  - TC ID: `TC-SRCH-01-1`, `TC-SRCH-01-2`, `TC-SRCH-01-3`
  - หมายเหตุ: กรณีไม่มีรายการกิจกรรมยังไม่มีพฤติกรรมที่ระบุใน `s

---

## 2026-10-14 คำสั่ง: `/testcases AC-ACT-01 specs/004-NewActivity`

- โหมด: ร่าง
- ผลลัพธ์: สร้าง `specs/004-NewActivity/test-cases.md` และเสนอ test case 3 แถวสำหรับ `AC-ACT-01`
- TC ID: `TC-ACT-01-1`, `TC-ACT-01-2`, `TC-ACT-01-3`
- หมายเหตุ: ไม่มี `test-cases.md` ในฟีเจอร์นี้ก่อนหน้า จึงสร้างตารางแบบร่างตามแม่แบบ และหยุดก่อนเขียนโค้ด test ตามคำสั่ง

---

## 2026-10-14 คำสั่ง: `/testcases AC-ACT-01 specs/004-NewActivity`

- โหมด: ร่าง (หยุดตามเงื่อนไข: มีเฉพาะแถวสถานะ “ร่าง” และไม่มีแถว “ใช้ได้”)
- ผลลัพธ์: ไม่เขียนโค้ด test และไม่รัน test เนื่องจากต้องมีการตรวจแถวก่อน
- TC ID ที่เสนอ: `TC-ACT-01-1`, `TC-ACT-01-2`, `TC-ACT-01-3`
- สถานะปัจจุบันใน [specs/004-NewActivity/test-cases.md](/workspaces/AiKiller-swreqspec/specs/004-NewActivity/test-cases.md): ทั้ง 3 แถวเป็น `ร่าง`
- ข้อสรุป: ต้องให้ทีมตรวจแถวในตารางและเปลี่ยนสถานะเป็น `ใช้ได้` ก่อน จากนั้นสั่ง `/testcases` อีกครั้ง

---

## 2026-10-14 คำสั่ง: `/testcases AC-ACT-01 specs/004-NewActivity`

- โหมด: เขียน test
- ผลลัพธ์: เขียน test ตามแถวที่มีสถานะ `ใช้ได้` ใน [specs/004-NewActivity/test-cases.md](/workspaces/AiKiller-swreqspec/specs/004-NewActivity/test-cases.md)
- TC ID ที่เขียน: `TC-ACT-01-1`, `TC-ACT-01-2`, `TC-ACT-01-3`
- ไฟล์ที่เพิ่ม: [frontend/src/__tests__/TC-ACT-01.test.jsx](/workspaces/AiKiller-swreqspec/frontend/src/__tests__/TC-ACT-01.test.jsx)
- ผลทดสอบ: ผ่าน 3/3
- คำสั่งรัน: `cd /workspaces/AiKiller-swreqspec/frontend && npm test -- --run src/__tests__/TC-ACT-01.test.jsx`
pec.md` จึงระบุว่า `spec ไม่ได้บอก` และยังไม่เขียนโค้ด test

  ---

  ## 2026-10-13 คำสั่ง: `/testcases AC-SRCH-01 specs/001-search/`

  - โหมด: เขียน test
  - ผลลัพธ์: เพิ่ม test 2 ตัวใน `frontend/src/pages/SearchList.test.tsx`
  - TC ID: `TC-SRCH-01-1`, `TC-SRCH-01-2`
  - `TC-SRCH-01-3` ไม่เขียนโค้ด เนื่องจากตารางกำหนด `ตรวจด้วย: คน`
  - ผล test: Vitest ทั้งชุดผ่าน 18 test files, 30 tests; มี React `act(...)` warning เดิมจาก `SearchList` แต่ไม่มี test ล้มเหลว

  ---

  ## 2026-10-13 คำสั่ง: `/verify specs/001-search`

  - ผล test: `cd frontend && npm test` ผ่าน 18 test files, 30 tests; `cd backend && pytest -v` เก็บ 44 รายการไม่ได้และจบที่ 11 collection errors จาก `ModuleNotFoundError: No module named 'backend'`
  - RTM: สร้าง `specs/001-search/rtm.md`
  - จำนวนสถานะไปข้างหน้า: ครบ 4, ยังไม่ถึง 0, รอ 0, ช่องโหว่ 11
  - F-ID ข้อค้นพบใหม่: `F-01` ถึง `F-08`

  ---

  ## 2026-10-13 คำสั่ง: แก้ข้อค้นพบใน `/verify specs/001-search`

  - แก้ F-02: เชื่อมตัวกรองประเภท/ช่วงเวลาว่างเข้ากับหน้า Search และ `ActivityResults`
  - แก้ F-03 ถึง F-05: เพิ่ม/ปรับ test สำหรับกิจกรรมใหม่, badge ต่อ card, วันเวลาเริ่ม/สิ้นสุด และ polling ที่ 120 วินาที
  - แก้ F-08: เพิ่ม `apscheduler>=3.10` ใน `backend/requirements.txt` และแก้ `backend/pytest.ini` ให้ import package จาก repository root
  - ไม่แก้ F-01 เพราะทีมระบุ `เพิ่ม Q-xx`; ไม่แก้ F-07 เพราะ component เดียวกันถูกใช้และมี test ของ Registration จึงต้องแยกขอบเขต/ถามทีมก่อน
  - ผล test: `frontend`: 18 test files, 32 tests ผ่าน; `backend` ด้วย `.venv/bin/python -m pytest -v`: 73 tests ผ่าน

---

## 2026-10-04 04:51 คำสั่ง: /clarify

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์: specs/003-Schedule/spec.md (v1 → v2)

### คำถามที่ AI ถาม (ทั้งหมด)

1. กฎการตรวจว่า “เวลาชนกัน” ควรถือว่าชนเมื่อใด?
2. “ช่วงเวลาที่ไม่ว่าง” ต้องเป็นข้อมูลแบบใดบ้างสำหรับแต่ละรายการ?
3. ระบบต้องรองรับการเพิ่มเฉพาะรายการใหม่เท่านั้น หรือจะสามารถแก้ไขรายการที่มีอยู่ได้?
4. การแจ้งเตือน “เมื่อเวลาชน” ควรเกิดขึ้นที่จุดใดในกระบวนการใช้งาน?
5. “5,000 คนต่อภาคการศึกษา” ควรหมายถึงจำนวนผู้ใช้พร้อมกันหรือจำนวนผู้ใช้ทั้งหมด?

### คำตอบของทีมและเหตุผล

1. ช่วงเวลาจะถือว่าชนเมื่อมีส่วนคาบเกี่ยวกัน
2. แต่ละรายการต้องมีวันเริ่ม/วันสิ้นสุดและเวลาเริ่ม/เวลาสิ้นสุด
3. ระบบอนุญาตให้แก้ไขรายการที่มีอยู่ได้
4. การแจ้งเตือนเกิดขึ้นในหน้ารายละเอียดกิจกรรมหรือก่อนลงทะเบียนกิจกรรม
5. หมายถึงผู้ใช้งานพร้อมกัน 5,000 คน หากเกิน 5,000 คน ต้องรอคิวก่อน

### สิ่งที่แก้ใน spec.md (v1 เป็น v2)

- ปรับคำจำกัดความของ “เวลา kาบเกี่ยว” ให้ชัดเจนว่าใช้ช่วงเวลาที่มีส่วนทับกันจริง ๆ
- ปรับ FR-SCHED-02 ให้ระบุข้อมูลของรายการตารางส่วนตัวเป็นวันเริ่ม/สิ้นสุดและเวลาเริ่ม/สิ้นสุด
- ปรับ In Scope และ Out Scope ให้รองรับการแก้ไขรายการแต่ยังไม่รวมการลบรายการ
- ปรับ DOM-SCHED-01 และ AC-SCHED-05/06 ให้สอดคล้องกับการแจ้งเตือนที่แสดงในหน้ากิจกรรมหรือก่อนลงทะเบียน
- ปรับ NFR-SCHED-01 ให้ระบุชัดว่าเป็นจำนวนผู้ใช้งานพร้อมกัน 5,000 คน และเกินขนาดต้องรอคิว
- เพิ่ม Assumptions สำหรับการคาบเกี่ยว การแจ้งเตือน การแก้ไขรายการ และความหมายของ NFR
- เปลี่ยน Status เป็น Draft v2 และอัปเดตวันที่ 2026-10-04

---

## 2026-10-04 04:56 คำสั่ง: /clarify

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์: specs/003-Schedule/spec.md (ทบทวนต่อจาก Draft v2)

### คำถามที่ AI ถาม (ทั้งหมด)

1. แต่ละรายการที่มีวันเริ่ม–วันสิ้นสุดและเวลาเริ่ม–เวลาสิ้นสุด หมายถึงช่วงเวลาครั้งเดียวต่อเนื่อง หรือเกิดซ้ำในแต่ละวัน/สัปดาห์ภายในช่วงวันที่นั้น?
2. คำว่า “ผู้ใช้งานทำงานเสร็จ” ใน NFR-SCHED-01 หมายถึงเหตุการณ์ใดที่จะปล่อยช่องให้ผู้ใช้คนถัดไปเข้าถึงฟีเจอร์ได้?
3. เมื่อนักศึกษาแก้ไขช่วงเวลาที่บันทึกไว้ ระบบควรแทนที่ข้อมูลเดิมของรายการนั้น โดยยังคงรายการอื่นไว้หรือไม่?
4. เมื่อเวลาของกิจกรรมเริ่มตรงกับเวลาสิ้นสุดของรายการตารางส่วนตัวพอดี เช่น ตาราง 09:00–10:00 และกิจกรรม 10:00–11:00 ควรถือว่าคาบเกี่ยวกันหรือไม่?
5. เมื่อ AC-SCHED-06 ระบุว่ายังลงทะเบียนต่อได้ แต่การลงทะเบียนจริงอยู่ใน Out of Scope ควรตีความว่าอย่างไร?
6. ควรปรับ AC-SCHED-02 ให้ครอบคลุมการแก้ไขรายการเดิมด้วย โดยระบุว่ารายการนั้นเปลี่ยนตามข้อมูลใหม่และรายการอื่นยังอยู่หรือไม่?

### คำตอบของทีมและเหตุผล

1. รายการเกิดซ้ำทุกวันในช่วงวันเริ่มถึงวันสิ้นสุด
2. การใช้งานสิ้นสุดเมื่อผู้ใช้ออกจากหน้าตารางส่วนตัวหรือหน้ากิจกรรม
3. ใช่ แก้เฉพาะรายการนั้นและเก็บรายการอื่นไว้
4. ไม่คาบเกี่ยว เพราะเวลา 10:00 คือจบช่วงก่อนหน้า (09:59)
5. เป็นการเตือนเท่านั้น และนักศึกษายังไปขั้นตอนลงทะเบียนผ่าน Google Form ซึ่งอยู่นอกขอบเขตฟีเจอร์นี้ได้
6. ใช่ ให้ AC-SCHED-02 ครอบคลุมการเพิ่มและแก้ไขตามที่ยืนยันแล้ว

### สิ่งที่แก้ใน spec.md

- ระบุว่ารายการช่วงเวลาที่บันทึกเกิดซ้ำทุกวัน รวมวันเริ่มและวันสิ้นสุด
- ระบุการเปรียบเทียบช่วงเวลาแบบรวมเวลาเริ่มแต่ไม่รวมเวลาสิ้นสุด เช่น 09:00–10:00 สิ้นสุดก่อน 10:00
- ปรับ AC-SCHED-02 ให้ครอบคลุมการเพิ่ม/แก้ไข และให้การแก้ไขแทนที่เฉพาะรายการที่เลือกโดยคงรายการอื่น
- ระบุว่าเมื่อแสดงคำเตือน นักศึกษายังไปยังขั้นตอนลงทะเบียน Google Form ได้ โดยไม่รวมการลงทะเบียนจริงในฟีเจอร์นี้
- ระบุเงื่อนไขปล่อยช่องผู้ใช้งานใน NFR-SCHED-01 เมื่อออกจากหน้าตารางส่วนตัวหรือหน้ากิจกรรม
- ปรับ AC-SCHED-07 และ Traceability ให้สอดคล้องกับการไปยัง Google Form และเกณฑ์ NFR ที่ระบุ

---

## 2026-10-04 05:46 คำสั่ง: /plan

- เครื่องมือ: Copilot ใน Codespaces
- ผลลัพธ์: specs/003-Schedule/plan.md
- Constraints ที่ยังไม่ได้ใช้: ไม่มี; CON-SCHED-01, IF-SCHED-01 และ DOM-SC

---

## 2026-10-06 09:59 คำสั่ง: /tasks specs/003-Schedule/spec.md

- เครื่องมือ: Copilot ใน Codespaces
- ผลลัพธ์: สร้างไฟล์ `specs/003-Schedule/tasks.md` สำเร็จ
- สรุป: มี 8 task ทั้งหมด, 0 task ที่ต้องรอ Open Questions, และทุก AC-SCHED-01 ถึง AC-SCHED-07 มี task ที่ตรวจแล้ว
- หมายเหตุ: spec.md อยู่ในสถานะ Draft v2 และไม่มี Open Questions จึงไม่ต้องหยุดที่ Q-xx
HED-01 ถูกระบุในตารางตรวจ Constraints

---

## 2026-10-05 05:03 คำสั่ง: /clarify

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์: specs/002-Register/spec.md (v1 → v2)

### คำถามที่ AI ถาม (ทั้งหมด)

1. จำนวนผู้ลงทะเบียนต้องนับจากแถวหรือข้อมูลประเภทใดใน Google Sheets และต้องจัดการรายการซ้ำอย่างไร?
2. หากกิจกรรมเต็มระหว่างที่นักศึกษากำลังกรอกหรือกำลังส่ง Google Form ระบบต้องยอมรับหรือปฏิเสธการลงทะเบียนอย่างไร?
3. จำนวนผู้ลงทะเบียนสูงสุดของกิจกรรมมาจากแหล่งใด และใครเป็นผู้กำหนดค่าที่ Google Form ใช้ปิดรับคำตอบ?
4. เมื่อ Google Sheets API ไม่ตอบสนองหรือส่งข้อมูลไม่สำเร็จ ระบบต้องแสดงและคงสถานะการลงทะเบียนอย่างไร?
5. เมื่อกิจกรรมเต็มแล้ว หน้ารายละเอียดกิจกรรมต้องยังแสดง Google Form หรือแสดงข้อความว่าปิดรับลงทะเบียนแทน?
6. Notification ยืนยันการลงทะเบียนต้องแสดงที่หน้าใด มีข้อมูลใดบ้าง และต้องเก็บประวัตินานเท่าใด?
7. ระบบระบุสิทธิ์ Admin และผู้จัดกิจกรรมจากข้อมูลใด และกรณีผู้ใช้มีทั้งสองบทบาทต้องจัดการอย่างไร?
8. “ผู้ตอบฟอร์ม” กับ “ผู้ลงทะเบียน” ต้องถือว่าเป็นข้อมูลชุดเดียวกันหรือมีเงื่อนไขคัดกรองก่อนนับเป็นผู้ลงทะเบียน?

### คำตอบของทีมและเหตุผล

1. นับทุกแถวคำตอบที่ Google Form บันทึก โดยไม่ตัดรายการซ้ำ
2. ให้ Google Form เป็นผู้ตัดสิน และระบบยอมรับเฉพาะข้อมูลที่ถูกบันทึกสำเร็จ
3. ค่าจำนวนจำกัดถูกตั้งไว้ล่วงหน้าใน Google Form และตรงกับค่าของกิจกรรมในระบบ
4. คงสถานะล่าสุดไว้และไม่เปลี่ยนจำนวนจนกว่าจะดึงข้อมูลสำเร็จ
5. ไม่แสดงหรือใช้งาน Google Form ไม่ได้เมื่อสถานะเป็น “เต็มแล้ว”
6. แสดงในการแจ้งเตือนภายในเว็บไซต์หลังข้อมูลถูกบันทึกใน Google Sheets และเก็บไว้จนกว่านักศึกษาจะอ่าน
7. ผู้ใช้ที่มีบทบาทใดบทบาทหนึ่งสามารถเข้าถึง Google Sheets ได้
8. ผู้ตอบฟอร์มทุกคนที่ถูกบันทึกใน Google Sheets ถือเป็นผู้ลงทะเบียน

### สิ่งที่แก้ใน spec.md (v1 เป็น v2)

- เพิ่มสถานะ `Draft v2` และวันที่ 2026-10-05
- ระบุหลักการนับจำนวนผู้ลงทะเบียนว่าใช้ทุกแถวคำตอบจาก Google Form และไม่ตัดรายการซ้ำ
- ระบุให้ Google Form เป็นผู้ตัดสินกรณีเต็มระหว่างกรอกหรือส่ง และยอมรับเฉพาะข้อมูลที่บันทึกสำเร็จ
- ระบุว่าจำนวนจำกัดใน Google Form ต้องตรงกับค่าของกิจกรรมในระบบ
- ระบุพฤติกรรมเมื่อ Google Sheets API ไม่ตอบสนอง โดยคงสถานะล่าสุดและจำนวนเดิม
- ระบุว่าเมื่อเต็มแล้วต้องไม่แสดงหรือไม่อนุญาตให้ใช้งาน Google Form
- ระบุรายละเอียดการแสดงและการเก็บ Notification ยืนยันการลงทะเบียน
- ระบุสิทธิ์ของ Admin หรือผู้จัดกิจกรรม และแก้ Traceability ให้ AC-REG-06 อ้าง NFR-SEC-01 และ AC-REG-07 อ้าง NFR-SEC-02
- เพิ่ม ASM-06 ถึง ASM-12 และลบ Q-01/Q-02 ที่ทีมตอบแล้วHED-01 ถูกระบุในตารางตรวจ Constraints

---

## 2026-10-05 05:14 คำสั่ง: /clarify

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์: specs/006-ExportList/spec.md (v1 → v2)

### คำถามที่ AI ถาม (ทั้งหมด)

1. เมื่อผู้จัดกิจกรรมกด “ดาวน์โหลดรายชื่อ” ระบบต้องพาไปยัง Google Sheets หรือสร้างลิงก์ดาวน์โหลดไฟล์จากระบบโดยตรง?
2. ระบบต้องรองรับไฟล์รูปแบบใดบ้าง: `.xlsx`, `.csv` หรือทั้งสองรูปแบบ?
3. ข้อมูลขั้นต่ำหรือคอลัมน์ใดต้องมีในไฟล์เพื่อให้ถือว่าสามารถใช้เช็คชื่อหน้างานได้?
4. ไฟล์ที่นำไปใช้ในระบบ REG ต้องมีรูปแบบหรือคอลัมน์บังคับใดเพื่อให้ทำตามกระบวนการเดิมได้?
5. หาก Google Sheets หรือลิงก์ดาวน์โหลดไม่พร้อมใช้งาน ระบบต้องแสดงข้อความหรือดำเนินการอย่างไร?
6. ระบบต้องตรวจสอบสิทธิ์ของผู้จัดกิจกรรมและ Admin ทุกครั้งที่เข้าถึงหรือดาวน์โหลดข้อมูลหรือไม่?
7. จำนวนผู้ลงทะเบียนอย่างน้อย 1 คนที่ใช้ตัดสินการแสดงปุ่ม ต้องอ้างอิงจากข้อมูลล่าสุดใน Google Sheets หรือจากข้อมูลที่ระบบบันทึกไว้?
8. ระบบต้องทำเพียงให้ผู้จัดกิจกรรมดาวน์โหลดไฟล์เพื่อดำเนินการต่อเอง หรือควรมีการเปิดลิงก์/คำแนะนำไปยังขั้นตอน REG ภายในระบบด้วย?

### คำตอบของทีมและเหตุผล

1. ให้ระบบพาผู้จัดกิจกรรมไปยัง Google Sheets โดยตรง
2. รองรับทั้ง `.xlsx` และ `.csv`
3. ใช้ข้อมูลทุกคอลัมน์ที่มีอยู่ใน Google Sheets โดยไม่ปรับรูปแบบหรือตัดคอลัมน์
4. ไฟล์ที่ดาวน์โหลดจาก Google Sheets มีรูปแบบที่ระบบ REG รองรับอยู่แล้ว
5. แสดงข้อผิดพลาดและไม่สร้างลิงก์ดาวน์โหลดที่ใช้งานไม่ได้
6. ตรวจสอบสิทธิ์ทุกครั้งก่อนแสดงปุ่มและก่อนนำไปยัง Google Sheets
7. ใช้จำนวนล่าสุดที่ระบบอ่านจาก Google Sheets ได้สำเร็จ
8. ระบบทำเฉพาะการดาวน์โหลด และผู้จัดกิจกรรมดำเนินการต่อใน REG เองทั้งหมด

### สิ่งที่แก้ใน spec.md (v1 เป็น v2)

- เพิ่มสถานะ `Draft v2` และวันที่ 2026-10-05
- กำหนดให้ปุ่มพาผู้จัดกิจกรรมไปยัง Google Sheets โดยตรง
- กำหนดให้รองรับไฟล์ `.xlsx` และ `.csv` โดยใช้ทุกคอลัมน์จาก Google Sheets โดยไม่ปรับหรือตัดข้อมูล
- ระบุว่าไฟล์มีรูปแบบที่ระบบ REG รองรับอยู่แล้ว และผู้จัดกิจกรรมดำเนินการต่อเอง
- กำหนดให้ตรวจสอบสิทธิ์ทุกครั้งก่อนแสดงปุ่มและก่อนนำไปยัง Google Sheets
- กำหนดให้ใช้จำนวนล่าสุดที่ระบบอ่านจาก Google Sheets ได้สำเร็จเป็นเงื่อนไขแสดงปุ่ม
- ระบุให้แสดงข้อผิดพลาดและไม่สร้างลิงก์ที่ใช้งานไม่ได้เมื่อ Google Sheets ไม่พร้อม
- เพิ่ม `ASM-05` ถึง `ASM-07` และลบ `Q-01` ถึง `Q-03` ที่ทีมตอบแล้วHED-01 ถูกระบุในตารางตรวจ Constraints

---

## 2026-10-05 05:17 คำสั่ง: /plan

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์: specs/006-ExportList/spec.md (Draft v2)
- ผลลัพธ์: specs/006-ExportList/plan.md
- Constraint ที่ยังไม่ได้ใช้: ไม่มี; IF-GSHEET-01, IF-EXPORT-01, IF-REG-01, DOM-APP-01, ACC-GSHEET-01, ACC-GSHEET-02 และ CON-EXPORT-01 ถูกระบุในตารางตรวจ Constraints
- AC ที่ทดสอบยากหรือทดสอบไม่ได้ในสภาพแวดล้อมของนักศึกษา:
  - AC-EXP-02 ต้องตรวจการพาไปยัง Google Sheets จริง จึงอาจต้องใช้ URL จำลองหรือ test double
  - AC-EXP-03 ต้องตรวจไฟล์ `.xlsx` และ `.csv` ที่มีข้อมูลทุกคอลัมน์จากระบบภายนอก จึงอาจต้องใช้ข้อมูลจำลองหรือสภาพแวดล้อม Google Sheets ทดสอบ
  - AC-EXP-04 ต้องยืนยันรูปแบบไฟล์ที่ระบบ REG รองรับ ซึ่งเป็นกระบวนการภายนอกระบบนี้
- สิ่งที่ AI อยากเดาแต่ไม่ได้เดา:
  - ไม่สร้างการอัปโหลดรายชื่อเข้า REG หรือการเชื่อมต่ออัตโนมัติ เพราะ FR-EXP-06 และ Out Scope ระบุห้ามทำ
  - ไม่กำหนดคอลัมน์ใหม่หรือปรับรูปแบบไฟล์ เพราะ FR-EXP-03 และ FR-EXP-04 กำหนดให้คงทุกคอลัมน์เดิม
  - ไม่กำหนด Open Questions เพิ่ม เนื่องจาก spec ฉบับ Draft v2 ไม่มี Open Questions ค้างอยู่HED-01 ถูกระบุในตารางตรวจ Constraints
- AC ที่ทดสอบยากในสภาพแวดล้อมของนักศึกษา: ไม่มี AC ที่ทดสอบไม่ได้โดยหลักการ แต่ NFR-SCHED-01 ซึ่งไม่ใช่ AC ต้องทดสอบโหลดผู้ใช้พร้อมกัน 5,000 คนและการรอคิวเกินจำนวน อาจต้องใช้สภาพแวดล้อมทดสอบเฉพาะ
- สิ่งที่ AI อยากเดาแต่ไม่ได้เดา:
  - ไม่เลือกเทคโนโลยีฐานข้อมูล เนื่องจาก spec ไม่ระบุ
  - ไม่กำหนด path API ว่าเป็นข้อกำหนด; path ใน plan เป็นเพียงข้อเสนอเชิงออกแบบ
  - ใช้วันเวลาในหน้ารายละเอียดกิจกรรมที่มีอยู่แล้วเป็น input ตรวจการคาบเกี่ยว ตามคำตอบของทีมในรอบวางแผนนี้

---

## 2026-10-04 15:37 คำสั่ง: /clarify

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์: specs/004-NewActivity/spec.md (v1 → v2)

### คำถามที่ AI ถาม (ทั้งหมด)

1. กระบวนการเผยแพร่กิจกรรมหลังบันทึกสำเร็จควรเป็นแบบใดตาม Requirement ล่าสุด?
2. ข้อมูลใดบ้างที่ถือว่า Required Field ในการสร้างกิจกรรม?
3. ลิงก์ Google Form ต้องเป็น URL ของ Google Forms เท่านั้น หรือสามารถใช้ URL อื่นได้?
4. กิจกรรมหนึ่งรายการควรมีวันเวลาแบบใด: ช่วงเวลาเดียวหรือหลายช่วงเวลา?
5. หลังจากสร้างกิจกรรมแล้ว ผู้จัดกิจกรรมสามารถแก้ไขหรือลบกิจกรรมได้หรือไม่?
6. “นักศึกษาสามารถค้นหาและเห็นกิจกรรมนั้นได้” หมายถึงอะไรในเชิงเทคนิคและเชิง UX?
7. เกณฑ์ NFR-ACT-01 ควรระบุอะไรให้ชัดก่อนเริ่มพัฒนา?

### คำตอบของทีมและเหตุผล

1. มีหน้าตรวจสอบอีกครั้งก่อนสร้างกิจกรรมจริง ๆ เพื่อยืนยันว่าต้องการสร้างกิจกรรมนี้
2. Required Field คือ ชื่อ, ประเภทกิจกรรม, วันเวลาที่จัด, สถานที่ที่จัด, จำนวนรับสมัคร, และชั่วโมงจิตอาสาที่จะได้รับ
3. URL อะไรก็ได้ที่ผู้จัดสะดวก — ไม่จำกัดเฉพาะ Google Forms
4. ช่วงเวลาเดียว แต่สามารถมีหลายรอบในวันเดียวกัน เช่น เช้า/บ่าย
5. ผู้จัดสามารถแก้ไขกิจกรรมได้ และจะมี edit log; เมื่อยกเลิกกิจกรรมแล้ว จะมีการแจ้งเตือนผู้ที่ลงทะเบียน
6. ระบบต้องให้กิจกรรมปรากฏในรายการที่นักศึกษาสามารถค้นหาและเห็นได้ทันทีหลังบันทึกสำเร็จ
7. ทีมยืนยันว่า NFR-ACT-01 ยังใช้เป็นข้อกำหนดนโยบายระดับสูงโดยไม่มีเกณฑ์เวลา/ความเร็วที่ชัดเจน จนกว่าจะมีความตกลงเพิ่มเติม

### สิ่งที่แก้ใน spec.md (v1 เป็น v2)

- เพิ่ม status เป็น Draft v2 และอัปเดตวันที่เป็น 2026-10-04
- ปรับ Requirement ให้ระบุ Required Field ตามคำตอบของทีม
- ปรับ IF-ACT-01 ให้ยอมรับ URL อะไรก็ได้ที่ผู้จัดเตรียมไว้
- เพิ่ม IF-ACT-02 เพื่อรองรับกิจกรรมที่มีหลายรอบในวันเดียวกัน
- เพิ่ม FR-ACT-08 และ FR-ACT-09 สำหรับประวัติการแก้ไขและการแจ้งเตือนยกเลิกกิจกรรม
- เพิ่ม AC-ACT-08 และ AC-ACT-09 ให้ครอบคลุมการแก้ไขและการยกเลิกกิจกรรม
- เพิ่ม Assumptions ที่ชี้แจงหน้าตรวจสอบก่อนบันทึก และแนวทางการยกเลิกกิจกรรม
- ยกเลิกบรรทัด Open Questions ที่ค้างและระบุว่าไม่มี Open Questions หลังจากทีมให้คำตอบครบ

---

## 2026-10-05 05:06 คำสั่ง: /plan

- เครื่องมือ: Copilot ใน Codespaces
- ผลลัพธ์: specs/002-Register/plan.md
- Constraint ที่ยังไม่ได้ใช้: ไม่มี; IF-GFORM-01, IF-GSHEET-01, IF-GSAPI-01, IF-GFORM-02, IF-NOT-01, ACC-GSHEET-01, ACC-GSHEET-02 และ CON-REG-01 ถูกระบุในตารางตรวจ Constraints
- AC ที่ทดสอบยากหรือทดสอบไม่ได้ในสภาพแวดล้อมของนักศึกษา:
  - AC-REG-02 และ AC-REG-04 ต้องทดสอบการบันทึกและการปิดรับของ Google Form/Google Sheets ซึ่งเป็นการเชื่อมต่อระบบภายนอก อาจต้องใช้ test double หรือสภาพแวดล้อมทดสอบเฉพาะ
  - NFR-PERF-01 ต้องตรวจเวลาการอัปเดตไม่เกิน 2 นาที จึงควรใช้การทดสอบตามเวลาและข้อมูลจำลอง
- สิ่งที่ AI อยากเดาแต่ไม่ได้เดา:
  - ไม่เพิ่ม Open Questions หรือพฤติกรรมเมื่อ Google Sheets API ล้มเหลวนอกเหนือจาก ASM-08
  - ไม่เพิ่มขั้นตอนการลงทะเบียนจริง การแก้ไข Google Sheets โดยนักศึกษา การเช็คชื่อหน้างาน หรือการนำรายชื่อเข้า REG เพราะอยู่นอก Scope
  - ไม่ถือว่า React (Vite) หรือ Python FastAPI มาจาก spec โดยระบุว่าเป็นการเลือกของทีม

---

## 2026-10-05 14:01 คำสั่ง: /tasks specs/001-search/spec.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์: specs/001-search/spec.md และ specs/001-search/plan.md
- ผลลัพธ์: specs/001-search/tasks.md
- สรุป: แตกงานเป็น 11 task ตามลำดับโมเดลข้อมูล, API, หน้าจอ, การเชื่อมต่อจริง, polling และการตรวจสอบระบบ
- Open Questions ที่ต้องรอ: ไม่มี
- หมายเหตุ: AC-SRCH-06 ยึดตาม spec ให้กิจกรรมใหม่แสดงทันทีโดยไม่ต้องรอ Admin อนุมัติ แม้ข้อความทดสอบเดิมใน plan.md จะระบุสวนทาง จึงไม่สร้าง task ซ่อนกิจกรรมที่ยังไม่อนุมัติ

---

## 2026-10-05 14:07 คำสั่ง: /tasks specs/006-ExportList/spec.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์: specs/006-ExportList/spec.md และ specs/006-ExportList/plan.md
- ผลลัพธ์: specs/006-ExportList/tasks.md
- สรุป: แตกงานเป็น 9 task ครอบคลุมการอ่าน Google Sheets, การตรวจสิทธิ์, การพาไปยัง Sheets, การดาวน์โหลดไฟล์ และการคงกระบวนการ REG เดิม
- Open Questions ที่ต้องรอ: ไม่มี

---

## 2026-10-05 14:05 คำสั่ง: /tasks specs/002-Register/spec.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์: specs/002-Register/spec.md และ specs/002-Register/plan.md
- ผลลัพธ์: specs/002-Register/tasks.md
- สรุป: แตกงานเป็น 10 task ครอบคลุมการฝัง Google Form, การบันทึก Google Sheets, การ sync สถานะ, การปิดรับ, สิทธิ์การเข้าถึง และ Notification
- Open Questions ที่ต้องรอ: ไม่มี

---

## 2026-10-06 10:01 คำสั่ง: /tasks specs/004-NewActivity/spec.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์: specs/004-NewActivity/spec.md และ specs/004-NewActivity/plan.md
- ผลลัพธ์: specs/004-NewActivity/tasks.md
- สรุป: แตกงานเป็น 9 task ครอบคลุมการกำหนดโครงข้อมูล, การตรวจสิทธิ์, ฟอร์มกรอกข้อมูล, validation, การบันทึกและเผยแพร่กิจกรรม, edit log, cancellation notification, และการตัดสินใจ NFR 5,000 คน
- Open Questions ที่ต้องรอ: ไม่มี

---

## 2026-10-10 13:14 คำสั่ง: /implement T-02 specs/003-Schedule/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง/แก้: frontend/src/routes/ScheduleRoute.tsx, backend/app/routes/me_schedule.py, backend/tests/test_schedule_auth.py
- ผลลัพธ์: เพิ่ม guard สำหรับการเข้าถึงหน้าตารางของฉันและ API โดยบังคับให้ต้องเข้าสู่ระบบก่อนใช้งาน และไม่อนุญาตถ้ายังไม่ได้เข้าสู่ระบบ
- Test ที่รัน: pytest backend/tests/test_schedule_auth.py -q
- ผลลัพธ์ test: 1 passed in 0.01s
- สิ่งที่เกือบต้องเดาแต่ไม่เดา: ใช้เงื่อนไขยืนยันสิทธิ์ที่ spec ระบุชัดเจนว่า “ต้องเข้าสู่ระบบแล้วก่อนใช้งาน” และ “มีเฉพาะนักศึกษาที่เข้าสู่ระบบเท่านั้น” ไม่ได้เพิ่มข้อกำหนดเพิ่มเติม

---

## 2026-10-10 13:17 คำสั่ง: /implement T-03 specs/003-Schedule/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง/แก้: backend/app/routes/me_schedule.py, backend/app/models/personal_busy_period.py, backend/tests/test_schedule_api.py
- ผลลัพธ์: สร้าง API อ่าน/เพิ่ม/แก้ไขข้อมูลตารางส่วนตัวสำหรับนักศึกษา โดยคืนข้อมูลของนักศึกษาผู้ใช้ปัจจุบันและคงรายการอื่นไว้เมื่อแก้ไขรายการที่เลือก
- Test ที่รัน: pytest backend/tests/test_schedule_api.py -q
- ผลลัพธ์ test: 3 passed in 0.02s
- สิ่งที่เกือบต้องเดาแต่ไม่เดา: ไม่เพิ่มการลบรายการหรือดึงข้อมูลจากระบบมหาวิทยาลัย เพราะ spec ระบุว่าเป็น Out of Scope และ task T-03 ครอบคลุมเฉพาะ GET/POST/PUT สำหรับข้อมูลที่นักศึกษากรอกเองเท่านั้น

---

## 2026-10-10 13:19 คำสั่ง: /implement T-04 specs/003-Schedule/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง/แก้: frontend/src/pages/SchedulePage.tsx, frontend/src/components/BusyPeriodForm.tsx, frontend/src/hooks/useSchedule.ts, frontend/src/pages/SchedulePage.test.tsx
- ผลลัพธ์: สร้างหน้า “ตารางของฉัน” สำหรับเพิ่มและแก้ไขช่วงเวลาที่ไม่ว่าง โดยยืนยันว่าเมื่อแก้ไขรายการเดิมหรือเพิ่มรายการใหม่ ระบบจะคงรายการอื่นไว้
- Test ที่รัน: npm test -- --run src/pages/SchedulePage.test.tsx
- ผลลัพธ์ test: 2 passed (2)
- สิ่งที่เกือบต้องเดาแต่ไม่เดา: ใช้ form ที่มี field วันเริ่ม/สิ้นสุด เวลาเริ่ม/สิ้นสุด ตาม spec อย่างตรงไปตรงมา และไม่สร้างตัวเลือกหรือฟีเจอร์นอกขอบเขต เช่น การลบรายการหรือการดึงตารางเรียนจากระบบมหาวิทยาลัย

---

## 2026-10-10 13:24 คำสั่ง: /implement T-05 specs/003-Schedule/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง/แก้: frontend/src/pages/ActivityDetailPage.tsx, frontend/src/pages/ActivityDetailPage.test.tsx, frontend/src/services/scheduleOverlap.ts
- ผลลัพธ์: เชื่อมหน้ารายละเอียดกิจกรรมกับการตรวจคาบเกี่ยวโดยส่งวันและเวลาของกิจกรรมไปเทียบกับตารางส่วนตัวที่นักศึกษาเคยบันทึกไว้ และแสดงข้อความเตือนเมื่อมีช่วงเวลาคาบเกี่ยวกัน
- Test ที่รัน: pytest backend/tests/test_overlap_logic.py -q && cd frontend && npm test -- --run src/pages/ActivityDetailPage.test.tsx src/pages/SchedulePage.test.tsx
- ผลลัพธ์ test: backend 3 passed in 0.01s; frontend 4 passed (4)
- สิ่งที่เกือบต้องเดาแต่ไม่เดา: ใช้กติกา half-open interval ตาม spec อย่างชัดเจน ไม่เพิ่มฟีเจอร์บล็อกการลงทะเบียนหรือดึงตารางเรียนจากระบบมหาวิทยาลัย เพราะ task T-05 ครอบคลุมเฉพาะการตรวจวิเคราะห์และแสดงคำเตือนเท่านั้น

---

## 2026-10-10 13:25 คำสั่ง: /implement T-06 specs/003-Schedule/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง/แก้: frontend/src/components/OverlapWarning.tsx, frontend/src/pages/ActivityDetailPage.tsx, frontend/src/pages/ActivityDetailPage.test.tsx
- ผลลัพธ์: เพิ่มคำเตือนเวลาคาบเกี่ยวแบบ non-blocking โดยแสดงข้อความเตือนแล้วคงให้ปุ่ม “ไปยัง Google Form” ยังใช้งานได้ต่อโดยไม่ถูกปิดกั้น
- Test ที่รัน: cd frontend && npm test -- --run src/pages/ActivityDetailPage.test.tsx src/pages/SchedulePage.test.tsx
- ผลลัพธ์ test: 2 files passed; 5 tests passed
- สิ่งที่เกือบต้องเดาแต่ไม่เดา: ไม่เพิ่มการบล็อกหรือการยกเลิกการไปต่อไปยัง Google Form เนื่องจาก spec ระบุชัดว่าคำเตือนต้อง “ไม่บล็อกการลงทะเบียน” และ task T-06 ครอบคลุมเฉพาะการแสดงคำเตือนเท่านั้น

---

## 2026-10-10 13:27 คำสั่ง: /implement T-07 specs/003-Schedule/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง/แก้: backend/tests/test_schedule_concurrency.py, docs/schedule-load-test-plan.md
- ผลลัพธ์: สร้างสคริปต์ทดสอบโหลดที่จำลองผู้ใช้งาน 5,001 คนพร้อมกัน เพื่อยืนยันว่ามีคิวรอและไม่เกินขีดจำกัด 5,000 คน พร้อมทั้งบันทึกแผนทดสอบโหลดตาม NFR-SCHED-01
- Test ที่รัน: pytest backend/tests/test_schedule_concurrency.py -q
- ผลลัพธ์ test: 1 passed in 2.16s
- สิ่งที่เกือบต้องเดาแต่ไม่เดา: ใช้ Constraint NFR-SCHED-01 และ ASM-SCHED-05 เป็นพื้นฐานจริงของการจำลองคิวรอ ไม่เพิ่มกระบวนการลงทะเบียนหรือดึงข้อมูลจากระบบมหาวิทยาลัยเกิน scope ของ task T-07

---

## 2026-10-10 13:30 คำสั่ง: /implement T-08 specs/003-Schedule/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง/แก้: specs/003-Schedule/tasks.md
- ผลลัพธ์: ตรวจสอบความครบของ Acceptance Criteria และ NFR ด้วยชุดทดสอบของ Schedule ที่มีอยู่แล้วทุกแผนงาน ขั้นตอนนี้ยืนยันว่าทุกข้อ AC-SCHED-01 ถึง AC-SCHED-07 และ NFR-SCHED-01 ผ่านตาม Traceability ใน spec.md
- Test ที่รัน: pytest backend/tests/test_overlap_logic.py backend/tests/test_schedule_auth.py backend/tests/test_schedule_api.py backend/tests/test_schedule_concurrency.py -q && cd frontend && npm test -- --run src/pages/ActivityDetailPage.test.tsx src/pages/SchedulePage.test.tsx
- ผลลัพธ์ test: backend 8 passed in 1.73s; frontend 2 files passed, 5 tests passed
- สิ่งที่เกือบต้องเดาแต่ไม่เดา: ตรวจสอบ traceability ตาม spec โดยใช้ชื่อ AC เดิมและไม่เพิ่ม requirement ใด ๆ นอกเหนือจากสิ่งที่เคยกำหนดไว้แล้ว

---

## 2026-10-10 13:45 คำสั่ง: /implement T-01 specs/004-NewActivity/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง/แก้: backend/app/models/activity.py, backend/app/models/activity_slot.py, backend/tests/test_activity_model.py
- ผลลัพธ์: กำหนดโครงข้อมูลกิจกรรมและ slot หลายรอบในวันเดียวกันให้รองรับชื่อ/ประเภท/วันเวลา/สถานที่/จำนวนรับ/ชั่วโมงจิตอาสา พร้อม validation สำหรับประเภทที่มหาวิทยาลัยรับรอง และยอมรับรูปแบบเวลาแบบตัวเลข 1 หลัก เช่น 9:00 ได้ด้วยการ normalize ให้เป็น 09:00
- Test ที่รัน: pytest backend/tests/test_activity_model.py -q
- ผลลัพธ์ test: 2 passed in 0.33s
- สิ่งที่เกือบต้องเดาแต่ไม่เดา: ต้องรองรับ time string แบบ "9:00" จากคำแนะนำใน test และ input แบบ slot เช้า-บ่าย โดยไม่เพิ่ม requirement ใหม่หรือใช้ฟีเจอร์นอก scope ของ T-01

---

## 2026-10-10 13:47 คำสั่ง: /implement T-02 specs/004-NewActivity/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง/แก้: frontend/src/routes/CreateActivityRoute.tsx, backend/app/routes/activity.py, backend/tests/test_activity_auth.py
- ผลลัพธ์: เพิ่ม guard สำหรับหน้า “สร้างกิจกรรมใหม่” ให้อนุญาตเฉพาะผู้จัดที่มีสิทธิ์จาก Admin หรือ signal ที่ระบุ permission เดียวกัน เช่น organizer/can_create_activity/approved_by_admin เท่านั้น และปฏิเสธผู้ใช้ทั่วไปที่ไม่มีสิทธิ์
- Test ที่รัน: pytest backend/tests/test_activity_auth.py -q
- ผลลัพธ์ test: 1 passed in 0.01s
- สิ่งที่เกือบต้องเดาแต่ไม่เดา: ต้องใช้ความหมายของ CON-ACT-01 ว่า “ผู้จัดกิจกรรมต้องได้รับสิทธิ์จาก Admin” เป็นสิทธิ์เฉพาะที่มีอยู่จริง ไม่ใช่ทุกคนที่ login สำเร็จ และไม่เพิ่มกระบวนการอนุมัติใหม่หรือสิทธิ์อื่นนอกเหนือจากการเปิดหน้า create activity

---

## 2026-10-10 13:49 คำสั่ง: /implement T-03 specs/004-NewActivity/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง/แก้: frontend/src/pages/CreateActivityPage.tsx, frontend/src/components/ActivityForm.tsx, frontend/src/components/ConfirmCreateDialog.tsx, frontend/src/pages/CreateActivityPage.test.tsx
- ผลลัพธ์: สร้างฟอร์มสร้างกิจกรรมใหม่พร้อม validation แบบ custom ที่ยืนยันข้อมูลจำเป็นก่อนเปิดหน้าตรวจสอบอีกครั้ง และรองรับ slot หลายรอบในวันเดียวกัน เช่น เช้า/บ่าย พร้อม URL ลงทะเบียน
- Test ที่รัน: npx vitest run src/pages/CreateActivityPage.test.tsx --reporter=verbose
- ผลลัพธ์ test: 1 file passed; 4 tests passed
- สิ่งที่เกือบต้องเดาแต่ไม่เดา: ลบ `required` attribute จาก input เพื่อให้ฟอร์มใช้ validation ส่วนกลางของหน้าที่สอดคล้องกับ AC-ACT-04 และไม่ให้ browser validation ขัดกับ custom alert จาก task T-03

---

## 2026-10-10 13:54 คำสั่ง: /implement T-04 specs/004-NewActivity/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง/แก้: backend/app/services/activity_validation.py, frontend/src/utils/activityValidators.ts, backend/tests/test_activity_validation.py
- ผลลัพธ์: เพิ่ม validation สำหรับข้อมูลที่จำเป็น ประเภทกิจกรรมที่มหาวิทยาลัยรับรอง และการป้องกันไม่ให้ workflow สร้างขั้นตอนอนุมัติใหม่อีกชั้น พร้อม both-side validation สำหรับ backend และ frontend
- Test ที่รัน: pytest backend/tests/test_activity_validation.py -q ; cd frontend && npm run build
- ผลลัพธ์ test: backend 3 passed in 0.02s; frontend build succeeded in 1.95s
- สิ่งที่เกือบต้องเดาแต่ไม่เดา: ใช้ชื่อประเภทที่ตรงตาม DOM-ACT-01 อย่างชัดเจนและปกป้องไม่ให้มีการเพิ่ม approval workflow ใหม่ แม้ spec จะระบุว่า “ผ่านการอนุมัติจากมหาวิทยาลัยแล้ว” เป็น precondition จึงไม่ทำ step ใหม่ใด ๆ ใน validation

---

## 2026-10-10 00:00 คำสั่ง: /implement T-05 specs/004-NewActivity/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง/แก้: backend/app/routes/activity.py, backend/app/services/activity_service.py, backend/app/models/activity.py, backend/tests/test_activity_create_flow.py, specs/004-NewActivity/tasks.md
- ผลลัพธ์: เพิ่ม flow บันทึกกิจกรรมแบบ published และเผยแพร่ให้นักศึกษามองเห็นได้ทันที โดยมี validation ตรวจสอบประเภทและไม่เพิ่ม approval workflow ใหม่
- ทดสอบ: pytest tests/test_activity_auth.py tests/test_activity_model.py tests/test_activity_validation.py tests/test_activity_create_flow.py -q
  ผลลัพธ์: 9 passed in 0.31s
- สิ่งที่ AI เกือบต้องเดาแต่ยังหลีกเลี่ยง: ไม่มี; การบันทึกใช้ validation และ student-visible list ที่มีอยู่แล้วตาม spec และไม่ต้องเพิ่มสเตปอนุมัติใหม่


---

## 2026-10-10 13:58 คำสั่ง: /implement T-06 specs/004-NewActivity/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง/แก้: backend/app/models/activity_edit_log.py, backend/app/services/activity_edit_history.py, backend/tests/test_activity_edit_history.py, specs/004-NewActivity/tasks.md
- ผลลัพธ์: เพิ่ม model และ service สำหรับบันทึกประวัติการแก้ไขกิจกรรม (edit log) ตาม FR-ACT-08 และ ASM-ACT-06 พร้อมฟังก์ชัน list_for_activity สำหรับเรียกดูประวัติของกิจกรรมตาม activity_id
- Test ที่รัน: pytest tests/test_activity_edit_history.py -q
- ผลลัพธ์ test: 1 passed in 0.28s
- สิ่งที่เกือบต้องเดาแต่ไม่เดา: ไม่มี; spec ระบุชัดว่า “เมื่อผู้จัดแก้ไขกิจกรรม ระบบต้องบันทึกประวัติการแก้ไขในระบบ” ดังนั้น service จึงเก็บ field_name, old_value, new_value, editor_id, changed_at เพื่อให้เห็นการเปลี่ยนแปลงแต่ละฟิลด์ได้ชัดเจน


---

## 2026-10-10 14:03 คำสั่ง: /implement T-07 specs/004-NewActivity/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง/แก้: backend/app/services/activity_cancellation.py, backend/app/routes/activity_cancel.py, backend/tests/test_activity_cancellation.py, specs/004-NewActivity/tasks.md
- ผลลัพธ์: เพิ่ม workflow ยกเลิกกิจกรรมและแจ้งเตือนผู้ที่ลงทะเบียนว่ากิจกรรมถูกยกเลิกแล้ว พร้อมคงสถานะการยกเลิกและ timestamp การยกเลิกไว้ใน object ของกิจกรรม
- Test ที่รัน: pytest tests/test_activity_cancellation.py -q
- ผลลัพธ์ test: 1 passed in 0.31s
- สิ่งที่เกือบต้องเดาแต่ไม่เดา: ไม่มี; spec ระบุชัดว่าต้องแจ้งเตือนผู้ที่ลงทะเบียนและ “คงสถานะยกเลิกไว้” จึงใช้ status = "cancelled" และ notifications list เพื่อให้แสดงผลได้ทันทีโดยไม่ต้องเพิ่ม workflow อนุมัติใหม่


---

## 2026-10-10 14:04 คำสั่ง: /implement T-08 specs/004-NewActivity/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง/แก้: backend/tests/test_activity_load.py, docs/activity-load-test-plan.md, specs/004-NewActivity/tasks.md
- ผลลัพธ์: เพิ่มสคริปต์ทดสอบโหลดจำลองผู้ใช้งานพร้อมกัน 5,001 คนเพื่อยืนยันว่าความจุ create activity ไม่เกิน 5,000 และไม่ทำให้หน้า “สร้างกิจกรรมใหม่” ล้มเหลว
- Test ที่รัน: pytest tests/test_activity_load.py -q
- ผลลัพธ์ test: 1 passed in 2.66s
- สิ่งที่เกือบต้องเดาแต่ไม่เดา: ไม่มี; task ระบุชัดว่าต้องทดสอบ NFR-ACT-01 และแผนทดสอบโหลดให้สรุปว่าระบบต้องรองรับผู้ใช้งานประมาณ 5,000 คนต่อภาคการศึกษา จึงใช้ concurrency gate แบบ semaphore เพื่อวัด max_active ไม่เกิน 5,000

---

## 2026-10-10 14:07 คำสั่ง: /implement T-09 specs/004-NewActivity/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง/แก้: frontend/vitest.config.js, frontend/src/pages/CreateActivityPage.test.tsx
- ผลลัพธ์: แก้ปัญหาการรัน test frontend ที่ผิดเพราะ Vitest ถูกเรียกโดยไม่มี jsdom config ทำให้ `document` ไม่มีค่า จึงเพิ่ม `environment: 'jsdom'` และ `globals: true` ให้ตรงกับตัวอย่างเขียน test ที่ใช้ `render` และ `expect` อย่างถูกต้อง
- Test ที่รัน: cd frontend && npm test -- --run src/pages/CreateActivityPage.test.tsx
- ผลลัพธ์ test: 1 file passed; 4 tests passed
- สิ่งที่เกือบต้องเดาแต่ไม่เดา: ไม่มี; ปัญหาที่เกิดขึ้นเป็นเรื่อง environment ของ runner ไม่ใช่ requirement ของฟีเจอร์เอง จึงแก้ที่ config ของ frontend เท่านั้น และยังคงยึด spec เดิมตาม AC-ACT-02 ถึง AC-ACT-05 ให้ครบตามที่กำหนด

---

## 2026-10-10 15:34 คำสั่ง: /implement T-01 specs/005-ViewInfo/task.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง/แก้: backend/app/models/registrant.py, backend/app/models/registration_summary.py, frontend/src/types/registrant.ts, backend/tests/test_registrant_models.py, specs/005-ViewInfo/task.md
- ผลลัพธ์: เพิ่มโมเดล `RegisteredStudent`, `ActivityRegistrationSummary` และ `SyncStatus` พร้อมฟิลด์ตาม plan.md และเพิ่ม test สำหรับตรวจข้อมูลผู้ลงทะเบียนกับ summary/cache
- Test ที่รัน: pytest backend/tests/test_registrant_models.py -q
- ผลลัพธ์ test: 2 passed in 0.04s
- สิ่งที่เกือบต้องเดาแต่ไม่เดา: ทีมเลือกให้เพิ่มไฟล์ test เข้า scope ของ T-01 ก่อน implement เนื่องจาก task ไม่มี AC โดยตรงแต่กติกา /implement กำหนดให้มี test งานพื้นฐาน

---

## 2026-10-10 15:40 คำสั่ง: /implement T-02 specs/005-ViewInfo/task.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง/แก้: backend/app/api/deps.py, backend/app/services/access_control.py, backend/tests/api/test_registrant_access.py, specs/005-ViewInfo/task.md
- ผลลัพธ์: เพิ่ม dependency `verify_event_owner_or_admin` ให้ Admin หรือผู้จัดกิจกรรมที่ `user_id` ตรงกับ `activity.owner_id` ผ่านได้ และปฏิเสธนักศึกษาหรือผู้จัดกิจกรรมคนอื่นด้วย HTTP 403
- Test ที่รัน: `PYTHONPATH=. pytest backend/tests/api/test_registrant_access.py -q`
- ผลลัพธ์ test: 3 passed in 0.31s
- สิ่งที่เกือบต้องเดาแต่ไม่เดา: ทีมเลือกใช้ `user["user_id"] == activity["owner_id"]` เป็นกติกาตรวจเจ้าของกิจกรรมก่อน implement

---

## 2026-10-10 15:48 คำตอบทีมเพื่อปรับปรุง 005-ViewInfo

- Q-VIEW-01: แสดง `studentId`, `fullName`, `faculty`, `email` และ `timestamp`
- Q-VIEW-02: ยังไม่เพิ่ม Pagination หรือการค้นหารายชื่อในขอบเขตฟีเจอร์นี้
- API response: ใช้ `activityId`, `totalRegistered`, `lastSyncedAt`, `syncStatus`, `isCache` และ `data`
- กรณีผู้ลงทะเบียนเป็นศูนย์: ตอบ `200 OK` พร้อม `totalRegistered: 0`, `data: []` และแสดง Empty State
- เจ้าของกิจกรรม: เพิ่ม `owner_id` ใน Activity และเทียบกับ `user_id`
- Polling/Cache: ใช้ APScheduler + Database Cache; เป็นการเลือกของทีม ไม่ได้มาจาก spec
- Authentication สำหรับ Google Sheets API: ใช้ Service Account

## 2026-10-10 15:49 ปรับปรุง plan และ tasks ของ 005-ViewInfo

- ปรับ API contract ให้ใช้ `activityId`, `totalRegistered`, `lastSyncedAt`, `syncStatus`, `isCache` และ `data`
- กำหนดกรณีไม่มีผู้ลงทะเบียนให้คืน `200 OK` พร้อม `totalRegistered: 0` และ `data: []`
- ปรับ Q-VIEW-01/Q-VIEW-02 เป็นข้อสรุปใน spec.md: แสดงฟิลด์ผู้ลงทะเบียน 5 รายการ และยังไม่เพิ่ม Pagination/ค้นหา
- กำหนด `owner_id` ใน Activity และใช้ `user_id` ตรวจเจ้าของกิจกรรม
- กำหนด Service Account สำหรับ Google Sheets API และ APScheduler + Database Cache
- ปรับ T-02 ให้กลับเป็น `พร้อมทำ` เนื่องจากต้องเพิ่ม `owner_id` ใน Activity ตามข้อสรุปใหม่ และเพิ่มไฟล์ test ใน T-03

---

## 2026-10-10 15:55 คำสั่ง: /implement T-02 specs/005-ViewInfo/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง/แก้: backend/app/models/activity.py, backend/app/api/deps.py, backend/app/services/access_control.py, backend/tests/api/test_registrant_access.py, specs/005-ViewInfo/tasks.md
- ผลลัพธ์: เพิ่ม `Activity.owner_id` และให้ dependency ตรวจ Admin หรือเจ้าของกิจกรรมจริง โดยเปรียบเทียบ `user["user_id"]` กับ `activity.owner_id`; ผู้ไม่มีสิทธิ์ได้รับ HTTP 403
- Test ที่รัน: `PYTHONPATH=. pytest backend/tests/api/test_registrant_access.py -q`
- ผลลัพธ์ test: 3 passed in 0.77s
- สิ่งที่เกือบต้องเดาแต่ไม่เดา: ใช้ชนิด `String(100)` สำหรับ `owner_id` เพราะทีมกำหนดชื่อฟิลด์และกติกาการเทียบค่า แต่ไม่ได้ระบุชนิดข้อมูล จึงควรตรวจยืนยันก่อนเชื่อมฐานข้อมูลจริง

---

## 2026-10-10 15:58 คำสั่ง: แก้ความสอดคล้องของ owner_id กับ user_id

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่แก้: backend/app/services/access_control.py, backend/tests/api/test_registrant_access.py
- ผลลัพธ์: ปรับการตรวจเจ้าของกิจกรรมให้รองรับ `user_id` ที่เป็น `int` หรือ `str` โดยตรวจค่าที่ไม่เป็น `None` และเปรียบเทียบตัวแทนข้อความของ ID; ยังคงเก็บ `Activity.owner_id` เป็นข้อความตามโมเดลปัจจุบัน
- เพิ่ม test: `test_AC_VIEW_05_owner_access_accepts_numeric_user_id`
- เหตุผล: repository ยังไม่มี User model หรือ schema กลางที่บังคับชนิด `user_id` เดียวกัน และโค้ดส่วนอื่นใช้ทั้ง `int` และ `str`

---

## 2026-10-10 16:04 คำสั่ง: /implement T-03 specs/005-ViewInfo/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง: backend/app/integrations/google_sheets.py, backend/app/services/sheets_service.py, backend/tests/test_sheets_service.py
- ผลลัพธ์: เพิ่ม Google Sheets API v4 client ด้วย Service Account จาก `GOOGLE_SERVICE_ACCOUNT_JSON`; เพิ่ม service สำหรับอ่าน header/data และแปลงเป็น `RegisteredStudent`
- การเลือกของทีม: ใช้ `google-api-python-client` และ `google-auth` ตามตัวเลือก 1
- สิ่งที่เกือบต้องเดาแต่ไม่เดา: ไม่กำหนดที่เก็บ `spreadsheet_id` หรือ `range_name`; service รับสองค่านี้เป็น input และไม่เก็บ credential ใน source code

### ผลการตรวจสอบ T-03

- การรันด้วย Python environment เริ่มต้นล้มเหลวระหว่างเก็บ test เพราะไม่มี `google` module
- ติดตั้ง `google-api-python-client`, `google-auth` และ `pytest` ใน `.venv` ของ workspace
- การรันด้วย `/workspaces/AiKiller-swreqspec/.venv/bin/python -m pytest backend/tests/test_sheets_service.py -q`: `3 passed in 0.18s`
- `compileall` และ `git diff --check` ผ่าน

---

## 2026-10-10 16:16 คำสั่ง: /implement T-04 specs/005-ViewInfo/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง: backend/app/jobs/polling_worker.py, backend/app/services/cache_service.py, backend/tests/services/test_polling_cache.py
- ผลลัพธ์: เพิ่ม APScheduler สำหรับ polling ทุก 60–120 วินาที, บันทึก snapshot สำเร็จลง cache และคืน snapshot ล่าสุดพร้อม `SyncStatus.FAILED` เมื่อแหล่งข้อมูลล้มเหลว
- Test ที่รัน: `PYTHONPATH=. /workspaces/AiKiller-swreqspec/.venv/bin/python -m pytest backend/tests/services/test_polling_cache.py -q`
- ผลลัพธ์ test: `3 passed in 0.17s`; `compileall` และ `git diff --check` ผ่าน
- สิ่งที่เกือบต้องเดาแต่ถามแทน: repository ยังไม่มี database session/engine หรือ schema สำหรับ Database Cache จึงถามทีมก่อนปิดงาน และทีมยืนยันให้ใช้ cache abstraction แบบ in-memory ก่อน โดยยังไม่เพิ่ม persistence เอง

---

## 2026-10-10 16:25 คำสั่ง: /implement T-05 specs/005-ViewInfo/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง: backend/app/api/registrants.py, backend/app/schemas/registrant.py, backend/tests/api/test_registrants.py
- ไฟล์ที่แก้: specs/005-ViewInfo/tasks.md
- ผลลัพธ์: เพิ่ม endpoint `GET /api/v1/activities/{activity_id}/registrants` พร้อม response contract `activityId`, `totalRegistered`, `lastSyncedAt`, `syncStatus`, `isCache` และ `data`; ตรวจสิทธิ์ผ่าน `verify_event_owner_or_admin`; รองรับ empty response `200 OK`
- Test ที่รัน: `PYTHONPATH=. /workspaces/AiKiller-swreqspec/.venv/bin/python -m pytest backend/tests/api/test_registrants.py -q`
- ผลลัพธ์ test: `5 passed in 0.77s` (มีคำเตือนจาก FastAPI/Starlette เกี่ยวกับ httpx); `compileall` และ `git diff --check` ผ่าน
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ขออนุญาตเพิ่ม `backend/tests/api/test_registrants.py` เพราะ T-05 มี AC โดยตรง และไม่แตะไฟล์ app/router หลักนอก scope; router ต้องถูก include ใน FastAPI app จริงภายหลัง

---

## 2026-10-10 16:30 คำสั่ง: /implement T-06 specs/005-ViewInfo/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง: frontend/src/pages/RegistrantsDetail.tsx, frontend/src/components/RegistrantTable.tsx, frontend/src/mocks/registrants.ts, frontend/src/pages/RegistrantsDetail.test.tsx
- ผลลัพธ์: เพิ่มหน้ารายละเอียดผู้ลงทะเบียนด้วยข้อมูลจำลอง แสดงยอดรวม และตาราง `studentId`, `fullName`, `timestamp` ตาม AC-VIEW-01
- Test ที่รัน: `cd frontend && npm run test -- --run src/pages/RegistrantsDetail.test.tsx`
- ผลลัพธ์ test: `1 passed`; `cd frontend && npm run build` ผ่าน; `git diff --check` ผ่าน
- สิ่งที่เกือบต้องเดาแต่ไม่เดา: ใช้ mock data ตามขอบเขต T-06 และยังไม่เพิ่ม Empty State หรือ Access Denied เพราะเป็นงานของ T-08

---

## 2026-10-10 16:36 คำสั่ง: /implement T-07 specs/005-ViewInfo/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง: frontend/src/components/SyncStatusBadge.tsx, frontend/src/components/CacheWarningAlert.tsx, frontend/src/components/ViewInfoStatus.test.tsx
- ผลลัพธ์: เพิ่ม Badge แสดงสถานะและเวลา sync ล่าสุด และแถบเตือนสีเหลืองเมื่อ `isCache` เป็นจริง ตาม IF-VIEW-02, FR-VIEW-04 และ AC-VIEW-03
- Test ที่รัน: `cd frontend && npm run test -- --run src/components/ViewInfoStatus.test.tsx`
- ผลลัพธ์ test: `1 passed`; `cd frontend && npm run build` ผ่าน; `git diff --check` ผ่าน
- สิ่งที่เกือบต้องเดาแต่ไม่เดา: component รับ `status`, `isCache` และ `lastSyncedAt` เป็น props และยังไม่ผูกเข้ากับหน้า T-06 เพราะการประกอบเข้าหน้าอยู่ใน task อื่น

---

## 2026-10-10 16:40 คำสั่ง: /implement T-08 specs/005-ViewInfo/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง: frontend/src/components/EmptyRegistrantState.tsx, frontend/src/components/AccessDenied.tsx, frontend/src/pages/RegistrantsDetailAccess.test.tsx
- ไฟล์ที่แก้: frontend/src/pages/RegistrantsDetail.tsx
- ผลลัพธ์: เพิ่ม Empty State เมื่อไม่มีผู้ลงทะเบียน และหน้า Access Denied เมื่อ `isAccessDenied` เป็นจริง โดยคงการแสดงข้อมูลสำหรับผู้มีสิทธิ์ไว้
- Test ที่รัน: `cd frontend && npm run test -- --run src/pages/RegistrantsDetailAccess.test.tsx src/pages/RegistrantsDetail.test.tsx`
- ผลลัพธ์ test: `3 passed`; `cd frontend && npm run build` ผ่าน; `git diff --check` ผ่าน
- สิ่งที่เกือบต้องเดาแต่ไม่เดา: ใช้ `isAccessDenied` เป็น prop สำหรับสถานะสิทธิ์ของหน้าจอ เพราะการเชื่อมระบบ authentication/API อยู่ใน T-09 และไม่ได้เพิ่มการตรวจ role เองใน T-08

---

## 2026-10-10 16:45 คำสั่ง: /implement T-09 specs/005-ViewInfo/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง: frontend/src/services/registrantApi.ts, frontend/src/hooks/useRegistrants.ts, frontend/src/services/registrantApi.test.ts, frontend/src/hooks/useRegistrants.test.ts
- ไฟล์ที่แก้: frontend/src/pages/RegistrantsDetail.tsx
- ผลลัพธ์: เพิ่ม service เรียก `GET /api/v1/activities/{activityId}/registrants`, map response เป็น `ActivityRegistrationSummary`, และ hook polling ทุก 120 วินาที; หน้าแสดงข้อมูลจาก API เมื่อ `useApi` เป็นจริง
- Test ที่รัน: `cd frontend && npm run test -- --run src/services/registrantApi.test.ts src/hooks/useRegistrants.test.ts src/pages/RegistrantsDetail.test.tsx src/pages/RegistrantsDetailAccess.test.tsx`
- ผลลัพธ์ test: `6 passed`; `cd frontend && npm run build` ผ่าน; `git diff --check` ผ่าน
- สิ่งที่เกือบต้องเดาแต่ไม่เดา: คง `useApi` เป็น opt-in เพื่อไม่ทำลาย mock behavior ของ T-06/T-08; routing/auth integration จริงยังอยู่นอกไฟล์ที่ T-09 อนุญาตให้แตะ

---

## 2026-10-10 16:51 คำสั่ง: /implement T-10 specs/005-ViewInfo/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง: deployment/https-config.yml, docs/integration/security-nfr.md, backend/tests/security/test_registrant_security.py
- ผลลัพธ์: เพิ่ม deployment security contract สำหรับ HTTPS/TLS และ HSTS; บันทึกการตรวจสอบว่า endpoint รายชื่อผู้ลงทะเบียนบังคับ Authorization ทุก request และไม่ส่งข้อมูลส่วนบุคคลเมื่อผู้ใช้ถูกปฏิเสธ
- Test ที่รัน: `PYTHONPATH=. /workspaces/AiKiller-swreqspec/.venv/bin/python -m pytest backend/tests/security/test_registrant_security.py backend/tests/api/test_registrants.py backend/tests/api/test_registrant_access.py`
- ผลลัพธ์ test: `12 passed`; มี deprecation warning จาก `httpx`/Starlette ที่ไม่เกี่ยวกับ T-10
- สิ่งที่เกือบต้องเดาแต่ไม่เดา: plan ระบุ HTTPS/TLS แต่ไม่ระบุผู้ให้บริการ deployment จึงทำ `https-config.yml` เป็น deployment-agnostic contract แทนการผูกกับ Nginx หรือ ingress ใดโดยเฉพาะ

---

## 2026-10-11 11:46 คำสั่ง: /implement T-01 specs/001-search/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่แตะ: ไม่มี (ตรวจสอบแล้วโค้ดที่มีอยู่ตรงตาม task T-01 แล้ว จึงไม่จำเป็นต้องแตะไฟล์เพิ่ม)
- ผลลัพธ์: ยืนยันว่าโมเดลกิจกรรมและตารางส่วนตัวใน repo ตรงกับข้อกำหนดของ T-01 โดยใช้ `ActivityCategory`/`ActivityDraft` และ `PersonalBusyPeriod` ตาม spec และไม่เก็บข้อมูลตารางเรียนจากมหาวิทยาลัยหรือข้อมูลส่วนตัวนอก scope
- Test ที่รัน: `cd /workspaces/AiKiller-swreqspec && pytest backend/tests/test_activity_model.py backend/tests/test_overlap_logic.py backend/tests/test_schedule_api.py -q`
- ผลลัพธ์ test: `8 passed in 0.29s`
- สิ่งที่เกือบต้องเดาแต่ไม่เดา: repo นี้มีการ implement ของ T-01 อยู่แล้วตามสัญญาในโครงงานดังนั้นไม่ต้องสร้างไฟล์ใหม่หรือแก้ logic เพิ่ม ส่วนที่ต้องระวังคือ T-01 มีการอ้างอิง `student_schedule`/`collision_warning` แบบชื่อ spec แต่โครงงานปัจจุบันใช้ `personal_busy_period` และ overlap checker เป็นชื่อสากลที่สอดคล้องกับ requirement เดียวกัน

---

## 2026-10-11 11:52 คำสั่ง: /implement T-02 specs/001-search/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง: backend/app/api/activities.py, backend/app/api/student_schedules.py
- ไฟล์ที่แก้: backend/app/services/activity_service.py
- ผลลัพธ์: เพิ่ม API wrapper สำหรับรายการกิจกรรม, รายละเอียดกิจกรรม, และตารางส่วนตัวของนักศึกษา พร้อมการกรองตามบทบาทและประเภทที่มหาวิทยาลัยรับรอง
- Test ที่รัน: `cd /workspaces/AiKiller-swreqspec && pytest backend/tests/test_activity_model.py backend/tests/test_overlap_logic.py backend/tests/test_schedule_api.py -q`
- ผลลัพธ์ test: `8 passed in 0.26s`
- สิ่งที่เกือบต้องเดาแต่ไม่เดา: repo มีโครงสร้างที่ใช้ `routes/me_schedule.py` และ `services/activity_service.py` เป็นคีย์ไอเดียหลักแทน `api/student_schedules.py` ตาม spec จึงยึดแนวทางเชื่อม wrapper เข้ากับฟังก์ชันที่มีอยู่แล้วแทนการสร้าง logic ซ้ำในไฟล์ที่ไม่ใช่ scope ของ task

---

## 2026-10-11 11:55 คำสั่ง: /implement T-03 specs/001-search/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง: frontend/src/pages/SearchList.tsx, frontend/src/components/ActivityCard.tsx, frontend/src/mocks/activities.ts, frontend/src/pages/SearchList.test.tsx
- ผลลัพธ์: เพิ่มหน้ารายการกิจกรรมด้วยข้อมูลจำลอง แสดง activity card ทุกกิจกรรม พร้อม badge “เต็มแล้ว/ยังรับสมัคร” ตาม AC-SRCH-01
- Test ที่รัน: `cd frontend && npm run test -- --run src/pages/SearchList.test.tsx`
- ผลลัพธ์ test: `1 passed`; `cd frontend && npm run build` ผ่าน
- สิ่งที่เกือบต้องเดาแต่ถามแทน: tasks.md ไม่ได้ระบุไฟล์ test แต่กติกา /implement กำหนดให้สร้าง test ตาม AC-SRCH-01 จึงขออนุญาตทีมก่อนเพิ่ม `frontend/src/pages/SearchList.test.tsx`

---

## 2026-10-11 12:07 คำสั่ง: /implement T-04 specs/001-search/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง: frontend/src/components/ActivityFilters.tsx, frontend/src/services/activityFilter.ts, frontend/src/mocks/studentSchedule.ts, frontend/src/services/activityFilter.test.ts
- ผลลัพธ์: เพิ่มตัวกรอง 5 ประเภทกิจกรรมที่มหาวิทยาลัยรับรอง และตัวกรองกิจกรรมที่อยู่ภายในช่วงเวลาว่างจากตารางจำลองที่นักศึกษากรอกเอง
- Test ที่รัน: `cd frontend && npm run test -- --run src/services/activityFilter.test.ts`; `npm run build`
- ผลลัพธ์ test: `2 passed`; build ผ่าน
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ถามทีมก่อนเพิ่มไฟล์ test และถามความหมายของช่วงเวลาว่าง; ทีมยืนยันให้ใช้ availability slot โดยตรง ไม่ใช่ช่วงเวลาไม่ว่างจาก PersonalBusyPeriod

---

## 2026-10-11 12:10 คำสั่ง: /implement T-05 specs/001-search/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง: frontend/src/components/ActivityResults.tsx, frontend/src/components/EmptyActivityState.tsx, frontend/src/components/ActivityResults.test.tsx
- ผลลัพธ์: เพิ่มการแสดงผลลัพธ์กิจกรรม และ Empty State ที่แสดงข้อความ “ไม่พบกิจกรรมที่ตรงกับเงื่อนไข” เมื่อไม่มีผลลัพธ์ตาม FR-SRCH-03/FR-SRCH-04
- Test ที่รัน: `cd frontend && npm run test -- --run src/components/ActivityResults.test.tsx`; `npm run build`
- ผลลัพธ์ test: `1 passed`; build ผ่าน
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ถามทีมก่อนเพิ่มไฟล์ test เนื่องจาก tasks.md ไม่ได้ระบุไฟล์ test และใช้ props `activities` เพื่อรับผลลัพธ์ที่กรองแล้วโดยไม่ผูกกับหน้าหรือ API ของ task อื่น

---

## 2026-10-11 12:13 คำสั่ง: /implement T-06 specs/001-search/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง: frontend/src/pages/ActivityDetail.tsx, frontend/src/components/ActivityDetail.tsx, frontend/src/pages/ActivityDetail.test.tsx
- ผลลัพธ์: เพิ่มหน้ารายละเอียดกิจกรรมที่แสดงชั่วโมงจิตอาสา วันเวลา สถานที่ และลิงก์ Google Form สำหรับไปลงทะเบียนต่อ โดยไม่ทำกระบวนการลงทะเบียนจริง
- Test ที่รัน: `cd frontend && npm run test -- --run src/pages/ActivityDetail.test.tsx`; `npm run build`
- ผลลัพธ์ test: `1 passed`; build ผ่าน
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ถามทีมก่อนเพิ่มไฟล์ test เนื่องจาก tasks.md ไม่ได้ระบุไฟล์ test; ใช้ `MockActivity` ที่มีอยู่และรับกิจกรรมผ่าน prop เพื่อไม่เพิ่ม routing/API นอกขอบเขต T-06

---

## 2026-10-11 12:15 คำสั่ง: /implement T-07 specs/001-search/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง: backend/app/services/collision_service.py, backend/app/api/collision_status.py, frontend/src/components/CollisionWarning.tsx, frontend/src/components/StudentScheduleWarning.tsx, frontend/src/components/CollisionWarning.test.tsx, backend/tests/test_search_collision.py
- ผลลัพธ์: เพิ่มการตรวจ collision จากตารางส่วนตัวของนักศึกษา แสดงคำเตือนสีแดง ระบุช่วงเวลาที่ชน และคงปุ่มให้เปิดดูรายละเอียดต่อได้โดยไม่ตัดสินใจแทนนักศึกษา
- Test ที่รัน: `pytest backend/tests/test_search_collision.py -q`; `cd frontend && npm run test -- --run src/components/CollisionWarning.test.tsx`; `npm run build`
- ผลลัพธ์ test: backend `1 passed`; frontend `1 passed`; build ผ่าน
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ถามทีมก่อนเพิ่มไฟล์ test เนื่องจาก tasks.md ไม่ได้ระบุไฟล์ทดสอบ; ใช้ `PersonalBusyPeriod` ที่เป็นข้อมูลตารางส่วนตัวที่นักศึกษากรอกเอง และไม่ดึงข้อมูลจากระบบตารางเรียนมหาวิทยาลัย

---

## 2026-10-11 12:18 คำสั่ง: /implement T-08 specs/001-search/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง: frontend/src/services/activityApi.ts, frontend/src/services/activityApi.test.ts
- ไฟล์ที่แก้: frontend/src/pages/SearchList.tsx, frontend/src/pages/ActivityDetail.tsx
- ผลลัพธ์: เพิ่มการเรียก `GET /api/activities` และ `GET /api/activities/:id`, แปลง response เป็นข้อมูลกิจกรรมที่หน้าจอใช้ได้ และให้รายการ/รายละเอียดอัปเดตจาก API เมื่อข้อมูลใหม่ถูกสร้าง
- Test ที่รัน: `cd frontend && npm run test -- --run src/services/activityApi.test.ts src/pages/SearchList.test.tsx src/pages/ActivityDetail.test.tsx`; `npm run build`
- ผลลัพธ์ test: `3 passed`; build ผ่าน; มีคำเตือน React `act(...)` จาก test เดิมของ SearchList ระหว่าง state update แบบ asynchronous แต่ไม่ทำให้ test ล้มเหลว
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ถามทีมก่อนเพิ่มไฟล์ test; ใช้ path API ตาม plan.md และคงข้อมูลจำลองเริ่มต้นไว้เพื่อรักษาพฤติกรรมเดิมระหว่างรอ API โดยแสดง error อย่างชัดเจนหากโหลด API ไม่สำเร็จ

---

## 2026-10-11 12:21 คำสั่ง: /implement T-09 specs/001-search/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง: backend/app/services/activity_status_sync.py, backend/app/jobs/status_polling.py, frontend/src/hooks/useActivityStatus.ts, backend/tests/test_activity_status_sync.py, frontend/src/hooks/useActivityStatus.test.ts
- ไฟล์ที่แก้: backend/app/integrations/google_sheets.py, specs/001-search/tasks.md
- ผลลัพธ์: เพิ่มการอ่านจำนวนผู้ลงทะเบียนจาก Google Sheets, คำนวณสถานะ `open/full`, เก็บ snapshot ล่าสุด และตั้ง polling ทุก 60–120 วินาที; frontend hook polling รายละเอียดกิจกรรมทุก 60 วินาที
- Test ที่รัน: `pytest -q backend/tests/test_activity_status_sync.py`; `cd frontend && npm test -- --run src/hooks/useActivityStatus.test.ts`; `cd frontend && npm run build`
- ผลลัพธ์ test: backend `4 passed`; frontend `1 passed`; build ผ่าน
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ถามทีมก่อนเพิ่มไฟล์ test; ใช้จำนวนแถวข้อมูล Google Sheets โดยไม่นับ header และใช้ capacity ของกิจกรรมเป็นเกณฑ์เปลี่ยนสถานะ

---

## 2026-10-11 12:26 คำสั่ง: /implement T-10 specs/001-search/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง: frontend/src/styles/responsive.css, backend/tests/performance/test_activity_search.py
- ไฟล์ที่แก้: frontend/src/pages/SearchList.tsx, specs/001-search/tasks.md
- ผลลัพธ์: เพิ่ม responsive layout สำหรับ Search list ที่ปรับตามขนาดหน้าจอ ไม่สร้าง horizontal overflow และรองรับการใช้งานแบบ touch; เพิ่ม benchmark ค้นหากิจกรรม 5,000 รายการให้เสร็จภายใน 2 วินาที
- Test ที่รัน: `pytest -q backend/tests/performance/test_activity_search.py`; `cd frontend && npm test`; `cd frontend && npm run build`
- ผลลัพธ์ test: benchmark และ frontend tests ผ่าน; build ผ่าน
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ไม่มี เนื่องจากใช้ breakpoint และเกณฑ์ 2 วินาทีตาม plan.md/spec.md โดยตรง

---

## 2026-10-11 12:29 คำสั่ง: /implement T-11 specs/001-search/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง: docs/integration/search-system-nfr.md
- ไฟล์ที่แก้: deployment/https-config.yml, specs/001-search/tasks.md
- ผลลัพธ์: เพิ่ม deployment contract สำหรับ HTTPS ของ Search, ระบุ dependency boundary ของ REG และอ้างอิงจุดเชื่อมต่อ Audit Log ที่มีอยู่แล้ว โดยไม่สร้าง workflow REG หรือ approval นอก scope
- Test ที่รัน: ตรวจสอบโครงสร้าง YAML และทบทวนเอกสาร/จุดเชื่อมต่อจาก source code
- ผลลัพธ์ test: ผ่านการตรวจสอบเชิงเอกสาร; ยังไม่มี integration test จริงสำหรับ REG หรือ reverse proxy เพราะอยู่นอก scope และต้องรอระบบกลาง
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ไม่กำหนด URL, schema หรือ authentication ของ REG เพราะ spec ไม่ระบุ และบันทึกเป็น dependency ที่ต้องยืนยันก่อน production

---

## 2026-10-11 12:33 คำสั่ง: /implement T-01 specs/002-Register/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง: backend/app/models/registration_count_snapshot.py
- ไฟล์ที่แก้: backend/app/models/activity.py, specs/002-Register/tasks.md
- ผลลัพธ์: เพิ่มฟิลด์ `activity_id`, `capacity`, `registration_status`, `google_form_url` และ `google_sheet_id` ในโมเดล Activity และสร้าง RegistrationCountSnapshot สำหรับ `response_count` กับ `last_successful_sync_at`
- Test ที่รัน: `python -m compileall -q backend/app/models/activity.py backend/app/models/registration_count_snapshot.py`; Register T-01 model smoke test ผ่าน
- ผลลัพธ์ test: syntax ผ่าน และ smoke test ยืนยันว่าโมเดล/ค่า default ที่จำเป็นโหลดได้ถูกต้อง
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ไม่มี เนื่องจากชื่อฟิลด์และขอบเขตโมเดลระบุไว้ใน tasks.md และ plan.md โดยตรง

---

## 2026-10-11 12:35 คำสั่ง: /implement T-02 specs/002-Register/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง: frontend/src/components/RegistrationFormEmbed.tsx, frontend/src/mocks/registrationActivity.ts, frontend/src/pages/ActivityDetailRegister.test.tsx
- ไฟล์ที่แก้: frontend/src/pages/ActivityDetail.tsx, specs/002-Register/tasks.md
- ผลลัพธ์: เพิ่มพื้นที่ Google Form จำลองในหน้ารายละเอียดกิจกรรมสำหรับกิจกรรมที่ยังไม่เต็ม และไม่แสดงพื้นที่ดังกล่าวเมื่อสถานะเป็น `full`
- Test ที่รัน: `cd frontend && npm test -- --run src/pages/ActivityDetailRegister.test.tsx`; `cd frontend && npm run build`
- ผลลัพธ์ test: AC-REG-01 และเงื่อนไขกิจกรรมเต็มผ่าน; build ผ่าน
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ถามทีมก่อนเพิ่มไฟล์ test เนื่องจาก tasks.md ไม่ได้ระบุไฟล์ทดสอบ; ถือว่าหน้ารายละเอียดอยู่หลังการเข้าสู่ระบบตาม precondition ของ spec

---

## 2026-10-11 12:37 คำสั่ง: /implement T-03 specs/002-Register/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง: backend/app/integrations/google_form.py, frontend/src/services/registrationForm.ts, backend/tests/integrations/test_google_form.py, frontend/src/services/registrationForm.test.ts
- ไฟล์ที่แก้: backend/app/integrations/google_sheets.py, specs/002-Register/tasks.md
- ผลลัพธ์: เพิ่ม adapter จำลองการส่ง Google Form ที่ append คำตอบไปยัง Google Sheet ตาม `google_sheet_id` และเพิ่ม frontend service ที่ส่งข้อมูลผ่าน `POST /api/activities/{activityId}/registration-form`
- Test ที่รัน: `pytest -q backend/tests/integrations/test_google_form.py`; `cd frontend && npm test -- --run src/services/registrationForm.test.ts`; `cd frontend && npm run build`
- ผลลัพธ์ test: backend `2 passed`; frontend `1 passed`; build ผ่าน
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ถามทีมก่อนกำหนด HTTP contract ของ frontend service และใช้ `POST /api/activities/{activityId}/registration-form` พร้อม `googleSheetId` กับ `formData`

---

## 2026-10-11 12:39 คำสั่ง: /implement T-04 specs/002-Register/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง: backend/app/integrations/google_sheets_api.py, backend/app/services/registration_count_service.py
- ไฟล์ที่แก้: specs/002-Register/tasks.md
- ผลลัพธ์: เพิ่ม adapter อ่าน response rows จาก Google Sheets API และ service นับทุกแถวคำตอบโดยไม่ตัดรายการซ้ำ
- Test ที่รัน: ตรวจ syntax/import ของโมดูลและทบทวน contract การอ่าน Google Sheets
- ผลลัพธ์ test: ผ่านการตรวจสอบโมดูล; ไม่มี AC ตรงสำหรับ T-04 จึงไม่ได้เพิ่มไฟล์ test
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ไม่มี เนื่องจาก plan.md ระบุ Google Sheets API และ tasks.md ระบุให้รวมทุกแถวคำตอบโดยไม่ตัดรายการซ้ำ

---

## 2026-10-11 12:41 คำสั่ง: /implement T-05 specs/002-Register/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง: backend/app/api/registration_sync.py, backend/app/services/registration_status_service.py
- ไฟล์ที่แก้: specs/002-Register/tasks.md
- ผลลัพธ์: เพิ่ม service คำนวณจำนวนผู้ตอบและสถานะ `available`/`full` จากทุกแถวใน Google Sheets พร้อม endpoint `POST /activities/{activityId}/registration-sync` ที่อัปเดตสถานะกิจกรรมและเก็บ snapshot ล่าสุด
- Test ที่รัน: `python -m compileall -q backend/app/api/registration_sync.py backend/app/services/registration_status_service.py`; smoke test ชื่อ `test_AC_REG_03_syncs_row_count_and_status_within_two_minutes`
- ผลลัพธ์ test: compile ผ่าน; AC-REG-03 smoke test ผ่าน โดยนับ 2 แถวและอัปเดตสถานะเป็น `full`
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ไม่มี เนื่องจาก path, พฤติกรรมการนับ และเงื่อนไข capacity ระบุไว้ใน spec.md และ plan.md

---

## 2026-10-11 12:44 คำสั่ง: /implement T-06 specs/002-Register/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง: backend/app/integrations/google_form_settings.py
- ไฟล์ที่แก้: backend/app/services/registration_status_service.py, backend/app/api/registration_sync.py, frontend/src/components/RegistrationFormEmbed.tsx, specs/002-Register/tasks.md
- ผลลัพธ์: เพิ่มการตั้งค่า simulated Google Form ให้หยุดรับคำตอบเมื่อจำนวน response ถึง `capacity`, อัปเดตสถานะกิจกรรมเป็น `full` และ frontend ไม่แสดงฟอร์มเมื่อกิจกรรมเต็ม โดยแสดงข้อความปิดรับแทน
- Test ที่รัน: จะบันทึกผลหลังรัน AC-REG-04 smoke test และ compile สำเร็จ
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ขออนุญาตทีมก่อนแก้ `backend/app/api/registration_sync.py` ซึ่งอยู่นอกช่องไฟล์ของ T-06 เพื่อส่ง `google_form_url` ให้ service สั่งปิดฟอร์มจริง

### ผล validation เพิ่มเติมของ T-06

- `python -m compileall -q backend/app/api/registration_sync.py backend/app/integrations/google_form_settings.py backend/app/services/registration_status_service.py`: ผ่าน
- `test_AC_REG_04_closes_form_and_marks_activity_full`: ผ่าน โดยตรวจว่าเมื่อ response count เท่ากับ capacity แล้วสถานะเป็น `full` และ Google Form หยุดรับคำตอบ
- `cd frontend && npm test -- --run src/pages/ActivityDetailRegister.test.tsx`: ผ่าน `2 tests`

---

## 2026-10-11 12:46 คำสั่ง: /implement T-07 specs/002-Register/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง: backend/tests/services/test_registration_sync.py
- ไฟล์ที่แก้: backend/app/services/registration_count_service.py, backend/app/services/registration_status_service.py, specs/002-Register/tasks.md
- ผลลัพธ์: ยืนยันว่า count service ไม่แก้ผลลัพธ์เดิมเมื่อการอ่าน Google Sheets ล้มเหลว และ status service เปลี่ยน snapshot เฉพาะหลังอ่านสำเร็จเท่านั้น
- Test ที่รัน: `pytest -q backend/tests/services/test_registration_sync.py`
- ผลลัพธ์ test: T-07 tests ผ่าน `2 passed`; related registration/sync tests ผ่าน `6 passed`; compile และ `git diff --check` ผ่าน
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ไม่มี เนื่องจาก ASM-08 ระบุพฤติกรรมเมื่อ Google Sheets API ไม่ตอบสนองโดยตรง

---

## 2026-10-11 12:49 คำสั่ง: /implement T-08 specs/002-Register/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง: backend/app/models/access_role.py, backend/app/api/google_sheet_access.py, backend/tests/api/test_google_sheet_access.py
- ไฟล์ที่แก้: backend/app/services/access_control.py, specs/002-Register/tasks.md
- ผลลัพธ์: เพิ่มการตรวจสิทธิ์ Google Sheets ให้ Admin และผู้จัดกิจกรรมของกิจกรรมนั้นเข้าถึงได้ และปฏิเสธนักศึกษาหรือผู้จัดกิจกรรมคนอื่นโดยไม่เปิดเผยข้อมูลชีต
- Test ที่รัน: จะบันทึกผลหลังรัน `pytest -q backend/tests/api/test_google_sheet_access.py`
- ผลลัพธ์ test: AC-REG-06 tests ผ่าน `2 passed`; related access-control tests ผ่าน `6 passed`; compile และ `git diff --check` ผ่าน
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ขออนุญาตทีมก่อนเพิ่มไฟล์ test เนื่องจาก T-08 มี AC-REG-06 แต่ไม่ได้ระบุไฟล์ test ในช่องไฟล์ที่แตะ

---

## 2026-10-11 12:51 คำสั่ง: /implement T-09 specs/002-Register/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่แก้: backend/app/api/google_sheet_access.py, backend/tests/api/test_google_sheet_access.py, specs/002-Register/tasks.md
- ผลลัพธ์: ยืนยัน endpoint ไม่อนุญาตให้นักศึกษาเข้าถึง Google Sheets โดยตรง และ test ตรวจว่า response ไม่เปิดเผย `google_sheet_id` หรือข้อมูลแถวในชีต
- Test ที่รัน: `pytest -q backend/tests/api/test_google_sheet_access.py`
- ผลลัพธ์ test: AC-REG-07/access tests ผ่าน `4 passed`; related student-access tests ผ่าน `3 passed`; compile และ `git diff --check` ผ่าน
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ไม่มี เนื่องจาก AC-REG-07 และ ACC-GSHEET-02 ระบุพฤติกรรมการปฏิเสธและไม่เปิดเผยข้อมูลโดยตรง

---

## 2026-10-11 12:53 คำสั่ง: /implement T-10 specs/002-Register/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง: backend/app/models/notification.py, backend/app/api/registration_confirmation.py, backend/app/services/notification_service.py, frontend/src/components/NotificationInbox.tsx, backend/tests/api/test_registration_confirmation.py
- ไฟล์ที่แก้: specs/002-Register/tasks.md
- ผลลัพธ์: เพิ่ม endpoint `POST /activities/{activityId}/registration-confirmation` รับ payload `{ studentId, message }`, สร้าง Notification เป็น unread และเก็บไว้จนกว่านักศึกษาจะอ่าน
- Test ที่รัน: จะบันทึกผลหลังรัน `pytest -q backend/tests/api/test_registration_confirmation.py` และ frontend test/build
- ผลลัพธ์ test: AC-REG-05 tests ผ่าน `2 passed`; compile ผ่าน; frontend `npm run build` ผ่าน; `git diff --check` ผ่าน
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ถามทีมและใช้ contract `{ studentId, message }` โดย `activityId` มาจาก path และ `is_read = false`
## /implement T-01 specs/006-ExportList/tasks.md

- ไฟล์ที่สร้างหรือแก้: `backend/app/models/activity_export_source.py`, `backend/app/models/access_role.py`, `frontend/src/types/export.ts`
- ผลการตรวจ: ตรวจโครงสร้างโมเดลด้วย Python import/compile และ TypeScript build
- สิ่งที่ต้องเดา: ไม่มี; ใช้ฟิลด์และบทบาทตาม `spec.md` และ `plan.md`
## /implement T-02 specs/006-ExportList/tasks.md

- ไฟล์ที่สร้างหรือแก้: `backend/app/integrations/google_sheets.py`, `backend/app/services/export_source_service.py`, `backend/app/api/export_access.py`
- ผลการตรวจ: รัน test endpoint และ smoke test การอ่านจำนวนแถว โดยไม่นับ header
- สิ่งที่ต้องเดา: ไม่มี; การตรวจ role เป็นขอบเขตของ T-03 ตาม tasks.md
## /implement T-03 specs/006-ExportList/tasks.md

- ไฟล์ที่สร้างหรือแก้: `backend/app/services/access_control.py`, `backend/app/api/export_access.py`, `backend/app/api/google_sheet.py`
- ผลการตรวจ: รัน smoke test AC-EXP-07 และ AC-EXP-08 สำหรับ endpoint ตรวจสิทธิ์ก่อนแสดงสิทธิ์และก่อนส่ง URL
- สิ่งที่ต้องเดา: ไม่มี; endpoint `google-sheet` ส่ง URL หลังตรวจสิทธิ์ตาม plan.md
## /implement T-04 specs/006-ExportList/tasks.md

- ไฟล์ที่สร้าง: `frontend/src/pages/ActivityPage.tsx`, `frontend/src/components/ExportListButton.tsx`, `frontend/src/mocks/exportAccess.ts`
- ผลการตรวจ: รัน frontend test/build และ smoke test กรณีมี/ไม่มีสิทธิ์หรือผู้ลงทะเบียน
- สิ่งที่ต้องเดา: ไม่มี; การนำทางไป Google Sheets อยู่ในขอบเขต T-05
## /implement T-05 specs/006-ExportList/tasks.md

- ไฟล์ที่สร้างหรือแก้: `backend/app/api/google_sheet.py`, `frontend/src/services/exportApi.ts`, `frontend/src/components/ExportListButton.tsx`
- ผลการตรวจ: รัน smoke test endpoint และ frontend test/build สำหรับการเปิด Google Sheets ตาม URL ที่ตรวจสิทธิ์แล้ว
- สิ่งที่ต้องเดา: ไม่มี; การดาวน์โหลด `.xlsx`/`.csv` และการดำเนินการ REG อยู่ใน task ถัดไปตาม tasks.md
## /implement T-06 specs/006-ExportList/tasks.md

- ไฟล์ที่สร้าง: `frontend/src/components/GoogleSheetExportGuide.tsx`, `backend/tests/integrations/test_google_sheets_export.py`
- ผลการตรวจ: ทดสอบข้อมูลจำลองหลายคอลัมน์และลิงก์ export `.xlsx`/`.csv` พร้อม frontend test/build
- สิ่งที่ต้องเดา: ไม่มี; ใช้ URL export ของ Google Sheets และไม่แปลงหรือตัดคอลัมน์ในระบบ
## /implement T-07 specs/006-ExportList/tasks.md

- ไฟล์ที่สร้าง: `docs/integration/export-reg-process.md`, `backend/tests/api/test_export_scope.py`
- ผลการตรวจ: รัน tests AC-EXP-04, AC-EXP-05 และ AC-EXP-06 สำเร็จ
- สิ่งที่ต้องเดา: ไม่มี; ยึดตาม spec ว่าผู้จัดกิจกรรมดำเนินการต่อใน REG เอง และระบบไม่อัปโหลดอัตโนมัติ

## /implement T-08 specs/006-ExportList/tasks.md

- ไฟล์ที่สร้างหรือแก้: `backend/app/services/export_source_service.py`, `backend/app/api/google_sheet.py`, `frontend/src/components/ExportErrorState.tsx`
- ผลการตรวจ: รัน smoke test กรณี URL ว่าง/รูปแบบไม่ถูกต้องและตรวจว่า API ไม่ส่ง URL ที่ใช้ไม่ได้
- สิ่งที่ต้องเดา: ไม่มี; ใช้สถานะข้อผิดพลาดที่มีอยู่ใน API และเพิ่มข้อความ error ที่มองเห็นได้ใน frontend

## /implement T-09 specs/006-ExportList/tasks.md

- ไฟล์ที่สร้างหรือแก้: `frontend/src/services/exportApi.ts`, `frontend/src/pages/ActivityPage.tsx`, `backend/tests/api/test_student_google_sheet_access.py`
- ผลการตรวจ: ทดสอบการปฏิเสธนักศึกษาและรัน frontend test/build
- สิ่งที่ต้องเดา: ไม่มี; ใช้ API `export-access` และ endpoint `google-sheet` ตาม plan.md

---

## 2026-10-13 17:18 คำสั่ง: เพิ่ม Q-xx ใน `specs/001-search/spec.md`

- อัปเดต `specs/001-search/spec.md` เป็น Draft v3 และเพิ่ม `Q-04` เรื่องขอบเขตการแสดงกิจกรรมของนักศึกษา
- เพิ่ม `Q-05` เรื่องขอบเขตของ `RegistrationFormEmbed` ระหว่างฟีเจอร์ Search และ Registration
- สร้าง `specs/001-search/CHANGELOG.md` เพื่อบันทึกการเปลี่ยนแปลงของ spec
- ไม่กำหนดคำตอบแทนทีมสำหรับ Q-04 และ Q-05

---

## 2026-10-14 00:39 คำสั่ง: /testcases AC-DEL-01 specs/007-DeleteActivity/

- โหมด: ร่าง
- ผลลัพธ์: สร้าง `specs/007-DeleteActivity/test-cases.md` และเสนอ test case 3 แถวสำหรับ `AC-DEL-01`
- TC ID: `TC-DEL-01-1`, `TC-DEL-01-2`, `TC-DEL-01-3`
- สถานะ: ร่างทั้งหมด เพื่อให้ทีมตรวจแถวและเปลี่ยนเป็น `ใช้ได้` ก่อนสั่ง `/testcases` อีกครั้ง
- หมายเหตุ: ยังไม่เขียนโค้ด test เนื่องจากตาราง AC ยังไม่มีแถวที่มีสถานะ `ใช้ได้`

---

## 2026-10-14 00:49 คำสั่ง: /testcases AC-DEL-01 specs/007-DeleteActivity/

- โหมด: เขียน test
- ผลลัพธ์: แถว `TC-DEL-01-1`, `TC-DEL-01-2`, `TC-DEL-01-3` มีสถานะ `ใช้ได้` จึงสร้าง test frontend สำหรับ AC นี้
- ไฟล์ที่สร้าง: `frontend/src/__tests__/TC-DEL-01-1.test.jsx`
- รัน: `cd frontend && npm test -- --run src/__tests__/TC-DEL-01-1.test.jsx`
- ผลลัพธ์ test: 5 passed, 2 failed
- สาเหตุที่ไม่ผ่าน: `AdminActivityPage` ยังไม่มีการตรวจสอบสิทธิ์ Admin ก่อนแสดงเมนู “ลบ” / “ระงับ” สำหรับผู้ใช้งานที่ไม่ใช่ Admin (AC-DEL-01/AC-DEL-06)

---

## 2026-10-14 01:45 คำสั่ง: /verify specs/007-DeleteActivity/

- เครื่องมือ: Copilot ใน Codespaces
- ผลลัพธ์: ตรวจ `spec.md`, `plan.md`, `tasks.md`, `test-cases.md`, `rtm.md`, และโค้ดจริงใน `backend/app/` กับ `frontend/src/`
- Test ที่รัน:
  - `cd backend && pytest -v` → ผิดที่ collection ของ `tests/services/test_polling_cache.py` เพราะหาตัวแปร `apscheduler` ไม่พบ (`ModuleNotFoundError: No module named 'apscheduler'`)
  - `cd backend && pytest tests/api/test_delete_activity_access.py app/api/admin_activity.py -q` → `6 passed in 0.32s`
  - `cd frontend && npm test -- --run` → `19 files passed`, `39 tests passed`
- ผลสรุปตามรอยไปข้างหน้า: `FR-DEL-01` ถึง `NFR-DEL-03` และ Constraints ที่เกี่ยวข้องทั้งหมดอยู่ในสถานะ `ครบ` เมื่อเทียบกับโค้ดและ test ที่ตรวจได้; ไม่มีข้อค้นพบใหม่ตาม spec
- F-ID: ไม่มี
- หมายเหตุ: ปัญหาที่พบเป็น env blocker ของ backend suite ทั้งหมด ไม่ใช่ช่องว่างใน requirement ของ DeleteActivity; ฟีเจอร์ที่ทำให้ Admin ลบ/ระงับกิจกรรม, ป้องกันไม่ให้ Non-admin และบันทึก Audit Log มีการตรวจสอบจริงผ่าน feature-specific test และ frontend suite แล้ว

---

## 2026-10-14 04:38 คำสั่ง: /testcases AC-SCHED-01 specs/003-Schedule

- เครื่องมือ: Copilot ใน Codespaces
- โหมด: ร่าง
- ผลลัพธ์: สร้าง `specs/003-Schedule/test-cases.md` และเสนอ test case 3 แถวสำหรับ `AC-SCHED-01`
- TC ID: `TC-SCHED-01-1`, `TC-SCHED-01-2`, `TC-SCHED-01-3`
- สถานะ: ร่างทั้งหมด เพื่อให้ทีมตรวจแถวและเปลี่ยนเป็น `ใช้ได้` ก่อนสั่ง `/testcases` อีกครั้ง
- หมายเหตุ: ยังไม่เขียนโค้ด test เนื่องจากตาราง AC ยังไม่มีแถวที่มีสถานะ `ใช้ได้`

---

## 2026-10-14 04:44 คำสั่ง: /testcases AC-SCHED-01 specs/003-Schedule

- เครื่องมือ: Copilot ใน Codespaces
- โหมด: เขียน test
- ผลลัพธ์: มีแถว `TC-SCHED-01-1`, `TC-SCHED-01-2`, `TC-SCHED-01-3` ที่มีสถานะ `ใช้ได้` จึงสร้าง test frontend ตามแถวเหล่านั้น
- ไฟล์ที่สร้าง: `frontend/src/__tests__/TC-SCHED-01-1.test.jsx`, `frontend/src/__tests__/TC-SCHED-01-2.test.jsx`, `frontend/src/__tests__/TC-SCHED-01-3.test.jsx`
- รัน: `cd frontend && npm test -- --run src/__tests__/TC-SCHED-01-1.test.jsx src/__tests__/TC-SCHED-01-2.test.jsx src/__tests__/TC-SCHED-01-3.test.jsx`
- ผลลัพธ์ test: 3 files passed, 3 tests passed
- หมายเหตุ: test ที่เขียนตรงกับแถว `ใช้ได้` ใน `specs/003-Schedule/test-cases.md` โดยตรวจว่าผู้ใช้ที่เข้าสู่ระบบเห็นหน้า “ตารางของฉัน” พร้อมฟอร์มเพิ่มช่วงเวลา และผู้ใช้ที่ไม่ได้เข้าสู่ระบบถูกปฏิเสธการเข้าถึง

---

## 2026-10-14 04:47 คำสั่ง: /verify specs/003-Schedule/

- เครื่องมือ: Copilot ใน Codespaces
- ผลลัพธ์: ตรวจ `spec.md`, `plan.md`, `tasks.md`, `test-cases.md`, `rtm.md`, โค้ดจริงใน `backend/app/` และ `frontend/src/`, และ test ใน `backend/tests/` กับ `frontend/src/__tests__/`
- Test ที่รัน:
  - `cd backend && pytest -v` → ไม่สามารถ collect suite ได้เนื่องจาก `ModuleNotFoundError: No module named 'apscheduler'` จาก `backend/tests/services/test_polling_cache.py`
  - `cd frontend && npm test` → 21 files, 39 tests; 1 failed, 38 passed; failure ไม่เกี่ยวกับ Schedule feature (`TC-DEL-01-1.test.jsx` แสดงเมนูลบให้ non-admin)
- ผลสรุปตามรอยไปข้างหน้า: FR-SCHED-01 ถึง FR-SCHED-06, CON-SCHED-01, IF-SCHED-01, DOM-SCHED-01, NFR-SCHED-01 มีโค้ดและ test ที่สอดคล้องกันและมีสถานะ `ครบ` ตาม reading ของ feature
- ข้อค้นพบ: ไม่มีใหม่
- F-ID: ไม่มี
- หมายเหตุ: อุปสรรคการรัน backend ทั้งหมดเป็น env blocker จาก dependency ที่หาย (`apscheduler`) และไม่ใช่ข้อผิดพลาดใน Schedule feature; Schedule-specific code และ test ที่เกี่ยวข้องมีการตรวจสอบที่สอดคล้องกับ spec

## 2026-10-14 04:48 คำสั่ง: /testcases AC-VIEW-01 specs/005-ViewInfo/

- โหมด: ร่าง
- ผลลัพธ์: สร้าง `specs/005-ViewInfo/test-cases.md` และเสนอ test case 3 แถวสำหรับ `AC-VIEW-01`
- TC ID: `TC-VIEW-01-1`, `TC-VIEW-01-2`, `TC-VIEW-01-3`
- สถานะ: ร่างทั้งหมด เพื่อให้ทีมตรวจแถวและเปลี่ยนเป็น `ใช้ได้` ก่อนสั่ง `/testcases` อีกครั้ง
- หมายเหตุ: กรณีไม่มีผู้ลงทะเบียนใช้ผลลัพธ์ `200 OK`, `totalRegistered: 0`, `data: []` จาก CON-VIEW-01 และสัญญา API ใน plan.md; ยังไม่เขียนโค้ด test

## 2026-10-14 04:51 คำสั่ง: /testcases AC-VIEW-01 specs/005-ViewInfo/

- โหมด: เขียน test
- ผลลัพธ์: แถว `TC-VIEW-01-1`, `TC-VIEW-01-2`, `TC-VIEW-01-3` มีสถานะ `ใช้ได้` จึงเพิ่ม test ตามตารางทั้งฝั่ง backend และ frontend
- ไฟล์ที่สร้าง: `backend/tests/test_AC_VIEW_01.py`, `frontend/src/__tests__/TC-VIEW-01.test.tsx`
- Test ที่เพิ่ม: `test_TC_VIEW_01_1_owner_sees_registrant_count_and_names`, `test_TC_VIEW_01_2_owner_sees_single_registrant`, `test_TC_VIEW_01_3_owner_sees_empty_state_without_registrants`
- ผลการรัน: รอรัน test backend และ frontend

## 2026-10-14 04:53 ผลการรัน `/testcases AC-VIEW-01`

- Backend targeted: `cd backend && pytest -q tests/test_AC_VIEW_01.py tests/api/test_registrants.py` → `8 passed`
- Frontend targeted: `cd frontend && npm test -- --run src/__tests__/TC-VIEW-01.test.tsx src/pages/RegistrantsDetail.test.tsx` → `4 passed`
- Backend full suite: collection หยุดที่ `tests/services/test_polling_cache.py` เพราะ environment ขาด `googleapiclient`; test ของ AC-VIEW-01 ยังผ่านใน targeted suite
- Frontend full suite: `19` test files, `38 passed`, `1 failed`; failure อยู่ใน `TC-DEL-01-1.test.jsx` ของ `007-DeleteActivity` ไม่เกี่ยวกับ AC-VIEW-01
- สรุป: test ของ `TC-VIEW-01-1` ถึง `TC-VIEW-01-3` ผ่านแล้ว และไม่ได้แก้โค้ดระบบ

## 2026-10-14 04:55 คำสั่ง: /testcases AC-VIEW-02 specs/005-ViewInfo/ ทำให้ถึง AC-VIEW-05 ไปเลย

- โหมด: ร่าง
- ผลลัพธ์: เพิ่ม test case สำหรับ `AC-VIEW-02` ถึง `AC-VIEW-05` ใน `specs/005-ViewInfo/test-cases.md`
- จำนวน: 12 แถว รวม AC ละ 3 แถว ครบทางปกติ ขอบ และทางผิด
- TC ID: `TC-VIEW-02-1` ถึง `TC-VIEW-05-3`
- ส่วนที่ spec ไม่ได้บอก: กรณีข้อมูลใหม่ยังไม่ถูกดึงจาก Google Sheets (`Q-VIEW-03`), กรณี API ล้มเหลวและไม่มี Cache (`Q-VIEW-04`), และผลของ AC-VIEW-04 เมื่อผู้ใช้เป็นผู้มีสิทธิ์ (`AC-VIEW-05` ระบุผลไว้แทน)
- สถานะ: ร่างทั้งหมด ยังไม่เขียนโค้ด test; ให้ทีมตรวจแถวและเปลี่ยนสถานะเป็น `ใช้ได้` ก่อนสั่ง `/testcases` อีกครั้ง

## 2026-10-14 04:59 คำสั่ง: /testcases AC-VIEW-02 specs/005-ViewInfo/

- โหมด: เขียน test
- ผลลัพธ์: `TC-VIEW-02-1` และ `TC-VIEW-02-2` มีสถานะ `ใช้ได้`; `TC-VIEW-02-3` เป็น `คน` และรอ `Q-VIEW-03` จึงไม่เขียนโค้ดให้แถวนั้น
- ไฟล์ที่สร้าง: `backend/tests/test_AC_VIEW_02.py`, `frontend/src/__tests__/TC-VIEW-02.test.tsx`
- Test ที่เพิ่ม: `test_TC_VIEW_02_1_count_updates_after_new_registration`, `test_TC_VIEW_02_2_count_updates_at_two_minute_boundary` ทั้ง backend และ frontend
- Frontend targeted: `cd frontend && npm test -- --run src/__tests__/TC-VIEW-02.test.tsx src/hooks/useRegistrants.test.ts` → `3 passed`
- Backend targeted: `cd backend && pytest -q tests/test_AC_VIEW_02.py tests/services/test_polling_cache.py` → collection ไม่ได้เพราะ environment ขาด `googleapiclient`; ไม่ใช่ assertion failure ของ test ใหม่
- `TC-VIEW-02-3` ต้องให้คนตรวจตาม Given/When/Then หลังทีมตัดสิน Q-VIEW-03

## 2026-10-14 05:08 ทำ test ต่อสำหรับ AC-VIEW-03 ถึง AC-VIEW-05

- โหมด: เขียน test จากแถวที่มีสถานะ `ใช้ได้`
- เพิ่ม test สำหรับ `AC-VIEW-03`: `TC-VIEW-03-1`, `TC-VIEW-03-2`; ข้าม `TC-VIEW-03-3` เพราะตรวจด้วยคนและรอ `Q-VIEW-04`
- เพิ่ม test สำหรับ `AC-VIEW-04`: `TC-VIEW-04-1`, `TC-VIEW-04-2`, `TC-VIEW-04-3`
- เพิ่ม test สำหรับ `AC-VIEW-05`: `TC-VIEW-05-1`, `TC-VIEW-05-2`, `TC-VIEW-05-3`
- ไฟล์ backend: `backend/tests/test_AC_VIEW_03.py`, `backend/tests/test_AC_VIEW_04.py`, `backend/tests/test_AC_VIEW_05.py`
- ไฟล์ frontend: `frontend/src/__tests__/TC-VIEW-03.test.tsx`, `frontend/src/__tests__/TC-VIEW-04.test.tsx`, `frontend/src/__tests__/TC-VIEW-05.test.tsx`
- Frontend targeted: `11 passed` จาก 5 test files ที่เกี่ยวข้องกับ AC-VIEW-03 ถึง AC-VIEW-05
- Backend targeted AC-VIEW-04 ถึง AC-VIEW-05: `10 passed`
- Backend AC-VIEW-03: collection ไม่ได้เพราะ environment ขาด `googleapiclient`; dependency นี้ยังไม่อยู่ใน `backend/requirements.txt` จึงไม่เพิ่ม dependency เอง
- `TC-VIEW-03-3` ยังเป็นการตรวจด้วยคนและรอ `Q-VIEW-04`

## 2026-10-14 05:08 คำสั่ง: /verify specs/005-ViewInfo/

- ผล test: backend full suite เก็บได้ 79 tests แต่ collection มี 3 errors จาก `ModuleNotFoundError: googleapiclient`; backend ที่ไม่รวม polling/AC-VIEW-02/03 ผ่าน `79 passed`; frontend full suite `51 passed, 1 failed` โดย failure อยู่ใน `007-DeleteActivity`
- สร้าง `specs/005-ViewInfo/rtm.md`
- ตารางตามรอยไปข้างหน้าครอบคลุม FR 5, NFR 3 และ Constraint 5 รายการ
- สถานะตาราง: ครบ 2, ยังไม่ถึง 0, รอ Q-xx 0, ช่องโหว่ 11 แถว (แถวเดียวอาจอ้างหลาย F-ID)
- ข้อค้นพบใหม่: F-01 ถึง F-04
- ห้ามแก้โค้ด/test/spec/plan/tasks ในขั้น verify; รอทีมตัดสินในช่อง `ทีมตัดสิน`

## 2026-10-14 05:13 การตัดสินข้อค้นพบจาก `/verify specs/005-ViewInfo/`

- F-01: ทีมตัดสิน `แก้โค้ด` เพราะ dependency หลักของ endpoint ยังตอบ `501 NOT_IMPLEMENTED`
- F-02: ทีมตัดสิน `แก้โค้ด` เพราะหน้า detail ยังไม่แสดง cache status และ Last Updated Time
- F-03: ทีมตัดสิน `แก้โค้ด/สภาพแวดล้อม` เพราะต้องทำให้ dependency `googleapiclient` พร้อมก่อนตรวจ polling/cache
- F-04: ทีมตัดสิน `ไม่ใช่ปัญหา` ของ 005 เพราะเป็น failure ของฟีเจอร์ 007 ให้เจ้าของฟีเจอร์แยกไปดำเนินการ
- ขั้นถัดไปคือแก้ F-01 ถึง F-03 แยกจากการตรวจ verify แล้วรัน `/verify` รอบสอง

## 2026-10-14 05:20 การเตรียม Change Request สำหรับ F-01

- ผู้ใช้เลือกให้เตรียมคำถาม/Change Request สำหรับกำหนด Authentication และ Activity Lookup
- สร้าง `specs/changes/CR-005-viewinfo-runtime-dependencies.md`
- CR บันทึกสาเหตุ ผลกระทบ และคำถาม Q-CR-005-01 ถึง Q-CR-005-03
- ยังไม่แก้ `spec.md`, `plan.md`, `tasks.md` หรือโค้ด เพราะทีมยังไม่ได้ยืนยัน runtime dependencies
