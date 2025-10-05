# src/main.py
import argparse
import json
from src.services import (
    product_service,
    customer_service,
    order_service,
    payment_service,
    stock_service,
    report_service
)

# ------------------- Product Commands -------------------
def cmd_product_add(args):
    try:
        p = product_service.add_product(
            args.name, args.sku, args.price, args.stock, args.category
        )
        print("Product created:")
        print(json.dumps(p, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_product_list(args):
    products = product_service.list_products()
    print(json.dumps(products, indent=2, default=str))

# ------------------- Order Commands -------------------
def cmd_order_create(args):
    items = []
    for item in args.items:
        try:
            pid, qty = item.split(":")
            items.append({"prod_id": int(pid), "quantity": int(qty)})
        except Exception:
            print("Invalid item format:", item)
            return
    try:
        order = order_service.create_order(args.customer, items)
        print("Order created:")
        print(json.dumps(order, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_order_show(args):
    try:
        order = order_service.get_order_details(args.order)
        print(json.dumps(order, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_order_cancel(args):
    try:
        order = order_service.cancel_order(args.order)
        print("Order cancelled:")
        print(json.dumps(order, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

# ------------------- Payment Commands -------------------
def cmd_payment_process(args):
    try:
        payment = payment_service.process_payment(args.order, args.method)
        print("Payment processed:")
        print(json.dumps(payment, indent=2, default=str))
    except Exception as e:
        print("Error:", e)


def cmd_payment_refund(args):
    try:
        payment = payment_service.refund_payment(args.order)
        print("Payment refunded:")
        print(json.dumps(payment, indent=2, default=str))
    except Exception as e:
        print("Error:", e)
def cmd_product_update(args):
    fields = {}
    if args.name: fields["name"] = args.name
    if args.sku: fields["sku"] = args.sku
    if args.price: fields["price"] = args.price
    if args.stock is not None: fields["stock"] = args.stock
    if args.category: fields["category"] = args.category

    try:
        updated = product_service.update_product(args.prod_id, fields)
        print("Product updated:")
        print(json.dumps(updated, indent=2, default=str))
    except Exception as e:
        print("Error:", e)
def cmd_product_delete(args):
    try:
        deleted = product_service.delete_product(args.prod_id)
        print("Product deleted:")
        print(json.dumps(deleted, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_customer_add(args):
    try:
        c = customer_service.add_customer(
            args.name, args.email, args.phone, args.city
        )
        print("Customer added:")
        print(json.dumps(c, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_customer_list(args):
    try:
        customers = customer_service.list_customers()
        print(json.dumps(customers, indent=2, default=str))
    except Exception as e:
        print("Error:", e)
def cmd_customer_update(args):
    fields = {}
    if args.loyalty_points is not None:
        fields["loyalty_points"] = args.loyalty_points

    if args.name: fields["name"] = args.name
    if args.email: fields["email"] = args.email
    if args.phone: fields["phone"] = args.phone
    if args.city: fields["city"] = args.city

    try:
        customer = customer_service.update_customer(args.cust_id, fields)
        print("Customer updated:")
        print(json.dumps(customer, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_customer_delete(args):
    try:
        result = customer_service.delete_customer(args.cust_id)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print("Error:", e)

def cmd_customer_search(args):
    try:
        results = customer_service.search_customers(args.keyword)
        print(json.dumps(results, indent=2, default=str))
    except Exception as e:
        print("Error:", e)
def cmd_payment_list(args):
    payments = payment_service.list_payments()
    print(json.dumps(payments, indent=2, default=str))
def cmd_order_list(args):
    from src.services import order_service
    try:
        orders = order_service.list_orders()
        print(json.dumps(orders, indent=2, default=str))
    except Exception as e:
        print(f"Error: {e}")



# ------------------- CLI Parser -------------------
def build_parser():
    parser = argparse.ArgumentParser(prog="SmartInventorySalesCLI")
    sub = parser.add_subparsers(dest="command")

    # Products
    prod_parser = sub.add_parser("product")
    prod_sub = prod_parser.add_subparsers(dest="action")

    add_prod = prod_sub.add_parser("add")
    add_prod.add_argument("--name", required=True)
    add_prod.add_argument("--sku", required=True)
    add_prod.add_argument("--price", type=float, required=True)
    add_prod.add_argument("--stock", type=int, default=0)
    add_prod.add_argument("--category", default=None)
    add_prod.set_defaults(func=cmd_product_add)

    list_prod = prod_sub.add_parser("list")
    list_prod.set_defaults(func=cmd_product_list)

    # --- Update Product ---
    update_prod = prod_sub.add_parser("update")
    update_prod.add_argument("--prod_id", type=int, required=True)
    update_prod.add_argument("--name")
    update_prod.add_argument("--sku")
    update_prod.add_argument("--price", type=float)
    update_prod.add_argument("--stock", type=int)
    update_prod.add_argument("--category")
    update_prod.set_defaults(func=cmd_product_update)
    # --- Delete Product ---
    delete_prod = prod_sub.add_parser("delete")
    delete_prod.add_argument("--prod_id", type=int, required=True)
    delete_prod.set_defaults(func=cmd_product_delete)
    # --- Customers ---
    cust_parser = sub.add_parser("customer")
    cust_sub = cust_parser.add_subparsers(dest="action")

# Add Customer
    add_cust = cust_sub.add_parser("add")
    add_cust.add_argument("--name", required=True)
    add_cust.add_argument("--email", required=True)
    add_cust.add_argument("--phone", required=True)
    add_cust.add_argument("--city", default=None)
    add_cust.set_defaults(func=cmd_customer_add)

# List Customers
    list_cust = cust_sub.add_parser("list")
    list_cust.set_defaults(func=cmd_customer_list)
    # update customer
    update_cust = cust_sub.add_parser("update")
    update_cust.add_argument("--cust_id", type=int, required=True)
    update_cust.add_argument("--name")
    update_cust.add_argument("--email")
    update_cust.add_argument("--phone")
    update_cust.add_argument("--city")
    update_cust.set_defaults(func=cmd_customer_update)
    update_cust.add_argument("--loyalty_points", type=int)


# delete customer
    delete_cust = cust_sub.add_parser("delete")
    delete_cust.add_argument("--cust_id", type=int, required=True)
    delete_cust.set_defaults(func=cmd_customer_delete)

# search customer
    search_cust = cust_sub.add_parser("search")
    search_cust.add_argument("--keyword", required=True)
    search_cust.set_defaults(func=cmd_customer_search)


    # Orders
    order_parser = sub.add_parser("order")
    order_sub = order_parser.add_subparsers(dest="action")

    create_order_parser = order_sub.add_parser("create")
    create_order_parser.add_argument("--customer", type=int, required=True)
    create_order_parser.add_argument(
        "--items", nargs="+", required=True, help="prod_id:qty"
    )
    create_order_parser.set_defaults(func=cmd_order_create)

    show_order_parser = order_sub.add_parser("show")
    show_order_parser.add_argument("--order", type=int, required=True)
    show_order_parser.set_defaults(func=cmd_order_show)

    cancel_order_parser = order_sub.add_parser("cancel")
    cancel_order_parser.add_argument("--order", type=int, required=True)
    cancel_order_parser.set_defaults(func=cmd_order_cancel)
    # order list
    list_order = order_sub.add_parser("list", help="List all orders")
    list_order.set_defaults(func=cmd_order_list)


    # Payments
    # --- Payments ---
    pay_parser = sub.add_parser("payment")
    pay_sub = pay_parser.add_subparsers(dest="action")  # pay_sub must be defined first

    process_pay = pay_sub.add_parser("process")
    process_pay.add_argument("--order", type=int, required=True)
    process_pay.add_argument("--method", default="CASH")
    process_pay.set_defaults(func=cmd_payment_process)

    refund_pay = pay_sub.add_parser("refund")
    refund_pay.add_argument("--order", type=int, required=True)
    refund_pay.set_defaults(func=cmd_payment_refund)

# NEW: list payments
    list_pay = pay_sub.add_parser("list")
    list_pay.set_defaults(func=cmd_payment_list)

    # In build_parser() under sub = parser.add_subparsers(dest="command")
    report_parser = sub.add_parser("report")
    report_sub = report_parser.add_subparsers(dest="action")

# Orders report
    orders_r = report_sub.add_parser("orders")
    orders_r.add_argument("--status")
    orders_r.set_defaults(func=lambda args: print(json.dumps(report_service.orders_report(args.status), indent=2, default=str)))

# Payments report
    payments_r = report_sub.add_parser("payments")
    payments_r.add_argument("--status")
    payments_r.add_argument("--method")
    payments_r.set_defaults(func=lambda args: print(json.dumps(report_service.payments_report(args.status, args.method), indent=2, default=str)))

# Customers report
    customers_r = report_sub.add_parser("customers")
    customers_r.add_argument("--min_loyalty", type=int)
    customers_r.set_defaults(func=lambda args: print(json.dumps(report_service.customers_report(args.min_loyalty), indent=2, default=str)))

# Revenue report
    revenue_r = report_sub.add_parser("revenue")
    revenue_r.add_argument("--start", required=True)
    revenue_r.add_argument("--end", required=True)
    revenue_r.set_defaults(func=lambda args: print(json.dumps(report_service.revenue_report(args.start, args.end), indent=2, default=str)))


    
# ------------------- Stock -------------------
    stock_parser = sub.add_parser("stock")
    stock_sub = stock_parser.add_subparsers(dest="action")

# stock update
    update_stock_parser = stock_sub.add_parser("update")
    update_stock_parser.add_argument("--product", type=int, required=True, help="Product ID")
    update_stock_parser.add_argument("--stock", type=int, required=True, help="New stock value")
    update_stock_parser.set_defaults(func=lambda args: print(json.dumps(stock_service.update_stock(args.product, args.stock), indent=2, default=str)))

# list low stock
    low_stock_parser = stock_sub.add_parser("low")
    low_stock_parser.add_argument("--threshold", type=int, default=5, help="Low stock threshold")
    low_stock_parser.set_defaults(func=lambda args: print(json.dumps(stock_service.list_low_stock(args.threshold), indent=2, default=str)))

# get stock of a product
    get_stock_parser = stock_sub.add_parser("get")
    get_stock_parser.add_argument("--product", type=int, required=True, help="Product ID")
    get_stock_parser.set_defaults(func=lambda args: print(json.dumps(stock_service.get_stock(args.product), indent=2, default=str)))
    
    list_reports_parser = report_sub.add_parser("list")
    list_reports_parser.set_defaults(func=lambda args: print(json.dumps(report_service.list_all_reports(), indent=2, default=str)))

    return parser
# ------------------- Main -------------------
def main():
    parser = build_parser()
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
