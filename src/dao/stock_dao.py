# src/dao/stock_dao.py
from typing import List, Dict, Optional
from src.config import get_supabase

def _sb():
    """Return Supabase client instance."""
    return get_supabase()

# ---------------------------
# Update Stock
# ---------------------------
def update_stock(prod_id: int, new_stock: int) -> Optional[Dict]:
    """
    Update the stock value of a product in the database.
    """
    _sb().table("products").update({"stock": new_stock}).eq("prod_id", prod_id).execute()
    resp = _sb().table("products").select("*").eq("prod_id", prod_id).limit(1).execute()
    return resp.data[0] if resp.data else None

# ---------------------------
# List Low Stock Products
# ---------------------------
def list_low_stock(threshold: int = 5) -> List[Dict]:
    """
    Return a list of products with stock below the threshold.
    """
    resp = _sb().table("products").select("*").lt("stock", threshold).execute()
    return resp.data or []

# ---------------------------
# Get Stock for a Product
# ---------------------------
def get_stock(prod_id: int) -> Optional[int]:
    resp = _sb().table("products").select("stock").eq("prod_id", prod_id).limit(1).execute()
    return resp.data[0]["stock"] if resp.data else None
