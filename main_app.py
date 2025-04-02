import streamlit as st
from modules.map_module import show as show_map
from modules.data_management_module import show as show_data_manager
from modules.references_module import show as show_references
from modules.analytics_module import show as show_analytics
from modules.market_intelligence_module import show as show_market_intel
from modules.ideas_module import show as show_ideas

st.set_page_config(layout="wide")

st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio("Go to:", [
    "Map",
    "Database Manager",
    "References",
    "Analytics",
    "Market Intelligence",
    "💡 Suggestions"
])

if page == "Map":
    show_map()
elif page == "Database Manager":
    show_data_manager()
elif page == "References":
    show_references()
elif page == "Analytics":
    show_analytics()
elif page == "Market Intelligence":
    show_market_intel()
elif page == "💡 Suggestions":
    show_ideas()