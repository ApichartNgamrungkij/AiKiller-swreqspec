# CR-005: กำหนด Runtime Dependencies ของ ViewInfo

สถานะ: รอทีมยืนยัน  
วันที่: 2026-10-14  
อ้างอิงฟีเจอร์: `005-ViewInfo`  
อ้างอิงข้อค้นพบ: `F-01` ใน `specs/005-ViewInfo/rtm.md`

## เหตุผล

การตรวจ `/verify specs/005-ViewInfo/` พบว่า endpoint
`GET /api/v1/activities/{activity_id}/registrants` ยังมี dependency จำลอง
สองจุดใน `backend/app/api/registrants.py`:

- `get_current_user()` ตอบ `501 NOT_IMPLEMENTED`
- `get_activity(activity_id)` ตอบ `501 NOT_IMPLEMENTED`

ดังนั้น test ที่ override dependency ผ่าน ยังไม่ยืนยันว่า endpoint จริงอ่านผู้ใช้
และค้นหากิจกรรมเพื่อบังคับใช้ `ACC-VIEW-01`, `ACC-VIEW-02` และ `NFR-SEC-02`
ได้ครบถ้วน

## ขอบเขตผลกระทบ

- `FR-VIEW-01`, `FR-VIEW-05`
- `ACC-VIEW-01`, `ACC-VIEW-02`
- `NFR-SEC-02`
- `AC-VIEW-01`, `AC-VIEW-03`, `AC-VIEW-04`, `AC-VIEW-05`
- `backend/app/api/registrants.py`
- test endpoint และ test authorization ของ `005-ViewInfo`

## คำถามที่ต้องยืนยัน

### Q-CR-005-01: Authentication

`get_current_user()` ต้องอ่านตัวตนผู้ใช้จากวิธีใด?

- [ ] ใช้ dependency authentication ที่มีอยู่แล้วใน repo (โปรดระบุไฟล์/ฟังก์ชัน)
- [ ] ใช้ข้อมูลจาก `Authorization: Bearer <token>` (ทีมต้องระบุวิธีตรวจ token หรือ service ที่รับผิดชอบ)
- [ ] ใช้แนวทางอื่น (ทีมระบุ)

ข้อมูลขั้นต่ำที่ dependency ต้องคืนเพื่อให้ตรงกับ spec:

- `user_id` สำหรับเทียบกับ `Activity.owner_id`
- `role` หรือข้อมูลเทียบเท่าสำหรับแยก `Admin`, ผู้จัดกิจกรรม และนักศึกษา

### Q-CR-005-02: Activity lookup

`get_activity(activity_id)` ต้องค้นหา `Activity` จากแหล่งข้อมูลใด?

- [ ] ใช้ repository/service ที่มีอยู่แล้วใน repo (โปรดระบุไฟล์/ฟังก์ชัน)
- [ ] ใช้ฐานข้อมูลจริง (ทีมต้องระบุ session/repository dependency)
- [ ] ใช้แหล่งข้อมูลอื่น (ทีมระบุ)

กรณีไม่พบกิจกรรมต้องตอบกลับอย่างไร?

- [ ] `404 Not Found`
- [ ] ใช้ผลลัพธ์/รหัสอื่น (ทีมระบุ)

### Q-CR-005-03: สิทธิ์และสถานะผู้ใช้

ผู้จัดกิจกรรมต้องมีค่า `role` ใดจึงถือว่าเป็นผู้จัดที่ได้รับอนุญาต?

- [ ] `organizer`
- [ ] ใช้การเป็นเจ้าของจาก `user_id == owner_id` โดยไม่ตรวจ role เพิ่ม
- [ ] ค่าอื่น (ทีมระบุ)

Admin ต้องระบุด้วย field/role ใด และมีสิทธิ์ดูทุกกิจกรรมหรือไม่?

- [ ] `role=admin` และดูได้ทุกกิจกรรม
- [ ] ค่าอื่น (ทีมระบุ)

## เงื่อนไขก่อน implement

ทีมต้องยืนยัน Q-CR-005-01 ถึง Q-CR-005-03 ก่อนจึงจะ:

1. แก้ `spec.md` หรือเพิ่มส่วนข้อตกลงเพิ่มเติมที่ได้รับการยืนยัน
2. ปรับ `plan.md` และ `tasks.md` ให้ระบุ dependency ที่เลือก
3. ทำ task implementation ของ authentication/activity lookup
4. รัน `/verify specs/005-ViewInfo/` รอบสอง

ห้ามเลือกคำตอบแทนทีมจากตัวเลือกในเอกสารนี้
