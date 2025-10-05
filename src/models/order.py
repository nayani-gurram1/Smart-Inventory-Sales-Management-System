from typing import List, Dict, Optional
from datetime import datetime

class OrderItem:
    def __init__(self, prod_id: int, quantity: int, price: float):
        self.prod_id = prod_id
        self.quantity = quantity
        self.price = price
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def to_dict(self) -> Dict:
        return {
            "prod_id": self.prod_id,
            "quantity": self.quantity,
            "price": self.price,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

class Order:
    def __init__(self, cust_id: int, items: List[OrderItem], discount: float = 0.0):
        self.cust_id = cust_id
        self.items = items
        self.discount = discount
        self.status = "PLACED"
        self.total_amount = self.calculate_total()
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def calculate_total(self) -> float:
        total = sum(item.price * item.quantity for item in self.items)
        total -= self.discount
        return total

    def to_dict(self) -> Dict:
        return {
            "cust_id": self.cust_id,
            "items": [item.to_dict() for item in self.items],
            "total_amount": self.total_amount,
            "discount": self.discount,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
