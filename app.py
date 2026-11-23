from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px
from src.analytics import attrition_rate, department_summary, tenure_bands, salary_summary, data_quality, validate_schema

st.set_page_config(page_title="HR Workforce Intelligence", page_icon="👥", layout="wide")
st.markdown("""
<style>
.block-container {padding-top:1.6rem; padding-bottom:2.5rem;}
[data-testid="stMetric"] {background:rgba(120,120,120,.07); padding:14px 16px; border-radius:14px; border:1px solid rgba(120,120,120,.15);}
</style>
""", unsafe_allow_html=True)
st.title("👥 HR Workforce Intelligence")
st.caption("Understand workforce patterns through descriptive, aggregate analytics.")

@st.cache_data
def sample_data():
    return pd.read_csv(Path("data/sample_employees.csv"))

with st.sidebar:
    st.header("Data")
    file = st.file_uploader("Upload HR CSV", type=["csv"])
    if file:
        try:
            raw_df = pd.read_csv(file)
        except Exception as exc:
            st.error(f"Could not read CSV: {exc}")
            st.stop()
    else:
        raw_df = sample_data()
        st.info("Sample workforce loaded")
    st.caption("Synthetic sample data is provided for safe exploration.")

issues = validate_schema(raw_df)
if issues:
    st.error("Dataset schema needs attention")
    for issue in issues:
        st.write(f"• {issue}")
    st.info("Required columns: department, tenure_years, monthly_salary, engagement_score, attrition. Upload a matching dataset to view analytics.")
    st.subheader("Uploaded data preview")
    st.dataframe(raw_df.head(100), use_container_width=True)
    st.stop()

# Basic input safety: ensure required columns are numeric where metrics expect them
for col in ["tenure_years", "monthly_salary", "engagement_score"]:
    raw_df[col] = pd.to_numeric(raw_df[col], errors="coerce")
if raw_df.empty:
    st.warning("The dataset is empty.")
    st.stop()

st.sidebar.subheader("Filters")
departments = sorted(raw_df["department"].dropna().astype(str).unique())
selected_depts = st.sidebar.multiselect("Department", departments, default=departments)
locations = sorted(raw_df["location"].dropna().astype(str).unique()) if "location" in raw_df else []
selected_locations = st.sidebar.multiselect("Location", locations, default=locations) if locations else []
df = raw_df.copy()
if selected_depts:
    df = df[df["department"].astype(str).isin(selected_depts)]
if selected_locations:
    df = df[df["location"].astype(str).isin(selected_locations)]
if df.empty:
    st.warning("No employees match these filters. Adjust your selections.")
    st.stop()

c1,c2,c3,c4 = st.columns(4)
c1.metric("Employees", f"{len(df):,}")
c2.metric("Attrition rate", f"{attrition_rate(df):.1%}")
c3.metric("Median monthly salary", f"₹{df['monthly_salary'].median():,.0f}" if df["monthly_salary"].notna().any() else "N/A")
c4.metric("Average engagement", f"{df['engagement_score'].mean():.2f}/5" if df["engagement_score"].notna().any() else "N/A")

overview, attrition, compensation, quality = st.tabs(["Overview", "Attrition", "Compensation & tenure", "Data quality"])
with overview:
    a,b = st.columns(2)
    with a:
        st.subheader("Headcount by department")
        count = df.groupby("department").size().sort_values(ascending=False).reset_index(name="employees")
        st.plotly_chart(px.bar(count, x="department", y="employees", color="department", text_auto=True), use_container_width=True)
    with b:
        st.subheader("Workforce by location")
        if "location" in df.columns:
            loc = df.groupby("location").size().reset_index(name="employees")
            st.plotly_chart(px.pie(loc, names="location", values="employees", hole=.55), use_container_width=True)
        else:
            st.info("No location column in this dataset.")
    st.subheader("Department summary")
    st.dataframe(department_summary(df).style.format({"attrition_rate":"{:.1%}"}), use_container_width=True)
with attrition:
    st.subheader("Attrition patterns")
    dept = department_summary(df).reset_index()
    fig = px.bar(dept, x="department", y="attrition_rate", color="department", text_auto=".1%", labels={"attrition_rate":"Attrition rate"}, title="Attrition rate by department")
    fig.update_yaxes(tickformat=".0%", range=[0, max(.05, float(dept["attrition_rate"].max())*1.15)])
    st.plotly_chart(fig, use_container_width=True)
    if "hire_date" in df:
        hires = pd.to_datetime(df["hire_date"], errors="coerce").dropna()
        if not hires.empty:
            st.subheader("Hiring over time")
            hires_df = hires.dt.to_period("Y").astype(str).value_counts().sort_index().rename_axis("Year").reset_index(name="Hires")
            st.bar_chart(hires_df.set_index("Year"))
    st.caption("Patterns are descriptive, not causal. They should not be used to automate employment decisions.")
with compensation:
    a,b = st.columns(2)
    with a:
        st.subheader("Tenure distribution")
        st.bar_chart(tenure_bands(df).set_index("tenure_band"))
    with b:
        st.subheader("Monthly salary by department")
        salary = df.groupby("department")["monthly_salary"].median().dropna().sort_values()
        if not salary.empty:
            st.bar_chart(salary)
    st.subheader("Compensation detail")
    st.dataframe(salary_summary(df), use_container_width=True)
with quality:
    st.subheader("Data quality")
    dq = data_quality(df)
    dq["missing_pct"] = dq["missing_pct"].map(lambda v: f"{v:.1f}%")
    st.dataframe(dq, use_container_width=True)
    st.caption("Quality indicators help identify missing or inconsistent inputs before analysis.")
with st.expander("Raw data preview"):
    st.dataframe(df.head(250), use_container_width=True)
st.info("Synthetic sample only. This dashboard provides aggregate descriptive insights—not employee-level risk scores or automated HR recommendations.")
