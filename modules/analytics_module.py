import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from modules.data_loader import load_data

PATENT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Patents")


def get_internal_kpis(companies_df):
    return {
        "Total Companies": len(companies_df),
        "Total Current Capacity (t/year)": companies_df["Current Capacity (t/year)"].sum(),
        "Average Capacity per Company": companies_df["Current Capacity (t/year)"].mean(),
        "Industrial Scale Projects": (companies_df["Project Scale"].str.contains("industrial", case=False)).sum()
    }


def show():
    st.header("📌 Self-Assessment")

    companies_df = load_data("Companies")
    internal_capacity = companies_df["Current Capacity (t/year)"].sum()
    avicenne_capacity = 302_000  # Updated based on your image

    attainment = (internal_capacity / avicenne_capacity) * 100 if avicenne_capacity > 0 else 0

    st.subheader("Current Capacity vs. Avicenne (2024 Benchmark)")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🟢 Internal – Total Current Capacity", f"{internal_capacity:,.0f} t/year")
    with col2:
        st.metric("📘 Avicenne – Benchmark (2024)", f"{avicenne_capacity:,.0f} t/year")
    with col3:
        st.metric("🎯 Attainment", f"{attainment:.1f}%")

