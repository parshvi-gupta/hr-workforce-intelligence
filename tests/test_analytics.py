import pandas as pd
from src.analytics import attrition_rate, department_summary, tenure_bands, salary_summary, validate_schema

def sample():
    return pd.DataFrame({"department":["A","A","B"],"tenure_years":[0.5,2,5],"monthly_salary":[10,20,30],"engagement_score":[2,4,3],"attrition":["Yes","No","No"]})

def test_attrition_rate():
    assert attrition_rate(sample()) == 1/3

def test_department_summary_counts():
    result=department_summary(sample())
    assert result.loc["A","employee_count"] == 2

def test_tenure_bands():
    assert tenure_bands(sample())["employees"].sum() == 3

def test_salary_summary():
    assert salary_summary(sample()).loc["A","median"] == 15

def test_schema_ok():
    assert validate_schema(sample()) == []
