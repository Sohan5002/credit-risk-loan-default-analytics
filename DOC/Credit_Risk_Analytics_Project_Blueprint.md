# Credit Risk & Loan Default Analytics — Full Project Blueprint
### For 15+ LPA Data Analyst Roles (Amex / Fractal / Tiger / ZS / Walmart Global Tech tier)

---

## 1. Business Problem Statement

**FinEdge Capital** (fictional NBFC — Non-Banking Financial Company) issues personal, auto, and small-business loans across 25 branches in India. Over the last 3 years, the gross default rate has climbed from 4.1% to 7.8%, eroding net interest margin. The Chief Risk Officer needs a data-driven view of **who defaults, why, and which branches/loan officers/products are driving the loss**, so that underwriting policy and collections strategy can be corrected before the next lending cycle.

**Core question:** *Which borrower segments, loan products, and branches carry disproportionate default risk, and how much would tightening underwriting on the top 3 risk drivers save annually?*

---

## 2. Industry Background

NBFCs and digital lenders operate on thinner capital buffers than banks and are more sensitive to default-rate swings. Post-2023, RBI tightened unsecured lending norms, and rising interest rates increased EMI burden on variable-rate borrowers. Consulting firms like Fractal, ZS, and Tiger Analytics run exactly this kind of engagement for lending clients: **portfolio risk segmentation, early-warning scorecards, and collections prioritization**. This project mirrors a real "credit risk analytics" statement of work.

---

## 3. Stakeholders

| Stakeholder | Interest |
|---|---|
| Chief Risk Officer (CRO) | Overall default rate, capital-at-risk exposure |
| Head of Underwriting | Which applicant attributes predict default, policy thresholds |
| Branch Operations Heads | Branch-level performance, staff accountability |
| Collections Team Lead | Which delinquent accounts to prioritize (recovery likelihood) |
| Finance/Treasury | Provisioning (expected credit loss) impact |

---

## 4. Business Requirements

1. A single source of truth dashboard showing portfolio health (default rate, NPA%, exposure) refreshed monthly.
2. Segment-level default analysis by product, tenure, income band, credit score band, employment type, and branch.
3. A ranked list of top risk-driving factors backed by statistical testing, not just visual correlation.
4. A collections-priority list ranking currently-delinquent accounts by recovery probability.
5. A quantified recommendation: "If we cut approvals for [segment], we reduce projected default losses by ₹[X] annually."

---

## 5. Dataset Description

Real-world lending datasets exist (e.g., Lending Club, HMDA, Kaggle "Loan Default Prediction") but are overused. **Recommended approach: generate a realistic synthetic dataset (120,000 rows)** that mirrors real loan bureau structure — this is a legitimate, industry-standard technique data teams use in interviews ("I built a synthetic dataset modeled on real bureau schema because production lending data is sensitive/regulated") and it signals data-engineering maturity, not just dashboard-building.

**Generation approach (Python, `faker` + `numpy` + realistic correlation logic):**
- Simulate 120,000 loan applications over 36 months across 25 branches, 4 loan products (Personal, Auto, Business, Gold Loan).
- Bake in *realistic, non-random* default correlations: lower credit score → higher default probability; high debt-to-income → higher default; certain branches → higher fraud/default (to simulate a real finding); seasonal disbursal spikes.
- This avoids "clean toy data" — intentionally inject 3–5% missing values, a few duplicate applicant IDs, inconsistent date formats, and outlier incomes to justify a real cleaning section (Section 7).

I can generate this exact dataset for you as a next step (Python script, ~120k rows, CSV) if you want to move straight into building.

---

## 6. Data Dictionary

| Column | Type | Description |
|---|---|---|
| loan_id | string | Unique loan identifier |
| applicant_id | string | Unique borrower identifier |
| branch_id | string | Branch code (25 branches) |
| loan_product | category | Personal / Auto / Business / Gold Loan |
| disbursal_date | date | Loan disbursal date |
| loan_amount | float | Principal disbursed (₹) |
| tenure_months | int | Loan tenure |
| interest_rate | float | Annual interest rate (%) |
| credit_score | int | Bureau score (300–900) |
| monthly_income | float | Declared monthly income (₹) |
| debt_to_income_ratio | float | Existing EMI burden / income |
| employment_type | category | Salaried / Self-Employed / Business Owner |
| age | int | Applicant age |
| existing_loans_count | int | Active loans at time of application |
| emi_amount | float | Monthly installment |
| days_past_due | int | Current delinquency (0 = current) |
| loan_status | category | Active / Closed / Default / Written-Off |
| collateral_value | float | For secured loans (Auto/Gold) |
| loan_officer_id | string | Officer who processed the loan |

---

## 7. Data Cleaning Process

1. **Duplicate applicant IDs:** Deduplicate on `applicant_id + loan_id`, flag repeat borrowers separately (not an error — a real behavior).
2. **Missing income values (~4%):** Impute using median income by employment_type + branch, not global median — document the assumption.
3. **Inconsistent date formats:** Standardize `disbursal_date` (some rows simulate DD-MM-YYYY vs YYYY-MM-DD).
4. **Outlier detection:** Flag incomes >99.5th percentile and loan amounts inconsistent with declared income (potential data entry error vs. fraud signal — keep both interpretations documented).
5. **Referential integrity check:** Every `loan_officer_id` and `branch_id` must exist in a lookup dimension table — build this as part of the star schema (Section 16).

---

## 8. SQL Analysis (Core)

```sql
-- Overall default rate by product
SELECT loan_product,
       COUNT(*) AS total_loans,
       SUM(CASE WHEN loan_status = 'Default' THEN 1 ELSE 0 END) AS defaults,
       ROUND(100.0 * SUM(CASE WHEN loan_status = 'Default' THEN 1 ELSE 0 END) / COUNT(*), 2) AS default_rate_pct
FROM loans
GROUP BY loan_product
ORDER BY default_rate_pct DESC;
```

```sql
-- Default rate by credit score band
SELECT
  CASE
    WHEN credit_score < 600 THEN 'Below 600'
    WHEN credit_score BETWEEN 600 AND 699 THEN '600-699'
    WHEN credit_score BETWEEN 700 AND 799 THEN '700-799'
    ELSE '800+'
  END AS score_band,
  COUNT(*) AS total_loans,
  ROUND(100.0 * SUM(CASE WHEN loan_status='Default' THEN 1 ELSE 0 END)/COUNT(*),2) AS default_rate_pct
FROM loans
GROUP BY score_band
ORDER BY default_rate_pct DESC;
```

---

## 9. Advanced SQL (CTEs, Window Functions, Views, Indexes)

```sql
-- CTE + Window Function: Rank branches by default rate, show rolling 3-month trend
WITH branch_monthly AS (
  SELECT branch_id,
         DATE_TRUNC('month', disbursal_date) AS month,
         COUNT(*) AS loans_issued,
         SUM(CASE WHEN loan_status='Default' THEN 1 ELSE 0 END) AS defaults
  FROM loans
  GROUP BY branch_id, DATE_TRUNC('month', disbursal_date)
),
branch_ranked AS (
  SELECT *,
         ROUND(100.0*defaults/loans_issued,2) AS default_rate,
         AVG(100.0*defaults/loans_issued) OVER (
           PARTITION BY branch_id ORDER BY month
           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
         ) AS rolling_3mo_default_rate,
         RANK() OVER (PARTITION BY month ORDER BY 100.0*defaults/loans_issued DESC) AS risk_rank
  FROM branch_monthly
)
SELECT * FROM branch_ranked WHERE risk_rank <= 5;
```

```sql
-- View for the dashboard layer (single reusable object)
CREATE VIEW vw_portfolio_risk_summary AS
SELECT branch_id, loan_product, employment_type,
       COUNT(*) AS total_loans,
       AVG(credit_score) AS avg_credit_score,
       SUM(CASE WHEN loan_status='Default' THEN loan_amount ELSE 0 END) AS defaulted_exposure
FROM loans
GROUP BY branch_id, loan_product, employment_type;

-- Index to speed up dashboard queries filtering by date + status
CREATE INDEX idx_loans_status_date ON loans(loan_status, disbursal_date);
```

---

## 10. Python (Pandas, NumPy, Matplotlib/Plotly)

```python
import pandas as pd, numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("loans.csv", parse_dates=["disbursal_date"])

# Default flag
df["is_default"] = (df["loan_status"] == "Default").astype(int)

# Debt-to-income vs default rate, binned
df["dti_band"] = pd.qcut(df["debt_to_income_ratio"], 5)
dti_default = df.groupby("dti_band")["is_default"].mean().reset_index()

plt.figure(figsize=(8,5))
plt.bar(dti_default["dti_band"].astype(str), dti_default["is_default"]*100)
plt.ylabel("Default Rate (%)"); plt.xlabel("Debt-to-Income Band")
plt.title("Default Rate by Debt-to-Income Quintile")
plt.xticks(rotation=30); plt.tight_layout(); plt.show()
```

---

## 11. Exploratory Data Analysis (EDA)

- Univariate: distribution of credit_score, loan_amount, tenure — check skew, cap outliers.
- Bivariate: default rate vs. credit score band, vs. employment type, vs. branch, vs. loan officer (surface any single officer with abnormally high defaults — a real audit flag).
- Correlation heatmap: credit_score, DTI, income, age, existing_loans_count vs. is_default.
- Time series: monthly default rate trend — check if the 4.1%→7.8% rise is uniform or concentrated in specific quarters/products (likely story: unsecured Personal loans post rate-hike quarter).

---

## 12. Statistical Analysis

- **Chi-square test:** employment_type vs. default (categorical vs. categorical) — is the association statistically significant, or noise?
- **Two-sample t-test:** mean credit_score of defaulters vs. non-defaulters — quantify the gap with a p-value, not just "defaulters have lower scores."
- **Logistic regression** (simple, interpretable — not a black box): `is_default ~ credit_score + DTI + income + employment_type + tenure`. Report odds ratios: *"Each 50-point drop in credit score increases default odds by X%."* This single step is what separates a "dashboard project" from a "data analyst who understands risk modeling," and it's exactly what a Fractal/ZS interviewer will probe.

---

## 13. Feature Engineering

- `credit_utilization_proxy` = existing_loans_count / tenure_months
- `income_to_loan_ratio` = monthly_income*12 / loan_amount
- `is_high_risk_branch` = flag based on branch's historical default rate (rolling)
- `tenure_bucket` = short (<12mo) / medium / long
- `vintage_quarter` = quarter of disbursal, to test cohort-based default curves (a real risk-team technique: "vintage analysis")

---

## 14. Power BI Dashboard (Pages)

1. **Executive Summary:** Total exposure, overall default rate (with trend arrow vs. last quarter), NPA%, provisioning estimate.
2. **Segment Deep-Dive:** Default rate sliced by product/credit-score band/employment — interactive slicers.
3. **Branch & Officer Performance:** Ranked branch table with conditional formatting; drill-through to officer-level.
4. **Collections Priority View:** Currently delinquent accounts ranked by a simple recovery-likelihood score (based on days-past-due, collateral value, past payment history).
5. **What-If Page:** A DAX-driven slider simulating "if we raise minimum credit score cutoff to X, projected default rate and lost-volume trade-off."

---

## 15. Advanced DAX Measures

```dax
Default Rate % =
DIVIDE(
    CALCULATE(COUNTROWS(Loans), Loans[loan_status] = "Default"),
    COUNTROWS(Loans)
)

Rolling 3M Default Rate =
CALCULATE(
    [Default Rate %],
    DATESINPERIOD('Date'[Date], MAX('Date'[Date]), -3, MONTH)
)

Expected Credit Loss (ECL) =
SUMX(
    Loans,
    Loans[loan_amount] * [Default Rate %] * 0.6  -- 0.6 = assumed Loss Given Default
)

Risk-Adjusted Branch Rank =
RANKX(ALL(Loans[branch_id]), CALCULATE([Default Rate %]), , ASC)

YoY Default Rate Change =
VAR CurrentYear = [Default Rate %]
VAR PriorYear = CALCULATE([Default Rate %], SAMEPERIODLASTYEAR('Date'[Date]))
RETURN CurrentYear - PriorYear
```

---

## 16. Star Schema Data Model

**Fact table:** `Fact_Loans` (loan_id, applicant_key, branch_key, product_key, officer_key, date_key, loan_amount, emi_amount, is_default, days_past_due)

**Dimension tables:**
- `Dim_Applicant` (applicant_key, age, employment_type, credit_score_band, income_band)
- `Dim_Branch` (branch_key, branch_name, region, state)
- `Dim_Product` (product_key, loan_product, is_secured)
- `Dim_Officer` (officer_key, officer_name, branch_key, tenure_years)
- `Dim_Date` (date_key, date, month, quarter, year, fiscal_year)

This is the detail that signals "I understand data modeling for BI performance," not just flat-table dashboards — a common gap interviewers probe for at the 15+ LPA level.

---

## 17. KPIs and Metrics

- Overall Default Rate %, NPA % (90+ days past due)
- Expected Credit Loss (₹)
- Portfolio at Risk (PAR 30/60/90)
- Approval Rate by segment
- Average Days-to-Default (survival-style metric)
- Officer-level default rate variance

---

## 18. Business Insights (Illustrative — replace with your actual output numbers)

- Unsecured Personal Loans to self-employed applicants with DTI > 45% show 3.2x the default rate of the portfolio average.
- 4 of 25 branches account for 38% of total defaulted exposure despite issuing only 19% of loans.
- Credit score alone explains a meaningful share of default variance, but DTI adds significant incremental predictive power (from the logistic regression).
- Defaults cluster heavily in the 6th–9th month of the loan (early-tenure risk), suggesting underwriting — not macro shocks — is the primary driver.

---

## 19. Recommendations

1. Raise minimum credit score threshold for unsecured Personal Loans from [X] to [Y] in the 4 flagged high-risk branches.
2. Cap DTI at 40% for self-employed applicants pending income verification improvements.
3. Introduce a mandatory second-level review for loan officers whose default rate exceeds 2 standard deviations from the branch mean.
4. Prioritize collections outreach using the recovery-likelihood score rather than simple days-past-due ordering.

---

## 20. ROI / Business Impact

If tightening the 3 flagged risk drivers reduces default rate on the affected segment from 7.8% to 5.5% on a ₹[total exposure] portfolio, estimated annual loss avoidance ≈ **₹[exposure × 2.3% × (1 – recovery rate)]**. Frame this as a single headline number in your resume bullet and README — it's the sentence a hiring manager remembers.

---

## 21. Challenges Faced (write these honestly once you build it — sample framing)

- Balancing realistic default correlation without a real bureau dataset — solved by researching public NBFC risk reports to calibrate synthetic probabilities.
- Avoiding data leakage in the logistic regression (e.g., `days_past_due` should not be a feature if it's a symptom of default already occurring, not a predictor).
- Keeping the Power BI model performant with 120k+ rows and multiple slicers — solved via star schema + aggregated views instead of live-querying the flat fact table.

---

## 22. Future Improvements

- Replace logistic regression with a gradient-boosted model (XGBoost) and compare AUC — shows growth path toward Data Science.
- Add a real-time scoring API stub (Flask) for new applications.
- Incorporate macroeconomic variables (repo rate, inflation) for a vintage-cohort stress test.

---

## Folder / GitHub Repository Structure

```
credit-risk-analytics/
├── data/
│   ├── raw/loans_raw.csv
│   ├── processed/loans_cleaned.csv
├── notebooks/
│   ├── 01_data_generation.ipynb
│   ├── 02_data_cleaning_eda.ipynb
│   ├── 03_statistical_analysis.ipynb
│   └── 04_feature_engineering.ipynb
├── sql/
│   ├── schema.sql
│   ├── views.sql
│   └── analysis_queries.sql
├── powerbi/
│   └── Credit_Risk_Dashboard.pbix
├── images/
│   └── dashboard_screenshots/
├── README.md
└── requirements.txt
```

---

## README.md Content (ready to paste)

```markdown
# Credit Risk & Loan Default Analytics — FinEdge Capital (Simulated NBFC)

## Overview
End-to-end analytics project identifying key drivers of loan default across a
25-branch NBFC lending portfolio (120,000+ simulated loans), quantifying
Expected Credit Loss, and recommending underwriting policy changes projected
to reduce default-related losses by ₹[X] annually.

## Business Problem
FinEdge Capital's default rate rose from 4.1% to 7.8% over 3 years. This
project identifies which segments, branches, and products drive that increase
and quantifies the financial impact of corrective underwriting policy.

## Tech Stack
SQL (PostgreSQL) · Python (Pandas, NumPy, statsmodels, Matplotlib) · Power BI · DAX

## Key Findings
- [Insert your top 3 quantified findings]

## Dashboard
![Executive Summary](images/dashboard_screenshots/exec_summary.png)

## Repository Structure
[link to structure above]

## How to Reproduce
1. Run `notebooks/01_data_generation.ipynb` to generate the synthetic dataset.
2. Load `sql/schema.sql` into PostgreSQL, run `analysis_queries.sql`.
3. Open `powerbi/Credit_Risk_Dashboard.pbix` and refresh the data source.
```

---

## Resume Project Description (ATS-optimized, 4 bullets)

**Credit Risk & Loan Default Analytics | SQL, Python, Power BI, Statistics**
- Built an end-to-end credit risk analytics pipeline on a 120,000-row simulated NBFC loan portfolio, identifying key default drivers using SQL and logistic regression.
- Designed a star-schema data model and 15+ advanced SQL queries (CTEs, window functions, views) to quantify default rate by branch, product, and credit-score band.
- Developed a 5-page Power BI dashboard with advanced DAX (Expected Credit Loss, rolling default rate, risk-adjusted branch ranking) used to simulate underwriting policy changes.
- Quantified that tightening underwriting on the top 3 risk drivers could reduce annual default-related losses by an estimated ₹[X], and presented findings as actionable policy recommendations.

---

## LinkedIn Post (after completion)

> Just wrapped up a project I'm genuinely proud of: a full credit risk analytics pipeline for a simulated NBFC lending portfolio (120K+ loan records).
>
> The goal wasn't another dashboard — it was answering a real question: *which borrower segments and branches are driving rising loan defaults, and what would fixing it save?*
>
> What it involved:
> 🔹 SQL (CTEs, window functions, views) to segment risk across branches & products
> 🔹 Python + statsmodels for logistic regression to quantify default drivers (not just visualize them)
> 🔹 A star-schema data model + Power BI dashboard with DAX-driven Expected Credit Loss calculations
> 🔹 A final, quantified recommendation: tightening underwriting on the top risk drivers could cut default losses by ~₹[X]/year
>
> Full writeup + dashboard + code: [GitHub link]
>
> #DataAnalytics #SQL #PowerBI #CreditRisk #DataScience

---

## Interview Questions Likely Based on This Project (+ Answers)

**Q1: Why did you use synthetic data instead of a public Kaggle dataset?**
A: Real lending data is regulated/sensitive, so I modeled the schema and default correlations on publicly documented NBFC risk patterns (bureau score, DTI, employment type) to build a dataset with realistic signal, rather than relying on an already-cleaned Kaggle set that hides the data-quality problems real analysts face.

**Q2: Walk me through how you determined which factors actually drive default, not just correlate with it.**
A: I ran a chi-square test for categorical variables like employment type, a t-test comparing credit scores between defaulters and non-defaulters, and a logistic regression with multiple predictors together — this controls for confounding, so I can say DTI adds predictive power *independent of* credit score, not just that both move together.

**Q3: Why exclude `days_past_due` as a feature in the default prediction model?**
A: It's a data leakage risk — days past due is often a symptom that default is already occurring, not an independent predictor available at the time of underwriting. Including it would inflate model performance artificially.

**Q4: How did you decide on the star schema instead of one flat table?**
A: With 120K+ fact rows and multiple slicers (branch, product, date, officer), a flat table causes slow refreshes and duplicated dimension data. Splitting into fact/dimension tables reduced model size and made DAX time-intelligence functions (like rolling default rate) work correctly against a proper date dimension.

**Q5: What's Expected Credit Loss and how did you calculate it here?**
A: ECL approximates expected default losses using Probability of Default × Exposure at Default × Loss Given Default. I used the empirical default rate as a PD proxy, loan_amount as exposure, and assumed a 60% loss-given-default (industry-typical range for unsecured lending) as a simplifying assumption, which I documented clearly.

**Q6: If the CRO asked you to cut the false positive rate on your risk flag (avoid rejecting good borrowers), how would you adjust your approach?**
A: I'd move from a single hard credit-score cutoff to a probability threshold from the logistic regression, then tune the threshold against a cost matrix — weighing the cost of a missed default against the revenue lost from rejecting a good borrower, rather than eyeballing one variable.

**Q7: How would this differ with real production data at scale (millions of rows)?**
A: I'd move cleaning/aggregation into SQL or a Spark job rather than Pandas in memory, materialize the star schema as actual tables/views in the warehouse instead of building it inside Power BI, and add incremental refresh instead of full reloads.

---

## Expected Duration
**3–4 weeks** at a steady pace (evenings/weekends): Week 1 data generation + cleaning, Week 2 SQL + Python/stats, Week 3 Power BI + DAX, Week 4 polish, README, LinkedIn, mock interview prep.

## Difficulty Level
**Advanced-Intermediate** — the SQL/DAX/dashboard work is intermediate; the statistical modeling and data-model design are what push it to a level most fresher portfolios don't reach.

## Skills Demonstrated
SQL (advanced), Python (Pandas/NumPy/statsmodels), statistical hypothesis testing, logistic regression, data modeling (star schema), Power BI, advanced DAX, business framing/ROI communication, synthetic data generation.

## Companies That Would Value This Most
American Express, Fractal Analytics, ZS Associates (via financial services clients), Tiger Analytics, any NBFC/bank/fintech (Axis, HDFC, Bajaj Finserv, Paytm), and general Data Analyst roles anywhere risk/credit/collections analytics is relevant. Walmart/Google/Microsoft value the *rigor* (stats + data modeling) even if the specific domain differs.

---

## Top 10 Data Analyst Project Ideas — Ranked for 2026 Hiring Impact

| Rank | Project | Why it Ranks Here |
|---|---|---|
| **1** | **Credit Risk & Loan Default Analytics** (this one) | Universally valued domain, forces statistics + data modeling, quantifiable ROI, rarely overdone |
| 2 | Healthcare Claims Cost & Fraud Analytics | Excellent for ZS/pharma-adjacent roles; strong stats angle; less universal outside healthcare |
| 3 | Supply Chain Demand Forecasting & Stockout Cost Analysis | Great for Walmart/retail/CPG; requires time-series forecasting, a strong differentiator |
| 4 | SaaS Customer Churn & Revenue Leakage Analytics (with cohort/LTV analysis) | Strong for tech/product companies; cohort analysis is a valued, less-common skill |
| 5 | Insurance Claims Reserve & Loss Ratio Analytics | Niche but high-value for insurance-focused analytics teams |
| 6 | Marketing Attribution & Customer Acquisition Cost Analytics | Good for growth/marketing analytics roles; multi-touch attribution is a strong differentiator |
| 7 | Employee Attrition Cost & Workforce Risk Analytics (beyond generic "HR Dashboard" — with survival analysis) | Only ranks this low if done shallow; done with survival analysis, jumps to top 5 |
| 8 | Fraud Detection in Digital Payments (transaction-level anomaly detection) | High interest but harder to make realistic without real transaction data; risk of looking like a toy ML project |
| 9 | Real Estate Pricing & Market Trend Analytics | Decent breadth but oversaturated as a "regression practice" project |
| 10 | Energy Consumption / Smart Grid Analytics | Interesting technically but low relevance unless targeting energy-sector employers specifically |

**Final recommendation:** Build the **Credit Risk & Loan Default Analytics** project. It's the one where the statistics section alone will differentiate you in an interview room from 90% of candidates who only show dashboards, and the ROI framing (₹ saved annually) is exactly the sentence that gets a resume pulled out of a stack for a 15+ LPA role.
