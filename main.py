import json

DB_FILE = "stock.json"

def load_data():
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def list_products():
    data = load_data()
    print("\n--- รายการสินค้าคงเหลือ ---")
    if not data:
        print("ไม่มีสินค้าในระบบ")
        return
    for item in data:
        print(f"[{item['id']}] {item['name']} | หมวด: {item['category']} | ราคา: {item['price']} บาท | เหลือ: {item['quantity']} ชิ้น")

def add_product(product_id, name, category, price, quantity):
    data = load_data()
    for item in data:
        if item["id"] == product_id:
            print(f"ข้อผิดพลาด: รหัสสินค้า {product_id} มีอยู่ในระบบแล้ว")
            return
    new_item = {
        "id": product_id,
        "name": name,
        "category": category,
        "price": float(price),
        "quantity": int(quantity)
    }
    data.append(new_item)
    save_data(data)
    print(f"เพิ่มสินค้า '{name}' เรียบร้อยแล้ว")

def main():
    print("=== ยินดีต้อนรับสู่ระบบสต็อกร้านเขียนดี ===")
    list_products()

if name == "main":
    main()
