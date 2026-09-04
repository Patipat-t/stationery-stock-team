from dataclasses import dataclass

@dataclass
class Product:
    sku: str
    name: str
    category: str
    stock: int
    price: float
    threshold: int

    def is_low_stock(self) -> bool:
        """ตรวจสอบว่าสต็อกต่ำกว่า threshold หรือไม่ (ต้องน้อยกว่าอย่างเคร่งครัด)"""
        return self.stock < self.threshold

@dataclass
class StockTransaction:
    sku: str
    amount: int
    transaction_type: str  # 'RECEIVE' หรือ 'ISSUE'
    remaining_stock: int