# HR Workforce Intelligence

Python-first workforce analytics project exploring employee attrition, hiring funnel metrics, compensation distributions, engagement, tenure cohorts, and headcount trends using synthetic data.

## Features
- Synthetic HR dataset included for safe demos
- Data-quality checks and profiling
- Attrition KPIs and department breakdowns
- Tenure cohort analysis
- Compensation summaries
- Hiring metrics and visualizations
- Streamlit dashboard
- Testable analytics functions separated from UI

## Run
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Ethics note
This demo uses synthetic data and predictive outputs, if later added, are decision-support only. Do not use employee analytics to automate hiring, firing, promotion, or other consequential decisions. Avoid individual-level risk scoring in real HR settings.

## Roadmap
- Robust statistical tests and confidence intervals
- Hiring funnel module
- Headcount forecast
- Salary-equity analysis with careful confounder controls
- API layer, tests, Docker, CI
