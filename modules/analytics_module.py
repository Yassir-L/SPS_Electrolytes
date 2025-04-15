import streamlit as st
import pandas as pd
import os
from modules.data_loader import load_data

KPI_SHEET = "Market Intelligence"

@st.cache_data
def load_external_kpis_dict():
    try:
        df = load_data(KPI_SHEET)
        kpi_dict = df.set_index("KPI Name").to_dict("index")
        return kpi_dict, df
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

def show():
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
