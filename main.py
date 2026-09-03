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

def main():
    print("=== ยินดีต้อนรับสู่ระบบสต็อกร้านเขียนดี ===")

if __name__ == "__main__":
    main()
