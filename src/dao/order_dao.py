from typing import List, Dict, Optional
from src.config import get_supabase
from src.utils.helpers import get_connection

def _sb():
    return get_supabase()

# -------------------------------
# Orders DAO
# -------------------------------
def create_order(cust_id: int, total_amount: float, discount: float = 0.0) -> Optional[Dict]:
    payload = {
        "cust_id": cust_id,
        "total_amount": total_amount,
        "discount": discount,
        "status": "PLACED"
    }
    _sb().table("orders").insert(payload).execute()
    resp = _sb().table("orders").select("*").eq("cust_id", cust_id).order("order_id", desc=True).limit(1).execute()
    return resp.data[0] if resp.data else None

def get_order_by_id(order_id: int) -> Optional[Dict]:
    resp = _sb().table("orders").select("*").eq("order_id", order_id).limit(1).execute()
    return resp.data[0] if resp.data else None

def list_orders_by_customer(cust_id: int) -> List[Dict]:
    resp = _sb().table("orders").select("*").eq("cust_id", cust_id).execute()
    return resp.data or []

def update_order(order_id: int, fields: Dict) -> Optional[Dict]:
    _sb().table("orders").update(fields).eq("order_id", order_id).execute()
    return get_order_by_id(order_id)

def delete_order(order_id: int):
    _sb().table("orders").delete().eq("order_id", order_id).execute()
def list_all_orders():
    resp = _sb().table("orders").select("*").execute()
    return resp.data or []
