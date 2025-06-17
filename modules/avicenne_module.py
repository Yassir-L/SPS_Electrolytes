import streamlit as st
import plotly.graph_objects as go
import pandas as pd


def show():
    st.title("📘 Experts Market Insights: LiPF₆")

    # --------- Section 1: Global Market Summary ---------
    st.header("📊 Global LiPF₆ Market Overview (2022–2024)")
    col1, col2, col3 = st.columns(3)
    col1.metric("2022 Demand", "172,000 t", "ASP: $49/kg")
    col2.metric("2023 Demand", "232,000 t", "ASP: $17/kg")
    col3.metric("2024 Demand", "302,000 t", "ASP: $9/kg")

    st.markdown("#### Demand Evolution")
    years = [2022, 2023, 2024]
    lipf6 = [172000, 232000, 302000]
    electrolyte = [1235000, 1660000, 2154000]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=lipf6, mode='lines+markers', name='LiPF₆ (tons)'))
    fig.add_trace(go.Scatter(x=years, y=electrolyte, mode='lines+markers', name='Electrolyte (tons)'))
    st.plotly_chart(fig, use_container_width=True)

    # --------- Section 2: Regional Demand Forecast (2030) ---------
    st.header("🌍 Regional Demand Forecast (2030)")
    demand_data = {
        'Region': ['China', 'Europe', 'North America', 'Other Asia (excl. China)', 'Rest of World'],
        'Battery Demand (GWh)': [1684, 909, 825, 288, 298],
        'Estimated LiPF₆ Share': ['High', 'Medium-High', 'Medium', 'Low-Medium', 'Low']
    }
    df_demand = pd.DataFrame(demand_data)
    st.dataframe(df_demand, use_container_width=True)

    fig_pie = go.Figure(data=[
        go.Pie(labels=df_demand['Region'], values=df_demand['Battery Demand (GWh)'], hole=.3)
    ])
    fig_pie.update_layout(title="Battery Demand Share (2030)")
    st.plotly_chart(fig_pie, use_container_width=True)

    # --------- Section 3: Key Companies ---------
    st.header("🏭 Leading Companies in LiPF₆ & Electrolytes")
    companies = pd.DataFrame({
        'Company': ['Tinci', 'Capchem', 'GTHR', 'Enchem', 'Soulbrain'],
        'Country': ['China', 'China', 'China', 'S. Korea', 'S. Korea'],
        'Role': ['Leader in LiPF₆ & Electrolytes', 'Top 3 in Electrolytes', 'Additives & Electrolytes', 'US/EU Expansion', 'High-performance Electrolytes'],
        'Revenue 2024': ['$1.7B', '$1.4B', 'N/A', 'N/A', 'N/A']
    })
    st.dataframe(companies, use_container_width=True)

    # --------- Section 4: Cost Structure ---------
    st.header("⚙️ Electrolyte Cost Breakdown (2024)")
    chemistries = ['LFP China', 'NMC China', 'High Perf China', 'LFP EU', 'NMC EU', 'High Perf EU']
    costs = {
        'Solvents': [1.05, 1.05, 1.27, 1.47, 1.47, 1.69],
        'LiPF₆': [1.2, 1.2, 1.4, 1.8, 1.8, 2.1],
        'Additives': [0.8, 1.2, 1.6, 1.3, 1.8, 2.2],
        'Conversion': [0.46, 0.46, 0.46, 0.96, 0.96, 0.96]
    }
    df_costs = pd.DataFrame(costs, index=chemistries)
    st.dataframe(df_costs, use_container_width=True)

    # --------- Section 5: Technology Impact ---------
    st.header("🧪 Technology Impact on LiPF₆")
    tech_df = pd.DataFrame({
        'Technology': ['Solid-State', 'Sodium-Ion', 'Semi-Solid', 'LiFSI Blends'],
        'Impact on LiPF₆': ['❌ Replace', '❌ Replace', '⬇ Reduce Use (5–10%)', '🔁 Partial Replacement'],
        'Timeframe': ['Long-term', 'Short to Mid-term', 'Mid-term', 'Already Growing']
    })
    st.dataframe(tech_df, use_container_width=True)

    # --------- Section 6: Strategic Insights ---------
    st.header("📈 Strategic Insights")
    st.markdown("""
    - **Europe & North America** are structurally under-supplied.
    - **China** dominates supply & pricing power.
    - **LiFSI** will gradually complement or replace LiPF₆ in high-end applications.
    - **Electrolyte costs** are significantly higher in the EU than in China (2x).
    - Technology shifts could disrupt demand after 2028.
    """)

    insight = st.text_area("📝 Add Your Own Strategic Notes")
    if insight:
        st.success("Note saved locally (not persistent yet).")
