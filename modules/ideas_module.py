import streamlit as st
import pandas as pd
import os
from datetime import datetime
from modules.data_loader import load_data, save_data

IDEAS_SHEET = "Dashboard_Ideas"


def load_ideas():
    try:
        return load_data(IDEAS_SHEET)
    except:
        return pd.DataFrame(columns=["Author", "Idea", "Response", "Timestamp"])


def save_ideas(df):
    save_data(df, IDEAS_SHEET)


def show():
    st.title("💡 Dashboard Improvement Ideas")

    ideas_df = load_ideas()

    st.subheader("📝 Submit a New Idea")
    with st.form("idea_form"):
        author = st.text_input("Your name")
        idea_text = st.text_area("What's your idea?")
        submitted = st.form_submit_button("Submit Idea")

        if submitted and author.strip() != "" and idea_text.strip() != "":
            new_idea = pd.DataFrame([{"Author": author, "Idea": idea_text, "Response": "", "Timestamp": datetime.now()}])
            ideas_df = pd.concat([ideas_df, new_idea], ignore_index=True)
            save_ideas(ideas_df)
            st.success("✅ Idea submitted successfully!")
            st.rerun()

    st.markdown("---")
    st.subheader("💬 All Suggestions")

    for idx, row in ideas_df.iterrows():
        with st.container():
            st.markdown(f"**💡 Idea #{idx+1}**")
            st.markdown(f"""
                <div style='padding:10px; background:#2c2f33; color:#ffffff; border-radius:10px'>
                    <i style='color:#bbb; font-size:13px;'>by {row['Author']}</i><br>
                    <b>{row['Idea']}</b><br>
                    <small><i>Submitted on {row['Timestamp'].strftime('%Y-%m-%d %H:%M')}</i></small>
                </div>
            """, unsafe_allow_html=True)

            # Edit idea
            with st.expander("✏️ Edit Idea"):
                edited_idea = st.text_area("Edit your idea:", value=row['Idea'], key=f"edit_{idx}")
                if st.button("Save Edit", key=f"save_{idx}"):
                    ideas_df.at[idx, "Idea"] = edited_idea
                    save_ideas(ideas_df)
                    st.success("✏️ Idea updated!")
                    st.rerun()

            # Response to idea
            with st.expander("💬 Respond to this idea"):
                current_response = row["Response"] if pd.notna(row["Response"]) else ""
                response = st.text_area("Your response:", value=current_response, key=f"response_{idx}")
                if st.button("Save Response", key=f"response_btn_{idx}"):
                    ideas_df.at[idx, "Response"] = response
                    save_ideas(ideas_df)
                    st.success("💬 Response saved!")
                    st.rerun()

            # Display saved response if exists
            if pd.notna(row["Response"]) and row["Response"].strip() != "":
                st.markdown(f"""
                    <div style='margin-top:5px; padding:10px; background:#dce7f8; color:#000; border-left: 4px solid #1f77b4; border-radius:5px'>
                        <b>🗨️ Response:</b><br>{row['Response']}
                    </div>
                """, unsafe_allow_html=True)

            # Delete button
            if st.button("🗑️ Delete this idea", key=f"delete_{idx}"):
                ideas_df = ideas_df.drop(index=idx).reset_index(drop=True)
                save_ideas(ideas_df)
                st.success("🗑️ Idea deleted!")
                st.rerun()

            st.markdown("---")
