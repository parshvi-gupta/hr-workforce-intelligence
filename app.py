from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px
from src.analytics import attrition_rate, department_summary, tenure_bands, salary_summary, data_quality, validate_schema

st.set_page_config(page_title="HR Workforce Intelligence", page_icon="👥", layout="wide")
st.title("👥 HR Workforce Intelligence")
st.caption("Descriptive workforce analytics using synthetic sample data")
file = st.sidebar.file_uploader("Upload HR CSV", type=["csv"])
df = pd.read_csv(file) if file else pd.read_csv(Path("data/sample_employees.csv"))
issues = validate_schema(df)
if issues: st.error("Schema validation: " + " | ".join(issues))
else:
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Employees", f"{len(df):,}")
    c2.metric("Attrition rate", f"{attrition_rate(df):.1%}")
    c3.metric("Median salary", f"₹{df['monthly_salary'].median():,.0f}")
    c4.metric("Avg. engagement", f"{df['engagement_score'].mean():.2f}/5")
    st.subheader("Attrition by department")
    dept = department_summary(df).reset_index()
    st.plotly_chart(px.bar(dept, x="department", y="attrition_rate", color="department", labels={"attrition_rate":"Attrition rate"}), use_container_width=True)
    st.subheader("Tenure distribution")
    st.plotly_chart(px.bar(tenure_bands(df), x="tenure_band", y="employees"), use_container_width=True)
    st.subheader("Salary summary by department")
    st.dataframe(salary_summary(df), use_container_width=True)
    st.subheader("Data quality")
    st.dataframe(data_quality(df), use_container_width=True)
    with st.expander("Raw data preview"):
        st.dataframe(df, use_container_width=True)
st.info("Synthetic data only. These aggregate insights are descriptive and should not be used to automate employment decisions.")
