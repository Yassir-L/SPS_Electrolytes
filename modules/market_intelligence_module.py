import streamlit as st
import pandas as pd
import os
from modules.data_loader import load_data, save_data

EXCEL_PATH = os.path.join("data", "LiPF6_data.xlsx")
KPI_SHEET = "External_KPIs"

KPI_FIELDS = [
    "Total Companies",
    "Total Current Capacity (t/year)",
    "Average Capacity per Company",
    "Industrial Scale Projects"
]

def load_external_kpis():
    try:
        df = load_data(KPI_SHEET)
        return df.set_index("KPI Name").to_dict("index"), df
    except:
        empty = pd.DataFrame(columns=["KPI Name", "Value", "Reference(s)", "Comment"])
        return {}, empty

def save_external_kpis(data_dict):
    try:
        new_df = pd.DataFrame.from_dict(data_dict, orient="index").reset_index().rename(columns={"index": "KPI Name"})
        save_data(new_df, KPI_SHEET)
    except Exception as e:
        st.error(f"❌ Failed to save KPI data: {e}")

def clear_kpi_sheet():
    try:
        empty_df = pd.DataFrame(columns=["KPI Name", "Value", "Reference(s)", "Comment"])
        save_data(empty_df, KPI_SHEET)
        st.success("🧹 Sheet cleared successfully.")
    except Exception as e:
        st.error(f"❌ Failed to clear the sheet: {e}")

def show():
    st.header("📈 Global LiPF₆ Market Intelligence")

    stored_data, current_df = load_external_kpis()
    updated_data = {}

    st.subheader("🧮 Input External KPIs")
    for kpi in KPI_FIELDS:
        st.markdown(f"### {kpi}")
        val = st.number_input(f"Value for {kpi}", value=float(stored_data.get(kpi, {}).get("Value", 0)), step=1.0, key=f"val_{kpi}")
        ref = st.text_input(f"Reference(s) for {kpi} (use | to separate multiple)", value=stored_data.get(kpi, {}).get("Reference(s)", ""), key=f"ref_{kpi}")
        comment = st.text_area(f"Comment for {kpi}", value=stored_data.get(kpi, {}).get("Comment", ""), key=f"comment_{kpi}")

        updated_data[kpi] = {
            "Value": val,
            "Reference(s)": ref,
            "Comment": comment
        }

    if st.button("🔐 Save External KPI Data"):
        save_external_kpis(updated_data)
        st.success("✅ Saved successfully.")
        st.rerun()

    if st.button("🧹 Clear All KPI Data (Warning: Cannot be undone)"):
        clear_kpi_sheet()
        st.rerun()

    st.markdown("---")

    st.subheader("📋 Edit KPI Data (Raw Table)")
    edited_df = st.data_editor(current_df, num_rows="dynamic", use_container_width=True, key="editor")

    if st.button("💾 Save Table Changes"):
        try:
            save_data(edited_df, KPI_SHEET)
            st.success("✅ Changes saved successfully.")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Failed to save table edits: {e}")
