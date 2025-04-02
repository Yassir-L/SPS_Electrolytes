import streamlit as st
import pandas as pd
from modules.data_loader import load_data
import os

def show():
    st.header("📚 References Library")
    ref_df = load_data("References")

    columns = ['All'] + ref_df.columns.tolist()
    selected_column = st.selectbox("Filter by column:", columns)
    search = st.text_input("Enter search keyword:")

    if search:
        if selected_column == 'All':
            filtered = ref_df[ref_df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]
        else:
            filtered = ref_df[ref_df[selected_column].astype(str).str.contains(search, case=False)]
        st.write(filtered if not filtered.empty else "❌ No matches found!")

    st.subheader("📑 Edit or Add References")
    edited_df = st.data_editor(ref_df, num_rows="dynamic")

    if st.button("💾 Save References"):
        edited_df.to_csv(ref_path, index=False)
        st.success("✅ References updated!")
        time.sleep(1.5)
        st.rerun()

# CSV backend, interactive map filters, clickable reference button, color-coded markers
