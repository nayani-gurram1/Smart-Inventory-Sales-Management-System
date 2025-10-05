# src/services/payment_service.py
from typing import Optional
from src.dao import payment_dao, order_dao

def process_payment(order_id: int, method: str = "CASH") -> Optional[dict]:
    order = order_dao.get_order_by_id(order_id)
    if not order:
        raise Exception(f"Order {order_id} not found")

    if order["status"] == "CANCELLED":
        raise Exception("Cannot pay for a cancelled order")

    payment = payment_dao.create_payment(order_id, order["total_amount"], method)
    order_dao.update_order(order_id, {"status": "COMPLETED"})

    return payment

def refund_payment(order_id: int) -> Optional[dict]:
    payment = payment_dao.refund_payment(order_id)
    if not payment:
        raise Exception(f"No payment found for order {order_id}")

    order_dao.update_order(order_id, {"status": "CANCELLED"})
    return payment

def list_payments() -> list:
    return payment_dao.list_all_payments()

def get_payment(payment_id: int) -> Optional[dict]:
    return payment_dao.get_payment_by_id(payment_id)

def delete_payment(payment_id: int):
    payment_dao.delete_payment(payment_id)
