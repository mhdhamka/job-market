import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from src.database.connection import get_connection

st.set_page_config(
    page_title="Job Market Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("Job Market Intelligence Dashboard")
st.markdown("Local-first analytics engine tracking multi-source roles (MyFutureJobs, RemoteOK, LinkedIn).")

# Load data from DuckDB with safe fallback if created_at is missing
@st.cache_data
def load_data():
    con = get_connection(read_only=True)
    try:
        df = con.execute("SELECT * FROM job_listings ORDER BY created_at DESC").fetchdf()
    except Exception:
        # Fallback if created_at column doesn't exist in the table yet
        df = con.execute("SELECT * FROM job_listings").fetchdf()
    con.close()
    return df

df_jobs = load_data()

if df_jobs.empty:
    st.warning("No job records found in the warehouse yet. Run your daily pipeline first!")
else:
    # Sidebar metrics & filtering tools
    st.sidebar.header("Filter & Metrics")
    total_jobs = len(df_jobs)
    st.sidebar.metric("Total Tracked Jobs", total_jobs)

    # Search filter to verify specific listings (e.g., LinkedIn or company names)
    search_query = st.sidebar.text_input("Search Job Titles", "")
    
    filtered_df = df_jobs
    if search_query:
        filtered_df = df_jobs[df_jobs['title'].str.contains(search_query, case=False, na=False)]

    st.sidebar.markdown(f"**Showing:** {len(filtered_df)} of {total_jobs} records")

    # Main Data Display
    st.subheader("Recent Job Listings")
    st.dataframe(filtered_df, use_container_width=True)

    # Skill breakdown analysis (aggregates skills across all sources including LinkedIn)
    st.subheader("Top Mentioned Skills Across Platforms")
    if "skills" in df_jobs.columns:
        all_skills = [skill for skills_list in df_jobs['skills'].dropna() for skill in skills_list]
        if all_skills:
            skill_counts = pd.Series(all_skills).value_counts().reset_index()
            skill_counts.columns = ['Skill', 'Count']
            st.bar_chart(skill_counts.set_index('Skill'))
        else:
            st.info("No skill tags parsed yet.")