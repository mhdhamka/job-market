import sys
from pathlib import Path
import duckdb
import pandas as pd
import streamlit as st

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parents[2]))
from src.database.connection import get_connection
from src.processing.matcher import JobMatcher

st.set_page_config(
    page_title="Kerja Scraper — Job Intelligence & Tracker",
    layout="wide",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        background-color: #F4F2EE;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        color: #191919;
    }

    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E5E3DD;
    }
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span {
        color: #191919 !important;
    }

    /* Keep multiselect tags crisp */
    [data-testid="stSidebar"] [data-baseweb="tag"] {
        background-color: #EBF3FC !important;
        border: 1px solid #B8D4F2 !important;
    }
    [data-testid="stSidebar"] [data-baseweb="tag"] span {
        color: #0A66C2 !important;
        font-weight: 600;
    }

    /* Top Brand Banner (White card + Blue font) */
    .top-banner {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E3DD !important;
        border-left: 5px solid #0A66C2 !important;
        padding: 22px 28px !important;
        border-radius: 14px !important;
        margin-bottom: 18px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
    }
    .top-banner h1 {
        color: #0A66C2 !important;
        font-size: 1.7rem !important;
        font-weight: 700 !important;
        margin: 0 0 6px 0 !important;
        letter-spacing: -0.02em !important;
        line-height: 1.2 !important;
    }
    .top-banner p {
        color: #0A66C2 !important;
        font-size: 0.96rem !important;
        font-weight: 500 !important;
        margin: 0 !important;
        line-height: 1.45 !important;
    }

    [data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E3DD !important;
        padding: 16px 20px !important;
        border-radius: 12px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
    }
    [data-testid="stMetric"] * {
        color: #191919 !important;
    }
    [data-testid="stMetricLabel"] * {
        color: #4A4F55 !important;
        font-weight: 600 !important;
        font-size: 0.82rem !important;
    }
    [data-testid="stMetricValue"] * {
        color: #0A66C2 !important;
        font-weight: 700 !important;
    }

    .surface-card {
        background-color: #FFFFFF;
        border: 1px solid #E5E3DD;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 12px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
        transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }
    .surface-card:hover {
        border-color: #0A66C2;
        box-shadow: 0 4px 12px rgba(10, 102, 194, 0.08);
    }
    .job-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #0A66C2;
        margin: 0 0 8px 0;
    }
    .job-meta-row {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        align-items: center;
        margin-bottom: 10px;
        font-size: 0.84rem;
        color: #374151;
    }
    .badge-platform {
        background-color: #EBF3FC;
        color: #0A66C2;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 0.76rem;
        border: 1px solid #C7DEF7;
    }
    .badge-salary {
        background-color: #EAF7EE;
        color: #137333;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 0.76rem;
        border: 1px solid #CBEAD5;
    }
    .badge-match {
        background-color: #FFF6E5;
        color: #9A5B00;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 0.76rem;
        border: 1px solid #F7DFAD;
    }
    .skill-pill {
        display: inline-block;
        background-color: #F3F4F6;
        color: #1F2937;
        border: 1px solid #E5E7EB;
        padding: 2px 9px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 500;
        margin: 2px 4px 2px 0;
    }
    .skill-pill-hit {
        background-color: #EBF3FC;
        color: #0A66C2;
        border-color: #B8D4F2;
        font-weight: 600;
    }

    /* Navigation Tabs */
    [data-testid="stTabs"] [data-baseweb="tab-list"],
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
        background-color: #FFFFFF !important;
        padding: 6px 10px !important;
        border-radius: 12px !important;
        border: 1px solid #E5E3DD !important;
    }
    [data-testid="stTabs"] button[role="tab"],
    .stTabs button[role="tab"] {
        border-radius: 8px !important;
        padding: 8px 18px !important;
        font-weight: 600 !important;
        background-color: #FFFFFF !important;
        color: #0A66C2 !important;
        border: 1px solid transparent !important;
    }
    [data-testid="stTabs"] button[role="tab"] *,
    .stTabs button[role="tab"] * {
        color: #0A66C2 !important;
        opacity: 1 !important;
    }
    [data-testid="stTabs"] button[role="tab"]:hover,
    .stTabs button[role="tab"]:hover {
        background-color: #EBF3FC !important;
        color: #0A66C2 !important;
    }
    [data-testid="stTabs"] button[role="tab"][aria-selected="true"],
    .stTabs button[role="tab"][aria-selected="true"] {
        background-color: #0A66C2 !important;
        color: #FFFFFF !important;
        border-color: #0A66C2 !important;
    }
    [data-testid="stTabs"] button[role="tab"][aria-selected="true"] *,
    .stTabs button[role="tab"][aria-selected="true"] * {
        color: #FFFFFF !important;
        opacity: 1 !important;
    }
    [data-testid="stTabs"] [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: #0A66C2 !important;
        height: 3px !important;
    }
    [data-testid="stTabs"] [data-baseweb="tab-border"],
    .stTabs [data-baseweb="tab-border"] {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "<div class='top-banner'><h1>Kerja Scraper</h1><p>Malaysian &amp; remote job intelligence feed, skill-match insights, and personal application tracker</p></div>",
    unsafe_allow_html=True,
)

tab1, tab2 = st.tabs(["Market Intelligence", "My Applications Pipeline"])


def render_skill_pills(skills_val, matched_set=None):
    if skills_val is None:
        return "<span style='color:#6B7280;font-size:0.78rem;'>No skills extracted</span>"
    if isinstance(skills_val, str):
        skills_iter = [s.strip() for s in skills_val.split(",") if s.strip()]
    else:
        try:
            skills_iter = list(skills_val)
        except TypeError:
            skills_iter = []

    if not skills_iter:
        return "<span style='color:#6B7280;font-size:0.78rem;'>No skills extracted</span>"

    matched_upper = {str(m).upper() for m in (matched_set or [])}
    pills = []
    for sk in skills_iter[:8]:
        hit_cls = " skill-pill-hit" if str(sk).upper() in matched_upper else ""
        pills.append(f"<span class='skill-pill{hit_cls}'>{sk}</span>")
    if len(skills_iter) > 8:
        pills.append(f"<span class='skill-pill'>+{len(skills_iter) - 8} more</span>")
    return "".join(pills)


# =========================================================
# TAB 1: MARKET INTELLIGENCE
# =========================================================
with tab1:
    @st.cache_data
    def load_data():
        con = get_connection(read_only=False)
        try:
            table_exists = (
                con.execute(
                    "SELECT count(*) FROM information_schema.tables WHERE table_name = 'job_listings'"
                ).fetchone()[0]
                > 0
            )
            if not table_exists:
                df = pd.DataFrame()
            else:
                df = con.execute("SELECT * FROM job_listings ORDER BY created_at DESC").fetchdf()
        except Exception:
            df = pd.DataFrame()
        finally:
            con.close()
        return df

    df_jobs = load_data()
    source_col = next((col for col in ["source", "platform", "board"] if col in df_jobs.columns), None)

    if df_jobs.empty:
        st.warning("No job records found in the warehouse yet. Run your daily pipeline first!")
    else:
        st.sidebar.markdown("### Search & Filter")

        if source_col:
            available_sources = df_jobs[source_col].dropna().unique().tolist()
        else:
            available_sources = []

        selected_sources = st.sidebar.multiselect(
            "Job Portals",
            options=available_sources,
            default=available_sources,
        )

        available_locations = (
            df_jobs["location"].dropna().unique().tolist() if "location" in df_jobs.columns else []
        )
        selected_location = st.sidebar.selectbox("Location", options=["All"] + available_locations)

        if "created_at" in df_jobs.columns:
            df_jobs["created_at_dt"] = pd.to_datetime(df_jobs["created_at"], errors="coerce")
            min_date = (
                df_jobs["created_at_dt"].min().date()
                if not df_jobs["created_at_dt"].isna().all()
                else pd.to_datetime("2026-01-01").date()
            )
            max_date = (
                df_jobs["created_at_dt"].max().date()
                if not df_jobs["created_at_dt"].isna().all()
                else pd.to_datetime("2026-12-31").date()
            )
            date_range = st.sidebar.date_input("Posted Date Range", value=(min_date, max_date))
        else:
            date_range = None

        st.sidebar.markdown("---")
        st.sidebar.markdown("### Resume Skill Matcher")
        user_skills_input = st.sidebar.text_input(
            "Your Skills (comma separated)",
            placeholder="Python, SQL, Docker, FastAPI",
        )
        user_skills_list = (
            [s.strip() for s in user_skills_input.split(",") if s.strip()] if user_skills_input else []
        )

        filtered_df = df_jobs.copy()

        if source_col and selected_sources:
            filtered_df = filtered_df[filtered_df[source_col].isin(selected_sources)]

        if selected_location != "All" and "location" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["location"] == selected_location]

        if date_range and len(date_range) == 2 and "created_at_dt" in filtered_df.columns:
            start_date, end_date = date_range
            filtered_df = filtered_df[
                (filtered_df["created_at_dt"].dt.date >= start_date)
                & (filtered_df["created_at_dt"].dt.date <= end_date)
            ]

        matched_lookup = {}
        if user_skills_list and "skills" in filtered_df.columns:
            match_percentages = []
            matching_details = []
            missing_details = []

            for idx, job_skills in enumerate(filtered_df["skills"]):
                clean_user_skills = list(user_skills_list)
                clean_job_skills = list(job_skills) if job_skills is not None else []

                match_result = JobMatcher.calculate_match(clean_user_skills, clean_job_skills)
                match_percentages.append(match_result["match_percentage"])
                matching_details.append(", ".join(match_result["matching_skills"]))
                missing_details.append(", ".join(match_result["missing_skills"]))
                matched_lookup[idx] = match_result["matching_skills"]

            filtered_df["match_score (%)"] = match_percentages
            filtered_df["matching_skills"] = matching_details
            filtered_df["missing_skills"] = missing_details
            filtered_df = filtered_df.sort_values(by="match_score (%)", ascending=False)

        search_query = st.text_input(
            "Search roles or keywords",
            placeholder="Search job titles or keywords (e.g., Data Engineer, Python, Kuching)...",
            label_visibility="collapsed",
        )
        if search_query:
            filtered_df = filtered_df[
                filtered_df["title"].str.contains(search_query, case=False, na=False)
            ]

        total_jobs = len(df_jobs)
        filtered_count = len(filtered_df)
        unique_platforms = (
            filtered_df[source_col].nunique() if source_col and source_col in filtered_df.columns else 1
        )
        avg_match = (
            f"{filtered_df['match_score (%)'].mean():.1f}%"
            if "match_score (%)" in filtered_df.columns and not filtered_df.empty
            else "—"
        )

        m1, m2, m3 = st.columns(3)
        m1.metric("Matching Roles", filtered_count, delta=f"of {total_jobs} indexed")
        m2.metric("Active Portals", unique_platforms)
        m3.metric("Avg Skill Match", avg_match)

        st.markdown("<br>", unsafe_allow_html=True)

        feed_col, table_col = st.columns([1.15, 1.35], gap="large")

        with feed_col:
            st.markdown("### Job Feed Preview")
            if filtered_df.empty:
                st.info("No roles match your current search or filter criteria.")
            else:
                for idx, (_, row) in enumerate(filtered_df.head(8).iterrows()):
                    title = str(row.get("title", "Untitled Role"))
                    platform = str(row.get(source_col, "Job Board")) if source_col else "Job Board"
                    location = (
                        str(row.get("location"))
                        if "location" in row and pd.notna(row.get("location"))
                        else "Malaysia / Remote"
                    )
                    salary = (
                        str(row.get("salary_range"))
                        if "salary_range" in row and pd.notna(row.get("salary_range"))
                        else "Salary not listed"
                    )
                    match_badge = (
                        f"<span class='badge-match'>{row['match_score (%)']}% Match</span>"
                        if "match_score (%)" in row and pd.notna(row.get("match_score (%)"))
                        else ""
                    )
                    pills_html = render_skill_pills(row.get("skills"), matched_lookup.get(idx))

                    card_html = (
                        f"<div class='surface-card'>"
                        f"<div class='job-title'>{title}</div>"
                        f"<div class='job-meta-row'>"
                        f"<span class='badge-platform'>{platform}</span>"
                        f"<span>{location}</span>"
                        f"<span class='badge-salary'>{salary}</span>"
                        f"{match_badge}"
                        f"</div>"
                        f"<div>{pills_html}</div>"
                        f"</div>"
                    )
                    st.markdown(card_html, unsafe_allow_html=True)

        with table_col:
            st.markdown("### All Listings & Match Breakdown")
            base_cols = ["id", "title"]
            if source_col:
                base_cols.append(source_col)
            if "location" in filtered_df.columns:
                base_cols.append("location")

            match_cols = ["match_score (%)", "skills", "missing_skills"] if user_skills_list else ["skills"]
            tail_cols = ["salary_range", "created_at"]
            display_cols = [col for col in base_cols + match_cols + tail_cols if col in filtered_df.columns]

            st.dataframe(filtered_df[display_cols], use_container_width=True, hide_index=True, height=540)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("### Market Analytics & Insights")
        ana_col1, ana_col2 = st.columns(2, gap="large")

        with ana_col1:
            st.markdown("#### Portal Volume Distribution")
            if source_col and source_col in filtered_df.columns and not filtered_df[source_col].isna().all():
                source_counts = filtered_df[source_col].value_counts().reset_index()
                source_counts.columns = ["Source", "Count"]
                st.bar_chart(source_counts.set_index("Source"), color="#0A66C2")
            else:
                st.info("No source breakdown available.")

        with ana_col2:
            st.markdown("#### Top Requested Skills")
            if "skills" in filtered_df.columns:
                all_skills = [
                    skill for skills_list in filtered_df["skills"].dropna() for skill in skills_list
                ]
                if all_skills:
                    skill_counts = pd.Series(all_skills).value_counts().head(10).reset_index()
                    skill_counts.columns = ["Skill", "Count"]
                    st.bar_chart(skill_counts.set_index("Skill"), color="#057642")
                else:
                    st.info("No skill tags parsed in the current filter selection.")


# =========================================================
# TAB 2: MY APPLICATIONS PIPELINE
# =========================================================
with tab2:
    st.markdown("### My Tracked Job Applications")
    st.markdown(
        "<p style='color:#4A4F55;'>Roles captured via your Plasmo browser extension while browsing JobStreet or MYFutureJobs.</p>",
        unsafe_allow_html=True,
    )

    try:
        db_path = Path(__file__).resolve().parents[2] / "data" / "job_market.duckdb"
        con = duckdb.connect(database=str(db_path), read_only=True)

        tables = con.execute("SHOW TABLES").fetchall()
        table_names = [t[0] for t in tables]

        if "job_applications" in table_names:
            df_apps = con.execute("SELECT * FROM job_applications ORDER BY applied_at DESC").fetchdf()
            con.close()

            if not df_apps.empty:
                c1, c2, c3 = st.columns(3)
                c1.metric("Applications Tracked", len(df_apps))
                c2.metric("Portals Used", df_apps["source_platform"].nunique())
                c3.metric("Active Pipeline", len(df_apps[df_apps["status"] != "Rejected"]))

                st.markdown("<br>", unsafe_allow_html=True)
                st.dataframe(df_apps, use_container_width=True, hide_index=True)
            else:
                st.info(
                    "No applications tracked yet. Load your Plasmo extension, browse JobStreet or MYFutureJobs, and click Track Application."
                )
        else:
            st.warning("The job_applications table hasn't been initialized yet. Run connection.py to create it.")
            con.close()
    except Exception as e:
        st.error(f"Error loading applications: {e}")