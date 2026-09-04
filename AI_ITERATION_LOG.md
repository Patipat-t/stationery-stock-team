# บันทึกการทดลองและปรับปรุงผลลัพธ์ AI (AI Iteration Log)

## 1. ผลการวิเคราะห์โค้ดก่อนมี Context (ขั้นที่ 4: inventory_no_context.py)
จากการผลการให้ AI เขียนโค้ดอิงจาก `spec.md` เพียงอย่างเดียวโดยยังไม่มีไฟล์กฎ (`.ai-rules.md`) พบปัญหาเชิงสถาปัตยกรรมดังนี้:
* **ขาด Type Hint และ Docstring:** ฟังก์ชันไม่มีการระบุ data type และไม่มีคำอธิบายฟังก์ชันภาษาไทยตามมาตรฐาน
* **ละเมิด Single Responsibility Principle (SRP):** คลาส `InventoryApp` รับหน้าที่มากเกินไป ทั้งจัดการข้อมูลสินค้า, ตรวจสอบสต็อก, คำนวณมูลค่า และส่งการแจ้งเตือน
* **Hardcode และ Coupling สูง:** method `issue_stock` มีการรับพารามิเตอร์ `email` และ `phone` เข้ามาตรง ๆ พร้อมเรียกคำสั่ง `print` แจ้งเตือนฝังไว้ใน business logic
* **ขาดความยืดหยุ่น (ละเมิด OCP/DIP):** ไม่สามารถเพิ่มช่องทางการแจ้งเตือนใหม่ได้หากไม่เข้าไปแก้ไขโค้ดเดิม

---

## 2. ตารางเปรียบเทียบก่อนและหลังมี Context (ขั้นที่ 6)

| ประเด็น | ก่อนมี context (ขั้นที่ 4) | หลังมี context (ขั้นที่ 6) |
| :--- | :--- | :--- |
| **การแยกไฟล์ / ความรับผิดชอบ** | รวมทุกอย่างไว้ใน class เดียวใน `inventory_no_context.py` | แยก 3 ไฟล์ชัดเจน: `models.py`, `notifiers.py`, `service.py` |
| **Type Hint + Docstring** | ไม่มี Type hint และไม่มี docstring ภาษาไทย | มี Type hint ครบทุก signature และมี docstring ภาษาไทย |
| **ความผูกพันของ Service กับ Notifier** | ผูกตรงและเรียก `print` ปนใน business logic | ไม่ผูกตรง แยกผ่าน Protocol/Interface (`StockObserver`) |
| **การตั้งค่า Configuration** | hardcode รับ email และโทรศัพท์ใน method ตรง ๆ | แยกตั้งค่าผ่าน Object และใช้ Dependency Injection ผ่าน Constructor |

---

## 3. บันทึกรอบ Iteration ที่แก้ต้นทาง (ขั้นที่ 7: ปรับที่ Spec/Context ไม่แก้โค้ดมือ)

### รอบที่ 1: การตรวจสอบเงื่อนไขขอบเขตของ Threshold
* **ผลที่ผิด:** ตอนรันเทียบกับ Acceptance Criteria พบว่า logic ตรวจสอบเป็น `<= threshold` ส่งผลให้สินค้าที่มีสต็อกเท่ากับเกณฑ์พอดีเกิดการแจ้งเตือน (False Positive)
* **สาเหตุอยู่ที่:** Spec ใน Acceptance Criteria ของ US-02 ยังไม่ได้ระบุ Edge Case กรณีเท่ากับไว้อย่างรัดกุม
* **แก้ต้นทางอย่างไร:** เข้าไปเพิ่ม Scenario ใน `specs/spec.md` เน้นย้ำว่ากรณีเท่ากับ threshold พอดี ต้องไม่ส่งการแจ้งเตือน (ต้องน้อยกว่าอย่างเคร่งครัด)
* **ผลหลังแก้:** AI แก้ไขเงื่อนไขใน method `is_low_stock()` เป็น `stock < threshold` ถูกต้องตามโจทย์

### รอบที่ 2: ข้อห้ามการส่งข้อความผ่านเครือข่ายจริง
* **ผลที่ผิด:** AI พยายามเรียกใช้ library สำหรับส่งอีเมลจริง (`smtplib`)
* **สาเหตุอยู่ที่:** Context ในคำสั่งยังไม่ชัดเจน ทำให้ AI เข้าใจว่าต้องเชื่อมต่อ mail server
* **แก้ต้นทางอย่างไร:** ระบุข้อห้ามเจาะจงใน `.ai-rules.md` บรรทัด "ห้ามส่ง email/sms จริง ให้ print แทน เช่น `print('[Email] ...')`"
* **ผลหลังแก้:** ทุก Notifier เปลี่ยนมาใช้คำสั่ง `print()` จำลอง ไม่มีการเรียก network ภายนอกจริง

---

## 4. บันทึกคำสั่ง Prompt ที่ใช้งานจริง

* **ขั้นที่ 3 (Review Spec):**
  ```text
  ช่วยรีวิว specs/spec.md ต่อไปนี้ โดยอย่าเพิ่งเขียนโค้ด ให้เสนอเป็น checklist สั้น ๆ ในประเด็น: ข้อกำหนดที่กำกวม, จุดที่อาจขัดแย้งกันเอง, และ Edge cases ที่ยังไม่ได้ระบุ
  ```
* **ขั้นที่ 4 (Generate โค้ดแบบไม่มี Context):**
  ```text
  จงเขียนโปรแกรมระบบจัดการสต็อกสินค้าภาษา Python ตามข้อกำหนดใน specs/spec.md ต่อไปนี้ [แนบเนื้อหา spec.md]
  ```
* **ขั้นที่ 6 (Generate โค้ดแบบมี Context):**
  ```text
  จงสร้างระบบ Inventory ตามสถาปัตยกรรมและกฎเกณฑ์ใน .ai-rules.md และตรงตามข้อกำหนดใน specs/spec.md ต่อไปนี้อย่างเคร่งครัด โดยแยกโค้ดออกเป็น 3 ไฟล์ models.py, notifiers.py, และ service.py [แนบเนื้อหา spec.md และ .ai-rules.md]
  ```
* **ขั้นที่ 8 (สร้าง Diagrams):**
  ```text
  ช่วยสร้าง Mermaid code สำหรับ Class Diagram และ Sequence Diagram (ตอนตัดจ่ายสินค้าแล้วสต็อกต่ำกว่าเกณฑ์จนส่งแจ้งเตือน) โดยอ้างอิงจากโค้ดใน models.py, notifiers.py และ service.py
  ```
* **ขั้นที่ 10 (Refactor ด้วย Factory + Observer):**
  ```text
  ปรับปรุงโค้ดระบบเพื่อแก้ปัญหาการละเมิด OCP และ DIP โดยนำ NotifierFactory มาใช้สร้าง Notifier และใช้ Observer Pattern ใน InventoryService เพื่อให้สามารถรองรับการแจ้งเตือนหลายช่องทางพร้อมกันได้โดยไม่แก้ไข Business Logic เดิม
  ```

---

## 5. เครื่องมือ AI ที่ใช้งาน
* **AI Tool:** Google Gemini 1.5 Pro (ผ่าน Google AI Studio) / GitHub Copilot
