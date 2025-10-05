# src/dao/customer_dao.py
from typing import List, Dict, Optional
from src.config import get_supabase
from src.utils.helpers import get_connection

def _sb():
    """Return Supabase client instance."""
    return get_supabase()

# -------------------------------
# Create Customer
# -------------------------------
def create_customer(name: str, email: str, phone: str, city: Optional[str] = None) -> Optional[Dict]:
    """Insert a new customer into the database."""
    payload = {
        "name": name,
        "email": email,
        "phone": phone,
        "city": city
    }
    _sb().table("customers").insert(payload).execute()
    resp = _sb().table("customers").select("*").eq("email", email).limit(1).execute()
    return resp.data[0] if resp.data else None

# -------------------------------
# Read Customer
# -------------------------------
def get_customer_by_id(cust_id: int) -> Optional[Dict]:
    resp = _sb().table("customers").select("*").eq("cust_id", cust_id).limit(1).execute()
    return resp.data[0] if resp.data else None

def get_customer_by_email(email: str) -> Optional[Dict]:
    resp = _sb().table("customers").select("*").eq("email", email).limit(1).execute()
    return resp.data[0] if resp.data else None

def get_customer_by_phone(phone: str) -> Optional[Dict]:
    resp = _sb().table("customers").select("*").eq("phone", phone).limit(1).execute()
    return resp.data[0] if resp.data else None

def list_all_customers() -> List[Dict]:
    resp = _sb().table("customers").select("*").execute()
    return resp.data or []

# -------------------------------
# Update Customer
# -------------------------------
def update_customer(cust_id: int, fields: Dict) -> Optional[Dict]:
    """Update an existing customer with provided fields."""
    _sb().table("customers").update(fields).eq("cust_id", cust_id).execute()
    return get_customer_by_id(cust_id)

# -------------------------------
# Delete Customer
# -------------------------------
def delete_customer(cust_id: int):
    """Delete customer from the database."""
    _sb().table("customers").delete().eq("cust_id", cust_id).execute()

# -------------------------------
# Search Customers
# -------------------------------
def search_customers(keyword: str) -> List[Dict]:
    """
    Search customers by name, email, or city.
    Returns list of matching customers.
    """
    resp = _sb().table("customers").select("*") \
        .or_(f"name.ilike.%{keyword}%," +
             f"email.ilike.%{keyword}%," +
             f"city.ilike.%{keyword}%") \
        .execute()
    return resp.data or []
