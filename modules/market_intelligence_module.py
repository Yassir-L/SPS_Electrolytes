import streamlit as st
import pandas as pd
import os
import json
import json
from modules.data_loader import load_data, save_data

KPI_FILE = os.path.join("data", "external_kpis.txt")
KPI_TEXT_PATH = os.path.join("data", "external_kpis.json")

@st.cache_data
def load_external_kpis_dict():
    try:
        if os.path.exists(KPI_FILE):
            with open(KPI_FILE, "r") as f:
                kpi_dict = json.load(f)
            df = pd.DataFrame.from_dict(kpi_dict, orient="index").reset_index().rename(columns={"index": "KPI Name"})
            return kpi_dict, df
        else:
            return {}, pd.DataFrame(columns=["KPI Name", "Value", "Reference(s)", "Comment"])
    except Exception as e:
        st.error(f"[DEBUG] Error loading external KPIs: {e}")
        return {}, pd.DataFrame(columns=["KPI Name", "Value", "Reference(s)", "Comment"])", "Comment"])
    except Exception as e:
        st.error(f"[DEBUG] Error loading external KPIs: {e}")
        return {}, pd.DataFrame(columns=["KPI Name", "Value", "Reference(s)", "Comment"])

def get_internal_kpis(companies_df):
    return {
        "Total Companies": len(companies_df),
        "Total Current Capacity (t/year)": companies_df["Current Capacity (t/year)"].sum(),
        "Average Capacity per Company": companies_df["Current Capacity (t/year)"].mean(),
        "Industrial Scale Projects": (companies_df["Project Scale"].str.contains("industrial", case=False)).sum()
    }

KPI_FIELDS = [
    "Total Companies",
    "Total Current Capacity (t/year)",
    "Average Capacity per Company",
    "Industrial Scale Projects"
]

def save_external_kpis(data_dict):
    try:
        # Save to Excel
        new_df = pd.DataFrame.from_dict(data_dict, orient="index").reset_index().rename(columns={"index": "KPI Name"})
        save_data(new_df, KPI_SHEET)

        # Save to JSON text file (overwrite)
        with open(KPI_TEXT_PATH, "w") as f:
            json.dump(data_dict, f, indent=2)

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

    stored_data, current_df = load_external_kpis_dict()
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

    st.markdown("---")

    st.header("📊 Analytics Dashboard")

    companies_df = load_data("Companies")
    internal_kpis = get_internal_kpis(companies_df)
    external_kpis_dict, raw_external_df = load_external_kpis_dict()

    st.subheader("📌 KPI Comparison (Internal vs. External)")

    for kpi_name, internal_val in internal_kpis.items():
        internal_val = round(internal_val, 2)
        external_val = round(float(external_kpis_dict.get(kpi_name, {}).get("Value", 0)), 2)
        attainment = round((internal_val / external_val * 100), 1) if external_val else 0

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label=f"📦 {kpi_name} (Internal)", value=internal_val)
        with col2:
            st.metric(label=f"🌐 {kpi_name} (External)", value=external_val)
        with col3:
            st.metric(label=f"🎯 Attainment (%)", value=f"{attainment}%")

    st.markdown("---")

    st.subheader("🔧 [DEBUG] Raw External KPI Data")
    st.dataframe(raw_external_df, use_container_width=True)

    st.markdown("---")

    st.subheader("📚 Patents per Company (Pareto Chart)")

    import plotly.graph_objects as go

    PATENT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Patents")

    search_keywords = st.text_input("🔎 Filter patents by keyword (comma separated):")
    keywords = [kw.strip().lower() for kw in search_keywords.split(",") if kw.strip()] if search_keywords else []

    patent_counts = {}

    if os.path.exists(PATENT_FOLDER):
        files = [f for f in os.listdir(PATENT_FOLDER) if f.lower().endswith(".xlsx")]
        for file in files:
            path = os.path.join(PATENT_FOLDER, file)
            try:
                df = pd.read_excel(path)
                company = os.path.splitext(file)[0]
                if keywords:
                    df_filtered = df[df.apply(lambda row: any(kw in str(cell).lower() for cell in row for kw in keywords), axis=1)]
                    count = len(df_filtered)
                else:
                    count = len(df)
                patent_counts[company] = count
            except Exception as e:
                st.warning(f"❌ Error reading {file}: {e}")

    if patent_counts:
        sorted_items = sorted(patent_counts.items(), key=lambda x: x[1], reverse=True)
        companies, counts = zip(*sorted_items)

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=companies,
            y=counts,
            marker_color='skyblue',
            text=counts,
            textposition='outside'
        ))
        fig.update_layout(
            title="Number of Patents per Company",
            yaxis_title="Patent Count",
            xaxis_title="Company",
            template="plotly_white",
            height=450
        )
        st.plotly_chart(fig)
    else:
        st.info("No patent data available or no matches found.")
