import streamlit as st
import pandas as pd
import os

EXCEL_PATH = os.path.join("data", "LiPF6_Market_Intelligence.xlsx")
KPI_SHEET = "Market Intelligence"

KPI_FIELDS = [
    "Total Companies",
    "Total Current Capacity (t/year)",
    "Average Capacity per Company",
    "Industrial Scale Projects"
]

def load_external_kpis():
    try:
        df = pd.read_excel(EXCEL_PATH, sheet_name=KPI_SHEET)
        return df.set_index("KPI Name").to_dict("index"), df
    except:
        empty = pd.DataFrame(columns=["KPI Name", "Value", "Reference(s)", "Comment"])
        return {}, empty

def save_external_kpis(data_dict):
    try:
        new_df = pd.DataFrame.from_dict(data_dict, orient="index").reset_index().rename(columns={"index": "KPI Name"})
        with pd.ExcelWriter(EXCEL_PATH, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            new_df.to_excel(writer, sheet_name=KPI_SHEET, index=False)
    except FileNotFoundError:
        new_df = pd.DataFrame.from_dict(data_dict, orient="index").reset_index().rename(columns={"index": "KPI Name"})
        with pd.ExcelWriter(EXCEL_PATH, engine="openpyxl", mode="w") as writer:
            new_df.to_excel(writer, sheet_name=KPI_SHEET, index=False)
    except Exception as e:
        st.error(f"❌ Failed to save KPI data: {e}")

def clear_kpi_sheet():
    try:
        empty_df = pd.DataFrame(columns=["KPI Name", "Value", "Reference(s)", "Comment"])
        with pd.ExcelWriter(EXCEL_PATH, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            empty_df.to_excel(writer, sheet_name=KPI_SHEET, index=False)
        st.success("🧹 Sheet cleared successfully.")
    except Exception as e:
        st.error(f"❌ Failed to clear the sheet: {e}")

def show():
    st.header("📈 Global LiPF₆ Market Intelligence")

    if st.button("🧹 Clear All KPI Data (Warning: Cannot be undone)"):
        clear_kpi_sheet()

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

        # Store in session state for use in Analytics module
        st.session_state[f"mi_{kpi}"] = val

    if st.button("🔐 Save External KPI Data"):
        save_external_kpis(updated_data)
        st.success("✅ Saved successfully.")

    st.markdown("---")

    # 🔍 Raw Editable Table
    st.subheader("📋 Edit KPI Data (Raw Table)")
    edited_df = st.data_editor(current_df, num_rows="dynamic", use_container_width=True, key="editor")

    if st.button("💾 Save Table Changes"):
        try:
            with pd.ExcelWriter(EXCEL_PATH, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
                edited_df.to_excel(writer, sheet_name=KPI_SHEET, index=False)
            st.success("✅ Changes saved successfully.")
        except Exception as e:
            st.error(f"❌ Failed to save table edits: {e}")
