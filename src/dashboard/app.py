import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add project root to path so modules resolve correctly
sys.path.append(str(Path(__file__).resolve().parents[2]))
from src.database.connection import get_connection

st.set_page_config(
    page_title="Job Market Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("Job Market Intelligence Dashboard")
st.markdown("Local-first analytics engine tracking software and data engineering roles.")

# Load data from DuckDB
@st.cache_data
def load_data():
    con = get_connection(read_only=True)
    df = con.execute("SELECT * FROM job_listings").fetchdf()
    con.close()
    return df

df_jobs = load_data()

if df_jobs.empty:
    st.warning("No job records found in the warehouse yet. Run your daily pipeline first!")
else:
    # Sidebar metrics
    st.sidebar.header("Filter & Metrics")
    total_jobs = len(df_jobs)
    st.sidebar.metric("Total Tracked Jobs", total_jobs)

    # Main Data Display
    st.subheader("Recent Job Listings")
    st.dataframe(df_jobs, use_container_width=True)

    # Skill breakdown analysis
    st.subheader("Top Mentioned Skills")
    if "skills" in df_jobs.columns:
        # Explode the list of skills arrays to count frequencies
        all_skills = [skill for skills_list in df_jobs['skills'].dropna() for skill in skills_list]
        if all_skills:
            skill_counts = pd.Series(all_skills).value_counts().reset_index()
            skill_counts.columns = ['Skill', 'Count']
            st.bar_chart(skill_counts.set_index('Skill'))
        else:
            st.info("No skill tags parsed yet.")