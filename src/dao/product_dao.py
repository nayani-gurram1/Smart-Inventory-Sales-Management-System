# src/dao/product_dao.py
from typing import List, Dict, Optional
from src.config import get_supabase

def _sb():
    return get_supabase()

# ---------------------------
# Insert a new product
# ---------------------------
def insert_product(payload: Dict) -> Dict:
    _sb().table("products").insert(payload).execute()
    # Fetch the newly created product
    resp = _sb().table("products").select("*").eq("sku", payload["sku"]).limit(1).execute()
    return resp.data[0] if resp.data else {}

# ---------------------------
# List all products
# ---------------------------
def list_all_products(limit: int = 100) -> List[Dict]:
    resp = _sb().table("products").select("*").limit(limit).execute()
    return resp.data or []

# ---------------------------
# List products by category
# ---------------------------
def list_products_by_category(category: str, limit: int = 100) -> List[Dict]:
    resp = _sb().table("products").select("*").eq("category", category).limit(limit).execute()
    return resp.data or []

# ---------------------------
# Get product by ID
# ---------------------------
def get_product_by_id(prod_id: int) -> Optional[Dict]:
    resp = _sb().table("products").select("*").eq("prod_id", prod_id).limit(1).execute()
    return resp.data[0] if resp.data else None

# ---------------------------
# Get product by SKU
# ---------------------------
def get_product_by_sku(sku: str) -> Optional[Dict]:
    resp = _sb().table("products").select("*").eq("sku", sku).limit(1).execute()
    return resp.data[0] if resp.data else None

# ---------------------------
# Update product
# ---------------------------
def update_product(prod_id: int, fields: Dict) -> Dict:
    _sb().table("products").update(fields).eq("prod_id", prod_id).execute()
    return get_product_by_id(prod_id)

# ---------------------------
# Delete product
# ---------------------------
def delete_product(prod_id: int):
    _sb().table("products").delete().eq("prod_id", prod_id).execute()

