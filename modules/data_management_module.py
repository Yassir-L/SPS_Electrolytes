import streamlit as st
import pandas as pd
import os
import time
from geopy.geocoders import Nominatim
from modules.data_loader import load_data, save_data

# Path to patent folder and favorite sheet
PATENT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Patents")
FAVORITES_SHEET = "Patents_Favorites"

def geocode_address(address):
    geolocator = Nominatim(user_agent="electrolyte_dashboard")
    try:
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
    except:
        pass
    return None, None

def show():
    st.header("🗂️ Database Manager")

    # --------------------- Section 1: Search Companies ---------------------
    df = load_data("Companies")
    st.subheader("🔍 Search the Database")
    columns = ['All'] + df.columns.tolist()
    selected_column = st.selectbox("Select column to search:", columns, key="search_select")
    search = st.text_input("Enter search term(s), separated by commas:", key="search_input")

    if search:
        search_terms = [term.strip().lower() for term in search.split(",") if term.strip()]
        if selected_column == 'All':
            filtered = df[df.apply(lambda row: all(
                any(term in str(cell).lower() for cell in row) for term in search_terms
            ), axis=1)]
        else:
            filtered = df[df[selected_column].astype(str).apply(
                lambda cell: all(term in cell.lower() for term in search_terms)
            )]
        st.write(filtered if not filtered.empty else "❌ No matches found!")

    # --------------------- Section 2: Edit/Add/Delete Companies ---------------------
    st.subheader("📝 Edit, Add, or Delete Companies")
    df = df.reset_index(drop=True)
    edited_df = st.data_editor(df, num_rows="dynamic", key="companies_editor")

    if st.button("💾 Save Changes"):
        common_cols = [col for col in df.columns if col in edited_df.columns]
        updated_df = edited_df[common_cols].copy()

        for idx, row in updated_df.iterrows():
            if pd.isna(row.get('lat')) or pd.isna(row.get('lon')):
                full_address = f"{row.get('Address', '')}, {row['Country']}"
                lat, lon = geocode_address(full_address)
                updated_df.at[idx, 'lat'] = lat
                updated_df.at[idx, 'lon'] = lon

        save_data(updated_df, "Companies")
        st.success("✅ Database updated successfully with geocoding!")
        st.balloons()
        time.sleep(1.5)
        st.rerun()

    # --------------------- Section 3: Patent Explorer ---------------------
    st.subheader("🔬 Patent Explorer")

    if not os.path.exists(PATENT_FOLDER):
        st.warning(f"⚠️ Patent folder not found at: {PATENT_FOLDER}")
        return

    file_options = [f for f in os.listdir(PATENT_FOLDER) if f.lower().endswith(".xlsx")]
    st.write("📁 Looking in:", PATENT_FOLDER)
    st.write("📄 Found files:", file_options)

    if not file_options:
        st.warning("⚠️ No Excel files found in the Patents folder.")
        return

    companies = [os.path.splitext(f)[0] for f in file_options]
    company_choice = st.selectbox("Select company file to search", ["All Companies"] + companies)

    def load_patents():
        dfs = []
        files_to_load = file_options if company_choice == "All Companies" else [company_choice + ".xlsx"]
        for fname in files_to_load:
            path = os.path.join(PATENT_FOLDER, fname)
            try:
                df_ = pd.read_excel(path)
                df_["Source Company"] = os.path.splitext(fname)[0]
                dfs.append(df_)
            except Exception as e:
                st.warning(f"❌ Error loading {fname}: {e}")
        if dfs:
            return pd.concat(dfs, ignore_index=True)
        else:
            return pd.DataFrame()

    if company_choice:
        patent_df = load_patents()

        if patent_df.empty:
            st.info("No data available from selected files.")
        else:
            st.markdown("**Select columns to search**")
            search_cols = st.multiselect("Columns:", patent_df.columns.tolist())
            query = st.text_input("Search patents (separate terms with commas):")

            if query and search_cols:
                terms = [t.strip().lower() for t in query.split(",") if t.strip()]

                def row_matches(row):
                    combined_text = " ".join([str(row[col]).lower() for col in search_cols if col in row])
                    return all(term in combined_text for term in terms)

                results = patent_df[patent_df.apply(row_matches, axis=1)].reset_index(drop=True)
                st.dataframe(results, use_container_width=True)

                st.markdown("### ⭐ Save Patents to Favorites")

                selected_indexes = st.multiselect(
                    "Select row indexes to save:",
                    options=list(results.index),
                    placeholder="Type or pick row numbers..."
                )

                if st.button("⭐ Add Selected Rows to Favorites"):
                    try:
                        selected_rows = results.loc[selected_indexes]
                        try:
                            favorites = load_data(FAVORITES_SHEET)
                            combined = pd.concat([favorites, selected_rows]).drop_duplicates()
                        except:
                            combined = selected_rows
                        save_data(combined, FAVORITES_SHEET)
                        st.success("✅ Selected rows added to favorites!")
                    except Exception as e:
                        st.error(f"❌ Error processing selection: {e}")

                if st.button("⭐ Add All Results to Favorites"):
                    try:
                        favorites = load_data(FAVORITES_SHEET)
                        combined = pd.concat([favorites, results]).drop_duplicates()
                    except:
                        combined = results
                    save_data(combined, FAVORITES_SHEET)
                    st.success("✅ All search results added to favorites!")

    # --------------------- View & Remove Favorites ---------------------
    st.subheader("📁 Favorite Patents")
    try:
        fav_df = load_data(FAVORITES_SHEET)
        edited_fav = st.data_editor(fav_df, num_rows="dynamic", key="fav_editor")
        if st.button("💾 Save Updated Favorites"):
            save_data(edited_fav, FAVORITES_SHEET)
            st.success("Favorites updated!")
    except:
        st.info("No favorites saved yet.")
