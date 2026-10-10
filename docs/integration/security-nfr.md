# ViewInfo Security NFR

เอกสารนี้ยืนยันการรองรับ `NFR-SEC-01`, `NFR-SEC-02`, `ACC-VIEW-01` และ
`ACC-VIEW-02` ของ ViewInfo

## HTTPS

นโยบาย deployment อยู่ที่ [`deployment/https-config.yml`](../../deployment/https-config.yml)
และกำหนดให้:

- เปิดใช้งาน HTTPS
- redirect HTTP ไป HTTPS
- ใช้ TLS อย่างน้อย `TLSv1.2`
- เปิด HSTS สำหรับการเชื่อมต่อครั้งถัดไป
- ไม่ส่งข้อมูลส่วนบุคคลของผู้ลงทะเบียนผ่านช่องทาง HTTP

ไฟล์นี้เป็น deployment contract แบบไม่ผูกกับผู้ให้บริการ การตั้งค่า reverse proxy
หรือ ingress จริงต้องทำให้ตรงกับ contract นี้ก่อนเปิดใช้งานระบบ

## Authorization ทุก request

Endpoint `GET /api/v1/activities/{activity_id}/registrants` เรียก
`verify_event_owner_or_admin` ก่อนอ่าน cache และสร้าง response ทุกครั้ง

- Admin อ่านข้อมูลได้
- ผู้จัดกิจกรรมอ่านได้เฉพาะกิจกรรมที่ `owner_id` ตรงกับ `user_id`
- ผู้ใช้ทั่วไปและผู้จัดกิจกรรมของกิจกรรมอื่นได้รับ `403 Forbidden`
- เมื่อถูกปฏิเสธ ระบบจะไม่สร้าง response ที่มีข้อมูลส่วนบุคคลของผู้ลงทะเบียน

การตรวจสอบนี้อยู่ใน dependency ของ endpoint ไม่ใช่เฉพาะใน UI จึงยังมีผลเมื่อเรียก
API โดยตรง

## หลักฐานการตรวจสอบ

การทดสอบใน
[`backend/tests/security/test_registrant_security.py`](../../backend/tests/security/test_registrant_security.py)
ตรวจทั้ง deployment contract และการปฏิเสธการเข้าถึงข้อมูลของนักศึกษาทั่วไป
