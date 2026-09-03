import json

def update_stock_and_notify(product_id, qty_change, threshold=15):
    # ตัวอย่างโค้ดแบบไม่มี context: รวม logic และ IO ไว้ด้วยกันทั้งหมด
    with open("stock.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    for item in data:
        if item["id"] == product_id:
            new_qty = item["quantity"] - qty_change
            if new_qty < 0:
                print("Error: สต็อกไม่พอ")
                return
            item["quantity"] = new_qty
            
            # hardcode การแจ้งเตือน ไม่แยก class ไม่ใช้ Observer
            if new_qty < threshold:
                print(f"[ALERT EMAIL] สต็อกสินค้า {item['name']} ต่ำกว่าเกณฑ์ เหลือ {new_qty}")
                print(f"[ALERT SMS] แจ้งเตือนด่วน สต็อกต่ำ เหลือ {new_qty}")
            break
            
    with open("stock.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def report_stock_value():
    with open("stock.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    report = {}
    total = 0
    for item in data:
        cat = item.get("category", "Uncategorized")
        val = item["price"] * item["quantity"]
        report[cat] = report.get(cat, 0) + val
        total += val
    print("รายงานมูลค่า:", report, "รวมทั้งหมด:", total)