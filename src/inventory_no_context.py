# src/inventory_no_context.py
# โค้ดที่ได้จากการสั่ง AI โดยยังไม่มี .ai-rules.md (รวมทุกอย่างในไฟล์เดียว ขาด SRP/DIP)

class InventoryApp:
    def __init__(self):
        self.products = {}

    def add_product(self, sku, name, category, stock, price, threshold):
        self.products[sku] = {
            "name": name,
            "category": category,
            "stock": stock,
            "price": price,
            "threshold": threshold
        }

    def issue_stock(self, sku, amount, email, phone):
        if self.products[sku]["stock"] < amount:
            raise ValueError("สต็อกไม่พอ")
        self.products[sku]["stock"] -= amount
        
        # มีปัญหา: hardcode และรวม I/O print ปนกับ business logic ใน method เดียว
        if self.products[sku]["stock"] < self.products[sku]["threshold"]:
            print(f"[Email to {email}] สินค้า {self.products[sku]['name']} สต็อกต่ำ!")
            print(f"[SMS to {phone}] สินค้า {self.products[sku]['name']} สต็อกต่ำ!")

    def report_value(self):
        report = {}
        for p in self.products.values():
            report[p["category"]] = report.get(p["category"], 0) + (p["stock"] * p["price"])
        return report