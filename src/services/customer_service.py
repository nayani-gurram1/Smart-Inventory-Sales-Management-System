# src/services/customer_service.py
import src.dao.customer_dao as customer_dao
from typing import List, Dict

class CustomerError(Exception):
    pass

# Add customer
def add_customer(name: str, email: str, phone: str, city: str = None) -> Dict:
    existing = customer_dao.get_customer_by_email(email)
    if existing:
        raise CustomerError("Customer with this email already exists")
    return customer_dao.create_customer(name, email, phone, city)

# List all customers
def list_customers() -> List[Dict]:
    return customer_dao.list_all_customers()

# Update customer
def update_customer(cust_id: int, fields: Dict) -> Dict:
    customer = customer_dao.get_customer_by_id(cust_id)
    if not customer:
        raise CustomerError("Customer not found")
    return customer_dao.update_customer(cust_id, fields)

# Delete customer
def delete_customer(cust_id: int):
    customer = customer_dao.get_customer_by_id(cust_id)
    if not customer:
        raise CustomerError("Customer not found")
    customer_dao.delete_customer(cust_id)
    return {"message": "Customer deleted successfully"}

# Search customer
def search_customers(keyword: str) -> List[Dict]:
    return customer_dao.search_customers(keyword)
