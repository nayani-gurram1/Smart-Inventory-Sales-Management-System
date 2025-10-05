from typing import List, Dict
from src.dao import order_dao, product_dao
from src.models.order import Order, OrderItem

class OrderError(Exception):
    pass

def create_order(cust_id: int, items: List[Dict]) -> Dict:
    order_items = []
    total_amount = 0

    # Check product stock and prepare order items
    for item in items:
        prod = product_dao.get_product_by_id(item["prod_id"])
        if not prod:
            raise OrderError(f"Product ID {item['prod_id']} not found")
        if prod["stock"] < item["quantity"]:
            raise OrderError(f"Insufficient stock for {prod['name']}")

        # Deduct stock
        product_dao.update_product(prod["prod_id"], {"stock": prod["stock"] - item["quantity"]})

        order_item = OrderItem(prod_id=prod["prod_id"], quantity=item["quantity"], price=prod["price"])
        order_items.append(order_item)
        total_amount += order_item.price * order_item.quantity

    # Create order in DB
    order_record = order_dao.create_order(cust_id=cust_id, total_amount=total_amount)
    order_id = order_record["order_id"]

    # Insert order items
    for item in order_items:
        _sb = product_dao._sb()
        _sb.table("order_items").insert({
            "order_id": order_id,
            "prod_id": item.prod_id,
            "quantity": item.quantity,
            "price": item.price
        }).execute()

    # Return full order
    return get_order_details(order_id)

def get_order_details(order_id: int) -> Dict:
    order = order_dao.get_order_by_id(order_id)
    if not order:
        raise OrderError("Order not found")

    _sb = product_dao._sb()
    items_resp = _sb.table("order_items").select("*").eq("order_id", order_id).execute()
    order["items"] = items_resp.data or []
    return order

def cancel_order(order_id: int) -> Dict:
    order = get_order_details(order_id)
    if order["status"] != "PLACED":
        raise OrderError("Only PLACED orders can be cancelled")

    # Restock products
    _sb = product_dao._sb()
    for item in order["items"]:
        prod = product_dao.get_product_by_id(item["prod_id"])
        product_dao.update_product(prod["prod_id"], {"stock": prod["stock"] + item["quantity"]})

    # Update order status
    updated_order = order_dao.update_order(order_id, {"status": "CANCELLED"})
    return updated_order
def list_orders():
    return order_dao.list_all_orders()