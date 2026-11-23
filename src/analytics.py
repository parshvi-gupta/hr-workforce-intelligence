"""Reusable HR metrics and descriptive analyses."""
from __future__ import annotations
import pandas as pd

REQUIRED = {"department", "tenure_years", "monthly_salary", "engagement_score", "attrition"}

def validate_schema(df: pd.DataFrame) -> list[str]:
    missing = sorted(REQUIRED - set(df.columns))
    return [f"Missing required column: {c}" for c in missing]

def attrition_rate(df: pd.DataFrame) -> float:
    if "attrition" not in df.columns or df.empty: return 0.0
    return float(df["attrition"].astype(str).str.strip().str.lower().isin(["yes", "true", "1"]).mean())

def department_summary(df: pd.DataFrame) -> pd.DataFrame:
    if "department" not in df or "attrition" not in df: raise ValueError("department and attrition columns are required")
    work = df.assign(_left=df["attrition"].astype(str).str.lower().isin(["yes", "true", "1"]))
    return work.groupby("department").agg(employee_count=("_left", "size"), attrition_count=("_left", "sum"), attrition_rate=("_left", "mean")).sort_values("attrition_rate", ascending=False)

def tenure_bands(df: pd.DataFrame) -> pd.DataFrame:
    if "tenure_years" not in df: raise ValueError("tenure_years column required")
    bands = pd.cut(df["tenure_years"], bins=[-0.01, 1, 3, 5, 10, float("inf")], labels=["0–1", "1–3", "3–5", "5–10", "10+"], include_lowest=True)
    return df.assign(tenure_band=bands).groupby("tenure_band", observed=False).size().rename("employees").reset_index()

def salary_summary(df: pd.DataFrame) -> pd.DataFrame:
    if "department" not in df or "monthly_salary" not in df: raise ValueError("department and monthly_salary required")
    return df.groupby("department")["monthly_salary"].agg(["count", "median", "mean", "min", "max"]).round(2)

def data_quality(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({"dtype": df.dtypes.astype(str), "missing": df.isna().sum(), "missing_pct": (df.isna().mean()*100).round(2), "unique": df.nunique()})
