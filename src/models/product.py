# src/models/product.py
from typing import Optional

class Product:
    def __init__(self, prod_id: int, name: str, sku: str, price: float, stock: int, category: Optional[str] = "General"):
        self.prod_id = prod_id
        self.name = name
        self.sku = sku
        self.price = price
        self.stock = stock
        self.category = category or "General"

    def __repr__(self):
        return f"<Product id={self.prod_id} name={self.name} sku={self.sku} stock={self.stock} category={self.category}>"

    # ---------------------------
    # Business Logic
    # ---------------------------
    def reduce_stock(self, quantity: int):
        if quantity > self.stock:
            raise ValueError(f"Insufficient stock for product '{self.name}'")
        self.stock -= quantity
        return self.stock

    def increase_stock(self, quantity: int):
        self.stock += quantity
        return self.stock

    def update_price(self, new_price: float):
        if new_price < 0:
            raise ValueError("Price cannot be negative")
        self.price = new_price
        return self.price

    def update_category(self, new_category: str):
        if not new_category:
            raise ValueError("Category cannot be empty")
        self.category = new_category
        return self.category

    # ---------------------------
    # Display / Reporting
    # ---------------------------
    def to_dict(self):
        return {
            "prod_id": self.prod_id,
            "name": self.name,
            "sku": self.sku,
            "price": self.price,
            "stock": self.stock,
            "category": self.category
        }

    def is_low_stock(self, threshold: int = 5):
        return self.stock <= threshold
