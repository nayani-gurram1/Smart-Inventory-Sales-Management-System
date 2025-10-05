# src/services/product_service.py
from typing import List, Dict, Optional
from src.dao import product_dao
import datetime

class ProductError(Exception):
    pass

# Add a new product
def add_product(name: str, sku: str, price: float, stock: int = 0, category: Optional[str] = None) -> Dict:
    # Check if SKU already exists
    existing = product_dao.get_product_by_sku(sku)
    if existing:
        raise ProductError(f"SKU '{sku}' already exists for product '{existing['name']}'")
    
    payload = {
        "name": name,
        "sku": sku,
        "price": price,
        "stock": stock,
        "category": category,
        "created_at": datetime.datetime.utcnow().isoformat()
    }
    product = product_dao.insert_product(payload)
    return product

# List all products with optional category filter
def list_products(category: Optional[str] = None, limit: int = 100) -> List[Dict]:
    if category:
        return product_dao.list_products_by_category(category, limit)
    return product_dao.list_all_products(limit)

# Update product details
def update_product(prod_id: int, fields: Dict) -> Dict:
    if "sku" in fields:
        existing = product_dao.get_product_by_sku(fields["sku"])
        if existing and existing["prod_id"] != prod_id:
            raise ProductError(f"SKU '{fields['sku']}' already exists")
    updated = product_dao.update_product(prod_id, fields)
    return updated

# Delete a product
def delete_product(prod_id: int):
    existing = product_dao.get_product_by_id(prod_id)
    if not existing:
        raise Exception("Product not found")
    product_dao.delete_product(prod_id)
    return existing

# Reduce stock after an order
def reduce_stock(prod_id: int, quantity: int):
    product = product_dao.get_product_by_id(prod_id)
    if not product:
        raise ProductError(f"Product ID '{prod_id}' not found")
    if product["stock"] < quantity:
        raise ProductError(f"Not enough stock for '{product['name']}'. Available: {product['stock']}, Required: {quantity}")
    
    new_stock = product["stock"] - quantity
    product_dao.update_product(prod_id, {"stock": new_stock})
    return {"prod_id": prod_id, "new_stock": new_stock}

# Increase stock (for order cancellation or returns)
def increase_stock(prod_id: int, quantity: int):
    product = product_dao.get_product_by_id(prod_id)
    if not product:
        raise ProductError(f"Product ID '{prod_id}' not found")
    
    new_stock = product["stock"] + quantity
    product_dao.update_product(prod_id, {"stock": new_stock})
    return {"prod_id": prod_id, "new_stock": new_stock}
