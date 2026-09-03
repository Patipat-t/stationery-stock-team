# Class Diagram: Inventory System

```mermaid
classDiagram
    class Product {
        +str sku
        +str name
        +str category
        +int stock
        +float price
        +int threshold
        +is_low_stock() bool
    }

    class StockTransaction {
        +str sku
        +int amount
        +str transaction_type
        +int remaining_stock
    }

    class StockObserver {
        <<Protocol>>
        +update(product_name: str, remaining_stock: int, threshold: int) None
    }

    class EmailNotifier {
        +str recipient_email
        +update(product_name: str, remaining_stock: int, threshold: int) None
    }

    class SMSNotifier {
        +str phone_number
        +update(product_name: str, remaining_stock: int, threshold: int) None
    }

    class NotifierFactory {
        +create_notifier(channel: str, target: str)$ StockObserver
    }

    class InventoryService {
        -dict _products
        -list _observers
        +register_observer(observer: StockObserver) None
        +add_product(product: Product) None
        +receive_stock(sku: str, amount: int) int
        +issue_stock(sku: str, amount: int) int
        -_notify_observers(product: Product) None
        +calculate_stock_value_by_category() dict
    }

    StockObserver <|.. EmailNotifier : implements
    StockObserver <|.. SMSNotifier : implements
    InventoryService o-- Product : aggregates
    InventoryService o-- StockObserver : notifies via DIP
    NotifierFactory ..> StockObserver : creates
```