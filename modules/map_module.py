import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
import numpy as np
from modules.data_loader import load_data


def show():
    st.title("🌍 Global LiPF₆ Producers Map")

    df = load_data("Companies")

    # FILTERS BLOCK
    st.subheader("🔍 Filters")
    col1, col2 = st.columns(2)
    with col1:
        column_choice = st.selectbox("Select column to filter", options=df.columns.tolist(), index=df.columns.get_loc("Project Scale"))
    with col2:
        unique_values = df[column_choice].dropna().unique().tolist()
        selected_value = st.selectbox(f"Filter by value in '{column_choice}'", ["All"] + unique_values)

    if selected_value != "All":
        df = df[df[column_choice] == selected_value]

    # MAP BLOCK
    seen_coords = set()

    def adjust_coords(lat, lon):
        offset = 0.02
        while (lat, lon) in seen_coords:
            lat += offset
            lon += offset
        seen_coords.add((lat, lon))
        return lat, lon

    m = folium.Map(location=[20, 0], zoom_start=2, tiles="cartodbpositron")
    color_counts = {"red": 0, "green": 0, "blue": 0}

    for _, row in df.iterrows():
        if pd.notnull(row['lat']) and pd.notnull(row['lon']):
            lat, lon = adjust_coords(row['lat'], row['lon'])
            project_type = str(row['Project Scale']).lower()
            if "industrial" in project_type:
                color = 'red'
                color_counts['red'] += 1
            elif "pilot" in project_type:
                color = 'green'
                color_counts['green'] += 1
            elif "upcoming" in project_type:
                color = 'blue'
                color_counts['blue'] += 1
            else:
                color = 'gray'

            html_popup = f"""
            <div style='width:200px; font-size: 14px;'>
                <h4>{row['Company']}</h4>
                <p><b>Country:</b> {row['Country']}<br>
                <b>Address:</b> {row.get('Address', 'N/A')}<br>
                <b>Current Capacity:</b> {row['Current Capacity (t/year)']} tons/year <br>
                <b>Expansion Plans:</b> {row['Expansion Plans (t/year)']} tons/year <br>
                <b>Key Clients:</b> {row['Key Clients']}<br>
                <b>Technology:</b> {row['Technology']}<br>
                <b>Scale:</b> {row['Project Scale']}</p>
            </div>
            """
            folium.Marker(
                location=[lat, lon],
                tooltip=row['Company'],
                icon=folium.Icon(color=color, icon="info-sign"),
                popup=folium.Popup(html_popup, max_width=250)
            ).add_to(m)

    st_folium(m, width=700, height=500)

    # LEGEND + KPIs BLOCK
    total_companies = color_counts['red'] + color_counts['green'] + color_counts['blue']
    total_capacity = df['Current Capacity (t/year)'].sum()

    st.markdown(f"""
    <div style="display: flex; align-items: flex-start; justify-content: space-between; background-color: #333; color: white; padding: 10px; border-radius: 5px;">
        <div>
            <b>Legend:</b><br>
            🔴 Industrial Scale<br>
            🟢 Pilot Project<br>
            🔵 Upcoming Facility
        </div>
        <div style="text-align: left;">
            <b>{total_companies} companies in total:</b><br>
            🔴 {color_counts['red']} Industrial<br>
            🟢 {color_counts['green']} Pilot<br>
            🔵 {color_counts['blue']} Upcoming<br>
            <b>🧮 Total Capacity:</b> {int(total_capacity):,} t/year
        </div>
    </div>
    """, unsafe_allow_html=True)

    # PARETO BLOCK WITH FILTER BUTTONS + DARK THEME
    st.subheader("🏆 Pareto of Top Producers")
    filter_colors = st.multiselect("Filter project types: ", ["red", "green", "blue"], default=["red", "green", "blue"])

    df['Volume'] = df['Current Capacity (t/year)']
    filtered_df = df[df['Project Scale'].str.lower().apply(lambda x: \
                        ('industrial' in x and 'red' in filter_colors) or \
                        ('pilot' in x and 'green' in filter_colors) or \
                        ('upcoming' in x and 'blue' in filter_colors))]

    top_df = filtered_df.sort_values(by='Volume', ascending=False).head(10)
    total_filtered = filtered_df['Volume'].sum()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=top_df['Company'],
        y=top_df['Volume'],
        marker_color='lightskyblue',
        text=(top_df['Volume'] / total_filtered * 100).apply(lambda x: f"{x:.2f}%"),
        textposition='outside'
    ))
    fig.update_layout(
        template="plotly_dark",
        yaxis_title="Production Capacity (t/year)",
        xaxis_title="Company",
        height=450,
        margin=dict(t=50)
    )
    st.plotly_chart(fig)

    # LORENZ CURVE BLOCK
    st.subheader("📈 Lorenz Curve")
    sorted_data = np.sort(filtered_df['Volume'].values)
    cum_data = np.cumsum(sorted_data)
    cum_data = np.insert(cum_data, 0, 0)
    cum_data = cum_data / cum_data[-1]
    x = np.linspace(0, 1, len(cum_data))
    fig_lorenz = go.Figure()
    fig_lorenz.add_trace(go.Scatter(x=x, y=cum_data, mode='lines', name='Lorenz Curve'))
    fig_lorenz.add_shape(type='line', x0=0, y0=0, x1=1, y1=1, line=dict(dash='dash', color='green'))
    fig_lorenz.update_layout(xaxis_title="Cumulative Companies", yaxis_title="Cumulative Capacity")
    st.plotly_chart(fig_lorenz)

    # PIE CHART BLOCK
    st.subheader("🍰 Global Capacity Distribution")
    labels = filtered_df['Company'].tolist()
    values = filtered_df['Volume'].tolist()
    fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig_pie.update_layout(title="Current Capacity Distribution by Company")
    st.plotly_chart(fig_pie)

    # FINAL DATAFRAME BLOCK
    st.subheader("📋 Full Company Dataset")
    st.dataframe(df)