import streamlit as st
from modules.map_module import show as show_map
from modules.data_management_module import show as show_data_manager
from modules.references_module import show as show_references
from modules.analytics_module import show as show_analytics
from modules.market_intelligence_module import show as show_market_intel
from modules.ideas_module import show as show_ideas
from modules.ai_single_question import show as show_ai_simple
from modules.avicenne_module import show as show_avicenne


st.set_page_config(layout="wide")

st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio("Go to:", [
    "Ai Support System",
    "Avicenne Insights",
    "Map",
    "Database Manager",
    "References",
    "Self-Assessment",
    "Market Intelligence",
    "💡 Suggestions"
])

if page == "Ai Support System":
    show_ai_simple()
elif page == "Map":
    show_map()
elif page == "Avicenne Insights":
    show_avicenne()
elif page == "Database Manager":
    show_data_manager()
elif page == "References":
    show_references()
elif page == "Self-Assessment":
    show_analytics()
elif page == "Market Intelligence":
    show_market_intel()
elif page == "💡 Suggestions":
    show_ideas()
