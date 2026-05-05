import streamlit as st
import pandas as pd
import altair as alt
from sqlalchemy import text
from src.utils.db_utils import get_engine

# Styling and Configuration
def apply_custom_css():
    """Injects custom CSS to handle zoom, hide popover arrows, and center metrics."""
    st.set_page_config(page_title="Wildlife Health Explorer", layout="wide", page_icon="🐾")
    st.markdown("""
        <style>
            html, body, [class*="css"]  { font-size: 1.15rem !important; }
            div[data-testid="stPopover"] > button svg { display: none !important; }
            div[data-testid="stDateInput"] { display: flex; justify-content: flex-end; }
            
            [data-testid="stMetric"] {
                text-align: center;
                padding-top: 5px !important;
                padding-bottom: 5px !important;
            }
            [data-testid="stMetricLabel"] {
                font-size: 1.3rem !important; 
                font-weight: 600 !important;
                justify-content: center !important;
                margin-bottom: 5px;
            }
            [data-testid="stMetricValue"] { font-size: 2.8rem !important; }
        </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    engine = get_engine()
    query = text("""
        SELECT 
            a.species_name, e.phenological_season_name AS season, 
            f.health_status_score, f.body_temperature, f.weight,
            l.indigenous_land_name, l.latitude, l.longitude,
            ag.agency_type, d.full_date
        FROM fact_observations f
        JOIN dim_environment e ON f.env_id = e.env_id
        JOIN dim_animal a ON f.animal_id = a.animal_id
        JOIN dim_location l ON f.location_id = l.location_id
        JOIN dim_agency ag ON f.agency_id = ag.agency_id
        JOIN dim_date d ON f.date_id = d.date_id
        WHERE e.state = 'NSW';
    """)
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    
    df['full_date'] = pd.to_datetime(df['full_date'])
    return df

def filter_dataset(df, filters):
    filtered = df[
        (df['species_name'].isin(filters['species'])) &
        (df['agency_type'].isin(filters['agencies'])) &
        (df['season'].isin(filters['seasons'])) &
        (df['indigenous_land_name'].isin(filters['lands'])) &
        (df['body_temperature'] >= filters['temp_range'][0]) & 
        (df['body_temperature'] <= filters['temp_range'][1])
    ]

    if len(filters['date_range']) == 2:
        filtered = filtered[
            (filtered['full_date'].dt.date >= filters['date_range'][0]) & 
            (filtered['full_date'].dt.date <= filters['date_range'][1])
        ]

    if filters['use_spatial']:
        filtered = filtered[
            (filtered['latitude'] >= filters['lat_range'][0]) & (filtered['latitude'] <= filters['lat_range'][1]) &
            (filtered['longitude'] >= filters['lon_range'][0]) & (filtered['longitude'] <= filters['lon_range'][1])
        ]
    return filtered

#* UI COMPONENTS
def render_top_bar(df):
    filters = {}
    top_left, _, top_right = st.columns([2, 7, 3])

    with top_left:
        with st.popover("User data rights"):
            lands = df['indigenous_land_name'].unique()
            filters['lands'] = [land for land in lands if st.checkbox(land, value=True)]

    with top_right:
        min_date, max_date = df['full_date'].min().date(), df['full_date'].max().date()
        filters['date_range'] = st.date_input("Date Range", (min_date, max_date), label_visibility="collapsed")
        
    return filters

def render_sidebar(df):
    filters = {}
    st.sidebar.header("Filter Analytics")

    with st.sidebar.popover("Animal Species"):
        species_list = df['species_name'].unique()
        filters['species'] = st.multiselect("Search Species", species_list, default=species_list, label_visibility="collapsed")

    with st.sidebar.popover("Agency Type"):
        agency_list = df['agency_type'].unique()
        filters['agencies'] = st.multiselect("Search Agencies", agency_list, default=agency_list, label_visibility="collapsed")

    with st.sidebar.popover("Environment (Season)"):
        season_list = df['season'].unique()
        filters['seasons'] = st.multiselect("Search Seasons", season_list, default=season_list, label_visibility="collapsed")

    st.sidebar.subheader("Observations")
    min_t, max_t = float(df['body_temperature'].min()), float(df['body_temperature'].max())
    filters['temp_range'] = st.sidebar.slider("Body Temp Range (°C)", min_t, max_t, (min_t, max_t))

    filters['use_spatial'] = st.sidebar.checkbox("Enable Spatial Coordinates")
    filters['lat_range'], filters['lon_range'] = None, None
    
    if filters['use_spatial']:
        min_lat, max_lat = float(df['latitude'].min()), float(df['latitude'].max())
        filters['lat_range'] = st.sidebar.slider("Latitude", min_lat, max_lat, (min_lat, max_lat))
        min_lon, max_lon = float(df['longitude'].min()), float(df['longitude'].max())
        filters['lon_range'] = st.sidebar.slider("Longitude", min_lon, max_lon, (min_lon, max_lon))
        
    return filters

def render_main_chart(df):
    st.write("") 
    with st.container(border=True):
        drop_col, _ = st.columns([2, 10])
        with drop_col:
            metric_choice = st.selectbox("Metric", ["Health Score", "Body Temp", "Weight"], label_visibility="collapsed")
            st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)
        
        if df.empty:
            st.warning("No data matches current filters.")
            return

        y_val = {"Health Score": "health_status_score", "Body Temp": "body_temperature", "Weight": "weight"}[metric_choice]
        
        chart = alt.Chart(df).mark_bar(color="#4B8BBE").encode(
            x=alt.X('season:N', axis=alt.Axis(labelAngle=-45, title=None, labelFontSize=14)),
            y=alt.Y(f'mean({y_val}):Q', title=None, axis=alt.Axis(labelFontSize=14)),
            tooltip=[alt.Tooltip('season:N', title='Season'), alt.Tooltip(f'mean({y_val}):Q', title=f'Avg {metric_choice}', format='.2f')]
        ).properties(height=450, width='container')
        
        st.altair_chart(chart, use_container_width=True)

def render_metrics_and_map(df):
    bottom_left, bottom_right = st.columns([1, 1])
    CUBE_HEIGHT = 210

    with bottom_left:
        m_row1_col1, m_row1_col2 = st.columns(2)
        avg_health = df['health_status_score'].mean() if not df.empty else 0
        avg_temp = df['body_temperature'].mean() if not df.empty else 0
        
        with m_row1_col1:
            with st.container(border=True, height=CUBE_HEIGHT):
                st.metric("Total Observations", len(df))
        with m_row1_col2:
            with st.container(border=True, height=CUBE_HEIGHT):
                st.metric("Avg Health Score", f"{avg_health:.2f} / 5")

        m_row2_col1, m_row2_col2 = st.columns(2)
        with m_row2_col1:
            with st.container(border=True, height=CUBE_HEIGHT):
                st.metric("Avg Body Temp", f"{avg_temp:.1f} °C")
        with m_row2_col2:
            with st.container(border=True, height=CUBE_HEIGHT):
                st.metric("Active Agencies", df['agency_type'].nunique())

    with bottom_right:
        with st.container(border=True, height=435):
            if not df.empty:
                pie_data = df['indigenous_land_name'].value_counts().reset_index()
                pie_data.columns = ['Land', 'Count']
                
                pie_chart = alt.Chart(pie_data).mark_arc().encode(
                    theta=alt.Theta(field="Count", type="quantitative"),
                    color=alt.Color(field="Land", type="nominal", legend=alt.Legend(title=None, orient="right", labelFontSize=14)),
                    tooltip=['Land', 'Count']
                ).properties(
                    title=alt.TitleParams(text="Data Sovereignty Map", anchor='middle', dx=-240, fontSize=20),
                    height=380
                )
                st.altair_chart(pie_chart, use_container_width=True)

def render_raw_data(df):
    st.subheader("Raw Interoperable Data")
    if not df.empty:
        display_df = df.drop(columns=['latitude', 'longitude'])
        st.dataframe(display_df.head(50), use_container_width=True)

def main():
    apply_custom_css()
    
    try:
        raw_df = load_data()
    except Exception as e:
        st.error(f"Database Connection Failed. Error: {e}")
        st.stop()

    top_filters = render_top_bar(raw_df)
    side_filters = render_sidebar(raw_df)
    all_filters = {**top_filters, **side_filters}
    
    filtered_df = filter_dataset(raw_df, all_filters)

    render_main_chart(filtered_df)
    render_metrics_and_map(filtered_df)
    render_raw_data(filtered_df)

if __name__ == "__main__":
    main()