# AI Iteration Log

## ขั้นที่ 4: ปัญหาที่พบจากการสั่ง AI โดยไม่มี Context (.ai-rules.md)
1. **โครงสร้างไฟล์:** โค้ดรวมทุกอย่างไว้ในไฟล์เดียว (`inventory_no_context.py`) ไม่แยก models, notifiers และ service ตามหลัก Modular Design
2. **Type Hints & Documentation:** ขาด Type Hint ใน signature และไม่มี docstring ภาษาไทยกำกับ
3. **Coupling & SOLID Violation:** มีการ hardcode print แจ้งเตือน email/sms ฝังอยู่ในฟังก์ชันอัปเดตสต็อกโดยตรง ไม่ได้ใช้ Observer Pattern หรือ Dependency Injection ทำให้ละเมิดหลัก SRP, OCP และ DIP
4. **Configuration:** มีการ hardcode threshold = 15 ไว้ในพารามิเตอร์โดยตรง