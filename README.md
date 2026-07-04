# Credit Risk & Loan Default Analytics

An end-to-end **Data Analytics** project that simulates a real-world **NBFC loan portfolio** to analyze credit risk, loan defaults, customer behavior, and lending performance using **Python, SQL, and Power BI**.

---

## Project Overview

Financial institutions rely on data-driven insights to reduce credit risk and improve lending decisions. This project analyzes a synthetic loan portfolio containing **120,720 loan records** and **53 business attributes**.

The dataset intentionally contains real-world data quality issues such as:

- Missing values
- Duplicate records
- Mixed date formats
- Outliers
- Fraud flags
- Class imbalance

These challenges simulate the raw data analysts typically receive from core banking systems.

---

## Project Objectives

- Clean and prepare raw banking data
- Perform Exploratory Data Analysis (EDA)
- Identify key drivers of loan defaults
- Analyze branch and loan officer performance
- Build SQL-based business reports
- Create an interactive Power BI dashboard
- Generate actionable business insights

---

## Tech Stack

- Python
- Pandas
- NumPy
- MySQL
- Power BI
- Excel
- Jupyter Notebook
- Git & GitHub

---

## Dataset Information

| Attribute | Value |
|-----------|--------|
| Industry | NBFC / Banking |
| Records | 120,720 |
| Columns | 53 |
| Dataset Type | Synthetic |
| Currency | Indian Rupees (₹) |

---

## Project Structure

```text
credit-risk-loan-default-analytics/
│
├── data/
│   ├── raw/
│   │   ├── loans_raw.csv
│   │   └── loans_raw.xlsx
│   │
│   └── processed/
│       ├── loans_cleaned.csv
│       └── loans_cleaned.xlsx
│
├── docs/
│   ├── 01_Data_Dictionary_and_Quality_Report.md
│   ├── 02_ER_Diagram_StarSchema_and_SQL_DDL.md
│   └── Credit_Risk_Analytics_Project_Blueprint.md
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_statistical_analysis.ipynb
│   └── 04_feature_engineering.ipynb
│
├── sql/
│   ├── schema.sql
│   ├── views.sql
│   └── analysis_queries.sql
│
├── powerbi/
│   └── Credit_Risk_Dashboard.pbix
│
├── images/
│   └── dashboard_screenshots/
│
├── generate_dataset.py
├── requirements.txt
└── README.md
```

---

## Project Workflow

1. Data Cleaning
2. Exploratory Data Analysis (EDA)
3. SQL Data Analysis
4. Statistical Analysis
5. Feature Engineering
6. Business KPI Reporting
7. Power BI Dashboard
8. Business Insights & Recommendations

---

## Key Business Questions

- Which branches have the highest default rate?
- Which loan products have the highest credit risk?
- How does credit score impact default probability?
- Which loan officers manage the best-performing portfolios?
- Which customer segments contribute most to defaults?
- How does Debt-to-Income (DTI) ratio influence loan performance?

---

## Dashboard Features

- Executive Portfolio Overview
- Default Analysis
- Branch Performance
- Loan Product Analysis
- Customer Segmentation
- Risk Distribution
- Loan Officer Performance
- Interactive KPI Cards
- Dynamic Filters & Slicers

---

## Skills Demonstrated

- Data Cleaning
- Data Validation
- SQL Query Writing
- Exploratory Data Analysis
- Statistical Analysis
- Data Modeling
- Feature Engineering
- Power BI Dashboard Development
- Business Intelligence
- Data Storytelling

---

## Future Enhancements

- Loan Default Prediction using Machine Learning
- Expected Credit Loss (ECL) Analysis
- Customer Risk Scoring
- Portfolio Stress Testing
- Real-Time Credit Risk Dashboard


