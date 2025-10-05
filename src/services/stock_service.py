# src/services/stock_service.py
from typing import List, Dict, Optional
import src.dao.stock_dao as stock_dao
import src.dao.product_dao as product_dao

# ---------------------------
# Update Stock
# ---------------------------
def update_stock(prod_id: int, new_stock: int) -> Optional[Dict]:
    product = product_dao.get_product_by_id(prod_id)
    if not product:
        raise ValueError(f"Product with ID {prod_id} does not exist.")
    
    updated_product = stock_dao.update_stock(prod_id, new_stock)
    return updated_product

# ---------------------------
# List Low Stock Products
# ---------------------------
def list_low_stock(threshold: int = 5) -> List[Dict]:
    return stock_dao.list_low_stock(threshold)

# ---------------------------
# Get Stock for Product
# ---------------------------
def get_stock(prod_id: int) -> Optional[int]:
    return stock_dao.get_stock(prod_id)
