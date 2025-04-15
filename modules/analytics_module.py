import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from modules.data_loader import load_data

PATENT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Patents")


@st.cache_data
def load_external_kpis():
    return {
        "Total Companies": st.session_state.get("mi_Total Companies", 0),
        "Total Current Capacity (t/year)": st.session_state.get("mi_Total Current Capacity (t/year)", 0),
        "Average Capacity per Company": st.session_state.get("mi_Average Capacity per Company", 0),
        "Industrial Scale Projects": st.session_state.get("mi_Industrial Scale Projects", 0)
    }

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

    st.subheader("📌 KPI Comparison")

    external_kpis = load_external_kpis()
    attainment_kpis = {}

    for kpi in internal_kpis:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.metric(label=f"Internal: {kpi}", value=f"{internal_kpis[kpi]:,.0f}")
        with col2:
            ext_value = external_kpis.get(kpi, 0)
            st.metric(label=f"External: {kpi}", value=f"{ext_value:,.0f}")
            if ext_value > 0:
                attainment = (internal_kpis[kpi] / ext_value) * 100
                attainment_kpis[kpi] = attainment
                st.caption(f"🎯 Attainment: {attainment:.1f}%")

    st.markdown("---")

    st.subheader("📚 Patents per Company (Pareto Chart)")

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
