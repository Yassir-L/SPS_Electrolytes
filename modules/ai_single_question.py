import streamlit as st
import fitz  # PyMuPDF
import pandas as pd
from openai import OpenAI
from modules.data_loader import load_data
import json
import os

# Initialize OpenAI
client = OpenAI(api_key=api_key)
SAVE_FILE = "saved_responses.json"

# Helper to persist saved responses across sessions
def load_saved_responses():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return []

def save_responses(responses):
    with open(SAVE_FILE, "w") as f:
        json.dump(responses, f)

def show():
    st.title("🤖 Our AI Expert")

    try:
        df_main = load_data("Companies")
        document_text = df_main.to_markdown()
        with st.expander("📊 Our Data (Click to show/hide)"):
            st.dataframe(df_main)
    except Exception as e:
        st.error(f"Could not load internal data: {e}")
        return

    if "history" not in st.session_state:
        st.session_state.history = []
    if "clear_input" not in st.session_state:
        st.session_state.clear_input = False
    if "saved_responses" not in st.session_state:
        st.session_state.saved_responses = load_saved_responses()

    uploaded_context_file = st.file_uploader("📎 Optional: Upload a document to include in the question", type=["pdf", "txt", "xlsx"])
    uploaded_text = ""
    if uploaded_context_file:
        if uploaded_context_file.name.endswith(".pdf"):
            doc = fitz.open(stream=uploaded_context_file.read(), filetype="pdf")
            uploaded_text = "\n".join(page.get_text() for page in doc)
        elif uploaded_context_file.name.endswith(".txt"):
            uploaded_text = uploaded_context_file.read().decode("utf-8")
        elif uploaded_context_file.name.endswith(".xlsx"):
            df_extra = pd.read_excel(uploaded_context_file)
            uploaded_text = df_extra.to_markdown()

    if st.button("📊 Analyse My Work with AI"):
        with st.spinner("GPT-4 is analysing your data..."):
            avicenne_summary = """
📘 Avicenne Data (High-level market view):
- Forecasted LiPF₆ demand in 2030:
  - Europe: 95 kta
  - North America: 85 kta
  - Asia (excl. CN, ROK, JP): 15 kta
  - Total demand (2030): ~685 kta
- 2024 global supply: ~335,000 tons vs. ~60,000 tons in 2020
- Major producers in 2024:
  - Tinci: 26%, DFD: 21%, Xintai: 18%, Jiangsu Jiujiu: 9%
- Price evolution:
  - $60+/kg (2021 peak) → $8.5/kg in China (Q4 2024)
- International expansion limited: only DFD (to SK) and Tinci (Morocco & US).
"""
            our_data_table = df_main.to_markdown(index=False)
            prompt = f"""
You are a market expert in LiPF₆ production and demand.
Please analyze and compare the following two datasets:
{avicenne_summary}
📗 Our Data (Company-level dataset):
{our_data_table}

Please deliver a brief, expert-level comparison that includes:
1. 🧠 Key high-level insights from Avicenne (demand trends, oversupply, regional gaps).
2. 🏭 Concrete insights from our dataset (who’s active, who’s expanding, gaps).
3. ⚖️ Critiques and strengths of our internal data — is it exhaustive, detailed, biased, lacking?
"""
            messages = [
                {"role": "system", "content": "You are an expert in LiPF6 market analysis."},
                {"role": "user", "content": prompt}
            ]
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=messages,
                    temperature=0.3
                )
                reply = response.choices[0].message.content
                st.session_state.history.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Error from GPT: {e}")

    if st.session_state.saved_responses:
        st.subheader("💾 Saved Insights")
        for i, saved in enumerate(st.session_state.saved_responses):
            col1, col2 = st.columns([8, 1])
            with col1:
                st.markdown(f"**Insight {i+1}:**\n{saved}")
            with col2:
                if st.button("x", key=f"delete_saved_{i}"):
                    st.session_state.saved_responses.pop(i)
                    save_responses(st.session_state.saved_responses)
                    st.rerun()

    if st.session_state.history:
        st.subheader("🤖 AI Responses")
        for i, msg in enumerate(st.session_state.history):
            if msg["role"] == "assistant":
                col1, col2 = st.columns([8, 1])
                with col1:
                    st.markdown(msg["content"])
                with col2:
                    if st.button("✅", key=f"keep_{i}"):
                        st.session_state.saved_responses.append(msg["content"])
                        save_responses(st.session_state.saved_responses)
                    if st.button("❌", key=f"remove_{i}"):
                        st.session_state.history.pop(i)
                        st.rerun()
            elif msg["role"] == "user":
                st.markdown(f"**You:** {msg['content']}")

    # Always-visible input section
    st.markdown("""
        <style>
        div[data-testid="stBottomContainer"] {position: fixed; bottom: 0; left: 0; width: 100%; background-color: #111; padding: 1rem; z-index: 1000;}
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.text_input("💬 Ask our AI expert a question:", key="chat_input", placeholder="Type your question here and press Enter...")

    if st.session_state.chat_input:
        user_input = st.session_state.chat_input
        st.session_state.chat_input = ""
        st.session_state.history.append({"role": "user", "content": user_input})
        with st.spinner("GPT-4 is responding..."):
            context = f"Avicenne Data:\n{avicenne_summary}\n\nOur Data:\n{document_text[:3000]}\n\nUser uploaded:\n{uploaded_text}"
            messages = [
                {"role": "system", "content": "You are an expert in LiPF6 market analysis."},
                {"role": "user", "content": context}
            ] + st.session_state.history
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=messages,
                    temperature=0.3
                )
                reply = response.choices[0].message.content
                st.session_state.history.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Error: {e}")
            st.rerun()
