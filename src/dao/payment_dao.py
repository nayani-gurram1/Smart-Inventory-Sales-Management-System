# src/dao/payment_dao.py
from typing import List, Dict, Optional
from src.config import get_supabase

def _sb():
    return get_supabase()

# Create Payment
def create_payment(order_id: int, amount: float, method: str = "CASH") -> Optional[Dict]:
    payload = {
        "order_id": order_id,
        "amount": amount,
        "method": method,
        "status": "PAID"
    }
    _sb().table("payments").insert(payload).execute()
    resp = _sb().table("payments").select("*").eq("order_id", order_id).order("payment_id", desc=True).limit(1).execute()
    return resp.data[0] if resp.data else None

# Get Payment by ID
def get_payment_by_id(payment_id: int) -> Optional[Dict]:
    resp = _sb().table("payments").select("*").eq("payment_id", payment_id).limit(1).execute()
    return resp.data[0] if resp.data else None

# List All Payments
def list_all_payments() -> List[Dict]:
    resp = _sb().table("payments").select("*").execute()
    return resp.data or []

# Refund Payment
def refund_payment(order_id: int) -> Optional[Dict]:
    payments = _sb().table("payments").select("*").eq("order_id", order_id).execute()
    if not payments.data:
        return None
    payment_id = payments.data[0]["payment_id"]
    _sb().table("payments").update({"status": "REFUNDED"}).eq("payment_id", payment_id).execute()
    return get_payment_by_id(payment_id)

# Delete Payment
def delete_payment(payment_id: int):
    _sb().table("payments").delete().eq("payment_id", payment_id).execute()
