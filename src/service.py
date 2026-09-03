from typing import Dict, List, Optional
from src.models import Product
from src.notifiers import StockObserver

class InventoryService:
    def __init__(self, observers: Optional[List[StockObserver]] = None) -> None:
        """ระบบคลังสินค้า รับ Observer ผ่าน Constructor (Dependency Injection)"""
        self._products: Dict[str, Product] = {}
        self._observers: List[StockObserver] = observers if observers is not None else []

    def register_observer(self, observer: StockObserver) -> None:
        """เพิ่มผู้รับการแจ้งเตือน (Observer Pattern)"""
        self._observers.append(observer)

    def add_product(self, product: Product) -> None:
        """เพิ่มสินค้าเข้าสู่ระบบ"""
        self._products[product.sku] = product

    def receive_stock(self, sku: str, amount: int) -> int:
        """บันทึกรับสินค้าเข้าคลัง"""
        if amount <= 0:
            raise ValueError("จำนวนรับเข้าต้องมากกว่า 0")
        if sku not in self._products:
            raise KeyError("ไม่พบรหัสสินค้าในระบบ")
        
        self._products[sku].stock += amount
        return self._products[sku].stock

    def issue_stock(self, sku: str, amount: int) -> int:
        """บันทึกจ่ายสินค้า และแจ้งเตือนหากสต็อกต่ำกว่าเกณฑ์"""
        if amount <= 0:
            raise ValueError("จำนวนจ่ายออกต้องมากกว่า 0")
        if sku not in self._products:
            raise KeyError("ไม่พบรหัสสินค้าในระบบ")
        
        product = self._products[sku]
        if product.stock < amount:
            raise ValueError("สต็อกสินค้าไม่เพียงพอสำหรับการจ่ายออก")
        
        product.stock -= amount
        
        if product.is_low_stock():
            self._notify_observers(product)
            
        return product.stock

    def _notify_observers(self, product: Product) -> None:
        """ส่งแจ้งเตือนไปยัง Observer ทุกตัว"""
        for observer in self._observers:
            observer.update(
                product_name=product.name,
                remaining_stock=product.stock,
                threshold=product.threshold
            )

    def calculate_stock_value_by_category(self) -> Dict[str, float]:
        """คำนวณมูลค่าสต็อกรวมแยกตามหมวดหมู่สินค้า"""
        category_values: Dict[str, float] = {}
        for product in self._products.values():
            val = product.stock * product.price
            category_values[product.category] = category_values.get(product.category, 0.0) + val
        return category_values