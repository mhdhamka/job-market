import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parents[2]))
from src.database.connection import get_connection
from src.processing.matcher import JobMatcher

# Page configuration
st.set_page_config(
    page_title="Job Market Intelligence",
    layout="wide"
)

# Custom Google Gemini-inspired styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 16px 20px;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    h1, h2, h3 {
        color: #1f1f1f;
        font-weight: 500;
    }
    .gemini-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 24px;
        border-radius: 16px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.title("Job Market Intelligence")
st.markdown("<p style='color: #5f6368; font-size: 1.1rem; margin-top: -10px;'>Local-first analytics tracking multi-source roles (MyFutureJobs, RemoteOK, LinkedIn).</p>", unsafe_allow_html=True)
st.markdown("---")

# Load data from DuckDB with safe fallback if created_at is missing
@st.cache_data
def load_data():
    con = get_connection(read_only=True)
    try:
        df = con.execute("SELECT * FROM job_listings ORDER BY created_at DESC").fetchdf()
    except Exception:
        df = con.execute("SELECT * FROM job_listings").fetchdf()
    con.close()
    return df

df_jobs = load_data()

# Dynamically find the source/platform column name in the database
source_col = next((col for col in ['source', 'platform', 'board'] if col in df_jobs.columns), None)

if df_jobs.empty:
    st.warning("No job records found in the warehouse yet. Run your daily pipeline first!")
else:
    # ---------------------------------------------------------
    # GRANULAR FILTERS & RESUME MATCHER (Sidebar Section)
    # ---------------------------------------------------------
    st.sidebar.header("Filter Controls")
    
    # 1. Source Filter (Robust fallback check)
    if source_col:
        available_sources = df_jobs[source_col].dropna().unique().tolist()
    else:
        available_sources = []
        
    selected_sources = st.sidebar.multiselect(
        "Source Platforms", 
        options=available_sources, 
        default=available_sources
    )
    
    # 2. Location Filter
    available_locations = df_jobs['location'].dropna().unique().tolist() if 'location' in df_jobs.columns else []
    selected_location = st.sidebar.selectbox("Location", options=["All"] + available_locations)

    # 3. Date Range Filter (if created_at is available)
    if 'created_at' in df_jobs.columns:
        df_jobs['created_at_dt'] = pd.to_datetime(df_jobs['created_at'], errors='coerce')
        min_date = df_jobs['created_at_dt'].min().date() if not df_jobs['created_at_dt'].isna().all() else pd.to_datetime("2026-01-01").date()
        max_date = df_jobs['created_at_dt'].max().date() if not df_jobs['created_at_dt'].isna().all() else pd.to_datetime("2026-12-31").date()
        
        date_range = st.sidebar.date_input("Posted Date Range", value=(min_date, max_date))
    else:
        date_range = None

    # 4. Resume Matcher Input
    st.sidebar.markdown("---")
    st.sidebar.subheader("Resume Matcher")
    user_skills_input = st.sidebar.text_input("Your Skills (comma separated)", placeholder="Python, SQL, Docker, FastAPI")
    user_skills_list = [s.strip() for s in user_skills_input.split(",") if s.strip()]

    # Apply Filters to DataFrame
    filtered_df = df_jobs.copy()
    
    if source_col and selected_sources:
        filtered_df = filtered_df[filtered_df[source_col].isin(selected_sources)]
        
    if selected_location != "All" and 'location' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['location'] == selected_location]
        
    if date_range and len(date_range) == 2 and 'created_at_dt' in filtered_df.columns:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df['created_at_dt'].dt.date >= start_date) & 
            (filtered_df['created_at_dt'].dt.date <= end_date)
        ]

    # Calculate Skill Match Scores if user inputs skills
    if user_skills_list and 'skills' in filtered_df.columns:
        match_percentages = []
        matching_details = []
        missing_details = []
        
        for job_skills in filtered_df['skills']:
            match_result = JobMatcher.calculate_match(user_skills_list, job_skills)
            match_percentages.append(match_result['match_percentage'])
            matching_details.append(", ".join(match_result['matching_skills']))
            missing_details.append(", ".join(match_result['missing_skills']))
            
        filtered_df['match_score (%)'] = match_percentages
        filtered_df['matching_skills'] = matching_details
        filtered_df['missing_skills'] = missing_details
        
        # Sort by match score descending
        filtered_df = filtered_df.sort_values(by='match_score (%)', ascending=False)

    # ---------------------------------------------------------
    # MAIN DASHBOARD CONTENT
    # ---------------------------------------------------------
    total_jobs = len(df_jobs)
    filtered_count = len(filtered_df)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Tracked Roles", filtered_count, delta=f"of {total_jobs} total")
    with col2:
        unique_platforms = filtered_df[source_col].nunique() if source_col and source_col in filtered_df.columns else 1
        st.metric("Active Platforms", unique_platforms)

    st.markdown("<br>", unsafe_allow_html=True)

    # Sleek Search Bar
    search_query = st.text_input("", placeholder="Search job titles or keywords (e.g., Python, Software Engineer)...", label_visibility="collapsed")
    
    if search_query:
        filtered_df = filtered_df[filtered_df['title'].str.contains(search_query, case=False, na=False)]

    st.markdown(f"<p style='color: #5f6368; font-size: 0.9rem;'>Displaying <b>{len(filtered_df)}</b> filtered records</p>", unsafe_allow_html=True)

    # Main Data Display Container
    st.subheader("Recent Job Listings & Match Analysis")
    
    base_cols = ['id', 'title']
    if source_col:
        base_cols.append(source_col)
    if 'location' in filtered_df.columns:
        base_cols.append('location')
        
    match_cols = ['match_score (%)', 'skills', 'missing_skills'] if user_skills_list else ['skills']
    tail_cols = ['salary_range', 'created_at']
    display_cols = [col for col in base_cols + match_cols + tail_cols if col in filtered_df.columns]
    
    st.dataframe(filtered_df[display_cols], use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # ADVANCED ANALYTICS & BENCHMARKING SECTION
    # ---------------------------------------------------------
    st.subheader("Market Analytics & Insights")
    
    ana_col1, ana_col2 = st.columns(2)

    with ana_col1:
        st.markdown("##### Platform Distribution")
        if source_col and source_col in filtered_df.columns and not filtered_df[source_col].isna().all():
            source_counts = filtered_df[source_col].value_counts().reset_index()
            source_counts.columns = ['Source', 'Count']
            st.bar_chart(source_counts.set_index('Source'), color="#1a73e8")
        else:
            st.info("No source breakdown available.")

    with ana_col2:
        st.markdown("##### Top Mentioned Skills")
        if "skills" in filtered_df.columns:
            all_skills = [skill for skills_list in filtered_df['skills'].dropna() for skill in skills_list]
            if all_skills:
                skill_counts = pd.Series(all_skills).value_counts().head(10).reset_index()
                skill_counts.columns = ['Skill', 'Count']
                st.bar_chart(skill_counts.set_index('Skill'), color="#34a853")
            else:
                st.info("No skill tags parsed in the current filter selection.")