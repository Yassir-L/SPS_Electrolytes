import streamlit as st
from modules.map_module import show as show_map
from modules.data_management_module import show as show_data_manager
from modules.references_module import show as show_references
from modules.analytics_module import show as show_analytics
from modules.market_intelligence_module import show as show_market_intel
from modules.ideas_module import show as show_ideas
from modules.ai_single_question import show as show_ai_simple
from modules.avicenne_module import show as show_avicenne
from modules.home_module import show as show_home
from modules.LiFSI_data import show as show_raw_materials


st.set_page_config(layout="wide")

st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio("Go to:", [
    "🏠 Accueil", 
    "Map",
    "LiFSI",
    "Avis d'experts", 
    "Self-Assessment",
    "Ai Support System",
    "Database Manager",
    "References",
    "💡 Suggestions"
])

# Redirection vers les bons modules
if page == "🏠 Accueil":
    show_home()
elif page == "Map":
    show_map()
elif page == "LiFSI":
    show_raw_materials()
elif page == "Ai Support System":
    show_ai_simple()
elif page == "Avis d'experts":  # nouveau nom utilisé ici aussi
    show_avicenne()
elif page == "Self-Assessment":
    show_analytics()
elif page == "Database Manager":
    show_data_manager()
elif page == "References":
    show_references()
elif page == "💡 Suggestions":
    show_ideas()
