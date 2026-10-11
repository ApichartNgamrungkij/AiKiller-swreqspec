# Search: การตรวจสอบ NFR ระบบกลางและ HTTPS

เอกสารนี้เป็น integration contract ของฟีเจอร์ Search ตาม NFR ใน
[`specs/001-search/spec.md`](../../specs/001-search/spec.md) โดยยืนยันเฉพาะ
จุดเชื่อมต่อที่มีอยู่แล้วหรือเป็น dependency ของระบบกลาง ไม่สร้าง workflow
การลงทะเบียนหรือ workflow REG ใหม่ในฟีเจอร์ Search

## HTTPS

นโยบาย deployment อยู่ที่
[`deployment/https-config.yml`](../../deployment/https-config.yml) และกำหนดว่า:

- ทุก request ต้องผ่าน TLS อย่างน้อย `TLSv1.2`
- HTTP ต้อง redirect ไป HTTPS ด้วยสถานะ `308`
- เปิด HSTS พร้อม `includeSubDomains` และ `preload`
- endpoint ของ Search ที่มี prefix `/api/activities` ต้องใช้ HTTPS
- reverse proxy หรือ ingress ที่นำไป deploy ต้องบังคับใช้ค่าในไฟล์นี้ก่อนเปิดระบบ

ดังนั้น Search ไม่ถือว่าการเชื่อมต่อปลอดภัยจากการตั้งค่าใน frontend เพียงอย่างเดียว
แต่พึ่งพา TLS termination ของ deployment layer

## จุดพึ่งพา REG

Search แสดงข้อมูลกิจกรรมและส่งผู้ใช้ต่อไปยัง Google Form เท่านั้น
การลงทะเบียนจริงและการเตรียมข้อมูลเพื่อส่งเข้า REG อยู่นอก scope ของ Search

จุดเชื่อมต่อที่ Search ต้องพึ่งพาจากระบบกลาง:

1. ระบบกลางรับผิดชอบการเตรียมข้อมูล REG ให้พร้อมภายใน 1 วันทำการ
   เมื่อเอกสารครบถ้วน
2. Search ต้องไม่สร้างข้อมูลลงทะเบียนหรือเรียก REG โดยตรง
3. readiness ของ dependency นี้ถูกประกาศไว้ใน
   `deployment/https-config.yml` ภายใต้ `system_integrations.reg`
4. ก่อน production ต้องมีผู้ดูแล `system-registry` ยืนยัน contract และ readiness

เนื่องจาก spec ไม่ระบุ URL, schema หรือ authentication ของ REG จึงไม่กำหนดค่า
เหล่านั้นในฟีเจอร์ Search

## Audit Log

การอนุมัติ/ปฏิเสธเอกสารเป็นความรับผิดชอบของระบบกลาง ส่วนการเปลี่ยนสถานะกิจกรรม
ของ Admin มีจุดเชื่อมต่อ audit log ที่มีอยู่แล้ว:

- [`record_activity_audit_log`](../../backend/app/api/admin_activity.py)
  บันทึก `activity_id`, `admin_id`, `action_type`, `reason` และเวลา
- [`ActivityAuditLogService`](../../backend/app/services/activity_audit_log_service.py)
  ตรวจสอบ action ที่รองรับและบังคับให้มีเหตุผล
- action ที่รองรับคือ `delete` และ `suspend`
- โครงสร้างข้อมูลอยู่ใน
  [`activity_audit_log.py`](../../backend/app/models/activity_audit_log.py)

Search เพียงพึ่งพา audit log ของระบบกลางสำหรับการตรวจสอบย้อนหลัง และไม่สร้าง
workflow การอนุมัติ/ปฏิเสธเอกสารเพิ่ม

## ผลการตรวจ

| รายการ | หลักฐาน | สถานะ |
|---|---|---|
| Search ใช้ HTTPS | `deployment/https-config.yml: https.enabled`, `search_api.require_https` | ผ่านตาม deployment contract |
| REG readiness | `system_integrations.reg` และ owner `system-registry` | รอการยืนยันจากระบบกลางก่อน production |
| Audit Log | `record_activity_audit_log` และ `ActivityAuditLogService` | มีจุดเชื่อมต่อแล้ว |

