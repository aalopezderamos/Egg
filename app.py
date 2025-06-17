import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("📦 Supplier Orders Overview")

# Upload Excel file
uploaded_file = st.file_uploader("Upload 'Master Incoming Report.xlsm'", type=["xlsm"])

if uploaded_file:
    # Read sheets
    supplier_df = pd.read_excel(uploaded_file, sheet_name="Supplier Info")
    po_df = pd.read_excel(uploaded_file, sheet_name="PO Info")

    # Clean column names
    supplier_df.columns = supplier_df.columns.str.strip()
    po_df.columns = po_df.columns.str.strip()

    # Dropdown for day of the week
    selected_day = st.selectbox("Select Order Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])

    # Filter suppliers by day
    filtered_suppliers = supplier_df[supplier_df["Order Day"] == selected_day]

    if filtered_suppliers.empty:
        st.warning(f"No suppliers found for {selected_day}.")
    else:
        st.subheader(f"Suppliers for {selected_day}")
        for supplier in filtered_suppliers["Supplier Name"].unique():
            with st.expander(f"📍 {supplier}"):
                supplier_pos = po_df[(po_df["Supplier"] == supplier) & (po_df["PO Num"].notna())]

                if supplier_pos.empty:
                    st.info("No open POs for this supplier.")
                    continue

                selected_po = st.selectbox(
                    f"Select PO for {supplier}",
                    supplier_pos["PO Num"].unique(),
                    key=supplier
                )

                po_details = supplier_pos[supplier_pos["PO Num"] == selected_po][[
                    "Purchase ID", "Receive Date", "Product", "Ordered"
                ]]

                st.write(po_details)
