import os
import sys
import streamlit as st
import pandas as pd
# ✅ Add src to sys.path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(ROOT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# ✅ Import Supabase config + services
from config import get_supabase
from services import product_service, order_service, customer_service, payment_service, report_service

# ✅ Initialize Supabase client (once)
supabase = get_supabase()
if not supabase:
    st.error("❌ Failed to initialize Supabase. Check your .env file for URL and KEY.")
else:
    st.sidebar.success("✅ Supabase Connected")

# ✅ Streamlit page config
st.set_page_config(page_title="🧾 Smart Inventory Dashboard", layout="wide")
st.title("📊 Smart Inventory & Sales Management System")

# Sidebar navigation
page = st.sidebar.selectbox(
    "Navigation",
    ["🏠 Dashboard", "📦 Products", "🧍 Customers", "📝 Orders", "💳 Payments", "📈 Reports"]
)

# ===============================
# 🏠 DASHBOARD
# ===============================
if page == "🏠 Dashboard":
    st.header("📊 Summary")
    try:
        orders = order_service.list_orders()
        products = product_service.list_products()
        payments = payment_service.list_payments()

        total_sales = sum([o["total_amount"] for o in orders]) if orders else 0
        total_products = len(products)
        total_orders = len(orders)
        total_payments = len(payments)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Sales", f"₹{total_sales:,.2f}")
        col2.metric("Total Products", total_products)
        col3.metric("Total Orders", total_orders)
        col4.metric("Payments", total_payments)
    except Exception as e:
        st.error(f"Error loading dashboard: {e}")

# ===============================
# 📦 PRODUCTS PAGE
# ===============================
elif page == "📦 Products":
    st.header("📦 Manage Products")

    if st.button("🔄 Refresh Products"):
        st.rerun()

    try:
        products = product_service.list_products()
        if products:
            st.dataframe(products, use_container_width=True)
        else:
            st.info("No products found.")
    except Exception as e:
        st.error(f"Error loading products: {e}")

    st.subheader("➕ Add Product")
    with st.form("add_product_form"):
        name = st.text_input("Product Name")
        sku = st.text_input("SKU")
        price = st.number_input("Price (₹)", min_value=0.0, format="%.2f")
        stock = st.number_input("Stock Quantity", min_value=0, step=1)
        category = st.text_input("Category")
        submitted = st.form_submit_button("Add Product")
        if submitted:
            try:
                product_service.add_product(name, sku, price, int(stock), category)
                st.success(f"✅ Product '{name}' added successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to add product: {e}")

# ===============================
# 🧍 CUSTOMERS PAGE
# ===============================
elif page == "🧍 Customers":
    st.header("🧍 Customer List")
    try:
        customers = customer_service.list_customers()
        if customers:
            st.dataframe(customers, use_container_width=True)
        else:
            st.info("No customers found.")
    except Exception as e:
        st.error(f"Error loading customers: {e}")

# ===============================
# 📝 ORDERS PAGE
# ===============================
elif page == "📝 Orders":
    st.header("📝 Orders List")

    status_filter = st.selectbox(
        "Filter by Status",
        ["ALL", "PENDING", "COMPLETED", "CANCELLED"]
    )

    try:
        orders = order_service.list_orders()
        if status_filter != "ALL":
            orders = [o for o in orders if o["status"] == status_filter]

        if orders:
            st.dataframe(orders, use_container_width=True)
        else:
            st.info("No orders match the selected status.")
    except Exception as e:
        st.error(f"Error loading orders: {e}")

# ===============================
# 💳 PAYMENTS PAGE
# ===============================
elif page == "💳 Payments":
    st.header("💳 Payment Records")
    try:
        payments = payment_service.list_payments()
        if payments:
            st.dataframe(payments, use_container_width=True)
        else:
            st.info("No payments recorded.")
    except Exception as e:
        st.error(f"Error loading payments: {e}")

# ===============================
# 📈 REPORTS PAGE (FINAL FIX)
# ===============================
elif page == "📈 Reports":
    st.header("📈 Generate Orders Report")

    status = st.selectbox("Select Order Status", ["COMPLETED", "PENDING", "CANCELLED"])

    # ✅ Generate report for selected status
    if st.button("Generate Report"):
        try:
            report_data = report_service.orders_report(status)
            st.success(f"Report generated for {status} orders.")
            if report_data:
                st.json(report_data)
            else:
                st.info(f"No {status} orders found.")
        except Exception as e:
            st.error(f"Error generating report: {e}")

    # ✅ Show filtered saved reports in table format
    st.subheader("📝 Saved Reports")
    try:
        reports = report_service.list_reports()

        # ✅ Match both "status=STATUS" or plain "STATUS" in criteria
        reports = [
            r for r in reports
            if status in r.get("criteria", "") or f"status={status}" in r.get("criteria", "")
        ]

        if reports:
            headers = ["Report ID", "Report Type", "Criteria", "Data", "Generated At"]
            rows = []

            for r in reports:
                data_field = r.get("data", {})
                criteria = r.get("criteria", "")
                data_str = str(data_field) if isinstance(data_field, dict) else str(data_field)

                rows.append([
                    r.get("report_id", ""),
                    r.get("report_type", ""),
                    criteria,
                    data_str,
                    r.get("generated_at", "")
                ])

            # ✅ Display clean table
            st.table([headers] + rows)
        else:
            st.info(f"No saved {status} reports found.")
    except Exception as e:
        st.error(f"Error loading reports: {e}")
