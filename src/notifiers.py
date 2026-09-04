from typing import Protocol

class StockObserver(Protocol):
    def update(self, product_name: str, remaining_stock: int, threshold: int) -> None:
        """แจ้งเตือนเมื่อสต็อกสินค้าต่ำกว่าเกณฑ์"""
        ...

class EmailNotifier:
    def __init__(self, recipient_email: str) -> None:
        self.recipient_email = recipient_email

    def update(self, product_name: str, remaining_stock: int, threshold: int) -> None:
        """ส่งการแจ้งเตือนทาง Email (จำลองด้วย print)"""
        print(f"[Email] ถึง {self.recipient_email}: สินค้า '{product_name}' สต็อกต่ำกว่าเกณฑ์! (คงเหลือ: {remaining_stock}, เกณฑ์: {threshold})")

class SMSNotifier:
    def __init__(self, phone_number: str) -> None:
        self.phone_number = phone_number

    def update(self, product_name: str, remaining_stock: int, threshold: int) -> None:
        """ส่งการแจ้งเตือนทาง SMS (จำลองด้วย print)"""
        print(f"[SMS] ถึง {self.phone_number}: สินค้า '{product_name}' สต็อกต่ำกว่าเกณฑ์! (คงเหลือ: {remaining_stock})")

class NotifierFactory:
    @staticmethod
    def create_notifier(channel: str, target: str) -> StockObserver:
        """สร้าง Object แจ้งเตือนตามช่องทาง (Factory Pattern)"""
        channel_lower = channel.strip().lower()
        if channel_lower == "email":
            return EmailNotifier(recipient_email=target)
        elif channel_lower == "sms":
            return SMSNotifier(phone_number=target)
        else:
            raise ValueError(f"ไม่รองรับช่องทางการแจ้งเตือน: {channel}")