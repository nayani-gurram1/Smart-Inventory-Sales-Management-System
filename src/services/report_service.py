from src.dao import order_dao, payment_dao, customer_dao, report_dao

def orders_report(status=None):
    orders = order_dao.list_all_orders()
    filtered = [o for o in orders if o["status"] == status] if status else orders

    for order in filtered:
        report_dao.insert_report("orders", {
            "criteria": f"status={status}",
            "data": order
        })
    return filtered

def payments_report(status=None, method=None):
    payments = payment_dao.list_all_payments()
    filtered = payments

    if status:
        filtered = [p for p in filtered if p["status"] == status]
    if method:
        filtered = [p for p in filtered if p["method"] == method]

    for payment in filtered:
        report_dao.insert_report("payments", {
            "criteria": f"status={status}, method={method}",
            "data": payment
        })
    return filtered

def customers_report(min_loyalty=None):
    customers = customer_dao.list_all_customers()
    filtered = customers

    if min_loyalty is not None:
        filtered = [c for c in customers if c.get("loyalty_points", 0) >= min_loyalty]

    for customer in filtered:
        report_dao.insert_report("customers", {
            "criteria": f"min_loyalty={min_loyalty}",
            "data": customer
        })
    return filtered

def revenue_report(start, end):
    orders = order_dao.list_all_orders()
    filtered = [
        o for o in orders if start <= o["order_date"] <= end and o["status"] == "COMPLETED"
    ]

    revenue = sum(o["total_amount"] for o in filtered)

    report_dao.insert_report("revenue", {
        "criteria": f"{start} to {end}",
        "data": {"total_revenue": revenue}
    })
    return {"total_revenue": revenue}

def list_reports():
    return report_dao.list_reports()

