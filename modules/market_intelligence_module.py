import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

EXCEL_PATH = os.path.join("data", "LiPF6_data.xlsx")
EXTERNAL_KPI_SHEET = "External_KPIs"

KPI_FIELDS = [
    "Total Companies",
    "Total Current Capacity (t/year)",
    "Average Capacity per Company",
    "Industrial Scale Projects"
]

st.header("📈 Global LiPF₆ Market Intelligence")

# Load or create External KPI sheet
def load_external_kpis():
    try:
        df = pd.read_excel(EXCEL_PATH, sheet_name=EXTERNAL_KPI_SHEET)
        return df.set_index("KPI Name").to_dict("index")
    except:
        return {}

def save_external_kpis(data_dict):
    try:
        all_sheets = pd.read_excel(EXCEL_PATH, sheet_name=None)
        new_df = pd.DataFrame.from_dict(data_dict, orient="index").reset_index().rename(columns={"index": "KPI Name"})
        all_sheets[EXTERNAL_KPI_SHEET] = new_df
        with pd.ExcelWriter(EXCEL_PATH, engine="openpyxl", mode="w") as writer:
            for name, sheet_df in all_sheets.items():
                sheet_df.to_excel(writer, sheet_name=name, index=False)
    except Exception as e:
        st.error(f"Failed to save external KPIs: {e}")

stored_data = load_external_kpis()
updated_data = {}

st.subheader("🔢 Input External KPIs")
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

    # Store in session for analytics module
    st.session_state[f"mi_{kpi}"] = val

if st.button("🔖 Save External KPI Data"):
    save_external_kpis(updated_data)
    st.success("Saved successfully.")

st.markdown("---")
st.info("These values will be used for comparison in the Analytics Dashboard.")
