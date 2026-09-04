# บันทึกการทดลองและปรับปรุงผลลัพธ์ AI (AI Iteration Log)

## 1. ผลการวิเคราะห์โค้ดก่อนมี Context (ขั้นที่ 4: inventory_no_context.py)
จากผลการให้ AI เขียนโค้ดโดยอิงจาก spec.md เพียงอย่างเดียวโดยยังไม่มีไฟล์กฎ (.ai-rules.md) พบปัญหาเชิงสถาปัตยกรรมดังนี้:
1. **ขาด Type Hint และ Docstring:** ฟังก์ชันไม่มีการระบุ data type และไม่มีคำอธิบายฟังก์ชันภาษาไทยตามมาตรฐาน
2. **ละเมิด Single Responsibility Principle (SRP):** คลาส `InventoryApp` รับหน้าที่มากเกินไป ทั้งจัดการข้อมูลสินค้า, ตรวจสอบสต็อก, คำนวณมูลค่า และส่งการแจ้งเตือน
3. **Hardcode และ Coupling สูง:** method `issue_stock` มีการรับพารามิเตอร์ email และ phone เข้ามาตรงๆ พร้อมเรียกคำสั่ง `print` แจ้งเตือนฝังไว้ใน business logic
4. **ขาดความยืดหยุ่น (ละเมิด OCP/DIP):** ไม่สามารถเพิ่มช่องทางการแจ้งเตือนใหม่ได้หากไม่เข้าไปแก้ไขโค้ดเดิม

## 2. ตารางเปรียบเทียบก่อนและหลังมี Context (ขั้นที่ 6)
| ประเด็น | ก่อนมี context (ขั้นที่ 4) | หลังมี context (ขั้นที่ 6) |
|---|---|---|
| แยกไฟล์/ความรับผิดชอบ | รวมทุกอย่างไว้ใน class เดียวใน `inventory_no_context.py` | แยก 3 ไฟล์ชัดเจน: `models.py`, `notifiers.py`, `service.py` |
| type hint + docstring | ไม่มี Type hint และไม่มี docstring ภาษาไทย | มี Type hint ครบทุก signature และมี docstring ภาษาไทย |
| service ผูกกับ notifier ตรง ๆ หรือไม่ | ผูกตรงและเรียก print ปนใน business logic | ไม่ผูกตรง แยกผ่าน Protocol/Interface (`StockObserver`) |
| hardcode config หรือไม่ | hardcode รับ email และโทรศัพท์ใน method ตรง ๆ | แยกตั้งค่าผ่าน Object และใช้ Dependency Injection ผ่าน Constructor |

## 3. บันทึกรอบ Iteration ที่แก้ต้นทาง (ขั้นที่ 7: ปรับที่ Spec/Context ไม่แก้โค้ดมือ)

### รอบที่ 1: การตรวจสอบเงื่อนไขขอบเขตของ Threshold
- **ผลที่ผิด:** ตอนรันเทียบกับ Acceptance Criteria พบว่า logic ตรวจสอบเป็น `<= threshold` ส่งผลให้สินค้าที่มีสต็อกเท่ากับเกณฑ์พอดีเกิดการแจ้งเตือน (False Positive)
- **สาเหตุอยู่ที่:** Spec ใน Acceptance Criteria ของ US-02 ยังไม่ได้ระบุ Edge Case กรณีเท่ากันไว้อย่างรัดกุม
- **แก้ต้นทางอย่างไร:** เข้าไปเพิ่ม Scenario ใน `specs/spec.md` เน้นย้ำว่ากรณีเท่ากับ threshold พอดี ต้องไม่ส่งการแจ้งเตือน (ต้องน้อยกว่าอย่างเคร่งครัด)
- **ผลหลังแก้:** AI แก้ไขเงื่อนไขใน method `is_low_stock()` เป็น `stock < threshold` ถูกต้องตามโจทย์

### รอบที่ 2: ข้อห้ามการส่งข้อความผ่านเครือข่ายจริง
- **ผลที่ผิด:** AI พยายามเรียกใช้ library สำหรับส่งอีเมลจริง (smtplib)
- **สาเหตุอยู่ที่:** Context ในคำสั่งยังไม่ชัดเจน ทำให้ AI เข้าใจว่าต้องเชื่อมต่อ mail server
- **แก้ต้นทางอย่างไร:** ระบุข้อห้ามเจาะจงใน `.ai-rules.md` บรรทัด "ห้ามส่ง email/sms จริง ใช้ print แทน เช่น print('[Email] ...')"
- **ผลหลังแก้:** ทุก Notifier เปลี่ยนมาใช้คำสั่ง `print()` จำลอง ไม่มีการเรียก network ภายนอกจริง