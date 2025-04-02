import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

def show():
    st.header("📈 Global LiPF₆ Market Intelligence")

    # Global LiPF₆ Market Data for 2024
    global_data = {
        "Metric": [
            "Effective Production Capacity (2024)",
            "Actual Production Output (2024)",
            "Market Value (2024)",
            "Projected Market Value (2031)",
            "CAGR (2024-2031)"
        ],
        "Value": [
            "390,000 metric tons",
            "187,000 metric tons",
            "$3.134 billion",
            "$5.946 billion",
            "9.7%"
        ],
        "Source": [
            "[EVTank](https://news.metal.com/newscontent/103222503/Prices-Are-Expected-to-Rise-The-LiPF6-Industry-May-Face-a-Supply-and-Demand-Tightening-Ahead-of-Schedule)",
            "[SMM Analysis](https://www.metal.com/en/newscontent/103144700)",
            "[Valuates Reports](https://reports.valuates.com/market-reports/QYRE-Auto-34C9597/global-lipf6)",
            "[Valuates Reports](https://reports.valuates.com/market-reports/QYRE-Auto-34C9597/global-lipf6)",
            "[Valuates Reports](https://reports.valuates.com/market-reports/QYRE-Auto-34C9597/global-lipf6)"
        ]
    }

    global_df = pd.DataFrame(global_data)

    # Display Global Market Data
    st.subheader("🌐 Global LiPF₆ Market Data (2024)")
    st.table(global_df)

    # Comparative Analysis with Internal Database
    st.subheader("🏭 Comparative Analysis with Internal Database")

    # Example internal database data (replace with actual data)
    internal_data = {
        "Company": ["Company A", "Company B", "Company C", "Company D", "Company E"],
        "Country": ["Country X", "Country Y", "Country Z", "Country W", "Country V"],
        "Production Capacity (2024)": [50000, 40000, 30000, 20000, 10000]  # in metric tons
    }

    internal_df = pd.DataFrame(internal_data)
    total_internal_capacity = internal_df["Production Capacity (2024)"].sum()

    # Calculate percentage share of each company
    internal_df["Global Capacity Share (%)"] = (internal_df["Production Capacity (2024)"] / 390000) * 100

    # Display Internal Database
    st.dataframe(internal_df)

    # Key Insights
    st.subheader("🔍 Key Insights")
    st.markdown(f"- **Total Internal Production Capacity (2024):** {total_internal_capacity:,} metric tons")
    st.markdown(f"- **Global Effective Production Capacity (2024):** 390,000 metric tons")
    st.markdown(f"- **Global Actual Production Output (2024):** 187,000 metric tons")
    st.markdown(f"- **Capacity Utilization Rate (2024):** {187000 / 390000 * 100:.2f}%")

    # Bar Chart: Internal Production Capacities
    st.subheader("📊 Internal Production Capacities")
    fig = go.Figure(data=[
        go.Bar(
            x=internal_df["Company"],
            y=internal_df["Production Capacity (2024)"],
            text=internal_df["Global Capacity Share (%)"].apply(lambda x: f"{x:.2f}%"),
            textposition='auto',
            marker_color='lightskyblue'
        )
    ])
    fig.update_layout(
        title="Company-wise Production Capacities (2024)",
        xaxis_title="Company",
        yaxis_title="Production Capacity (metric tons)",
        yaxis=dict(tickformat=","),
        template="plotly_white"
    )
    st.plotly_chart(fig)

    # Pie Chart: Global Capacity Distribution
    st.subheader("🍰 Global Capacity Distribution")
    labels = internal_df["Company"].tolist() + ["Other Global Capacity"]
    values = internal_df["Production Capacity (2024)"].tolist() + [390000 - total_internal_capacity]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_layout(
        title="Global LiPF₆ Production Capacity Distribution (2024)",
        template="plotly_white"
    )
    st.plotly_chart(fig)

    # Note on Data Accuracy
    st.info("**Note:** The internal database data is based on the provided example. Please ensure that your actual internal data is accurate and up-to-date for precise analysis.")

