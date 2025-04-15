import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from modules.data_loader import load_data

EXCEL_PATH = os.path.join("data", "LiPF6_Market_Intelligence.xlsx")
KPI_SHEET = "Market Intelligence"
PATENT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Patents")

# Load external KPIs directly from Market Intelligence file
@st.cache_data
def load_external_kpis_df():
    try:
        df = pd.read_excel(EXCEL_PATH, sheet_name=KPI_SHEET)
        return df
    except:
        return pd.DataFrame(columns=["KPI Name", "Value", "Reference(s)", "Comment"])

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
    external_kpis_df = load_external_kpis_df()

    st.subheader("📌 KPI Comparison")

    # Format table with attainment %
    comparison_rows = []
    for kpi_name, internal_val in internal_kpis.items():
        # Match row from external sheet
        external_row = external_kpis_df[external_kpis_df["KPI Name"] == kpi_name]
        if not external_row.empty:
            external_val = float(external_row["Value"].values[0])
            reference = external_row["Reference(s)"].values[0]
            comment = external_row["Comment"].values[0]
            attainment = (internal_val / external_val * 100) if external_val else 0
        else:
            external_val = 0
            reference = ""
            comment = ""
            attainment = 0

        comparison_rows.append({
            "KPI Name": kpi_name,
            "Internal Value": round(internal_val, 2),
            "External Value": round(external_val, 2),
            "🎯 Attainment (%)": round(attainment, 1),
            "Reference(s)": reference,
            "Comment": comment
        })

    st.dataframe(pd.DataFrame(comparison_rows), use_container_width=True)

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
