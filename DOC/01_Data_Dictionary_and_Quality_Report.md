# FinEdge Capital — Data Dictionary & Data Quality Report

**File:** `finedge_loan_portfolio.csv` / `finedge_loan_portfolio.xlsx`
**Rows:** 120,720 | **Columns:** 53 | **Encoding:** UTF-8
**Grain:** One row = one loan application/account

This file is deliberately exported in the same "raw core-banking extract" condition
a real analyst would receive it in — it contains missing values, mixed date formats,
duplicate rows, and outliers. Cleaning this is Phase 1 of the project (see Section 7
of the original project blueprint).

---

## 1. Data Dictionary

| # | Column | Type | Description | Notes |
|---|---|---|---|---|
| 1 | loan_id | string | Unique loan/account identifier (`LNxxxxxx`) | Primary key candidate |
| 2 | applicant_id | string | Unique borrower identifier (`APxxxxxx`) | One applicant can have multiple loans over time |
| 3 | customer_name | string | Borrower full name | Synthetic Indian names |
| 4 | gender | string | Male / Female | |
| 5 | date_of_birth | string (date) | Borrower DOB | YYYY-MM-DD |
| 6 | age | int | Borrower age at generation date | 21–64 |
| 7 | marital_status | string | Married / Single / Divorced / Widowed | |
| 8 | education | string | Highest education level | |
| 9 | occupation | string | Specific job/role | Mapped to employment_type |
| 10 | employment_type | string | Salaried / Self-Employed Professional / Self-Employed Business / Business Owner | Key risk driver |
| 11 | employer_name | string | Employer (or "Self Employed") | ~4.6% missing |
| 12 | years_with_employer | float | Tenure at current employer/business | ~3.9% missing |
| 13 | annual_income | float | Declared annual income (₹) | ~4.9% missing; contains outliers |
| 14 | monthly_income | float | Declared monthly income (₹) | ~4.4% missing; contains outliers |
| 15 | city | string | Applicant's city | |
| 16 | state | string | Applicant's state | |
| 17 | pincode | int | Postal code | |
| 18 | branch_id | string | Servicing branch code (`BRxxx`, 25 branches) | FK to branch dimension |
| 19 | branch_name | string | Branch name | |
| 20 | region | string | North / South / East / West / Central | |
| 21 | loan_product | string | Personal Loan / Auto Loan / Business Loan / Gold Loan | FK to product dimension |
| 22 | loan_purpose | string | Stated purpose of loan | |
| 23 | loan_amount | float | Amount requested (₹) | Contains ~0.2% outliers |
| 24 | sanctioned_amount | float | Amount approved (₹) | |
| 25 | disbursed_amount | float | Amount actually disbursed (₹) | |
| 26 | interest_rate | float | Annual interest rate (%) | |
| 27 | tenure_months | int | Loan tenure in months | |
| 28 | emi_amount | float | Monthly installment (₹) | Computed via standard amortization |
| 29 | processing_fee | float | One-time processing fee (₹) | |
| 30 | credit_score | float | Bureau score (300–900) | ~4.2% missing |
| 31 | debt_to_income_ratio | float | (Existing EMI + new EMI) / monthly income | Key risk driver |
| 32 | existing_loans_count | int | Active loans at application time | |
| 33 | existing_emi_obligations | float | Sum of existing EMIs (₹) | |
| 34 | collateral_type | string | None / Vehicle Hypothecation / Gold Ornaments | |
| 35 | collateral_value | float | Value of pledged collateral (₹) | ~3.4% missing (0 where unsecured) |
| 36 | co_applicant_flag | string | Yes/No | ~4.2% missing |
| 37 | application_date | string (date) | **Mixed formats intentionally**: YYYY-MM-DD, DD-MM-YYYY, DD/MM/YYYY, MM/DD/YYYY, "DD Mon YYYY" | Requires standardization |
| 38 | approval_date | string (date) | Same mixed-format issue | |
| 39 | disbursal_date | string (date) | Same mixed-format issue | |
| 40 | loan_status | string | Active / Closed / Default / Written-Off | |
| 41 | default_flag | int (0/1) | 1 if loan_status is Default or Written-Off | Target variable for modeling |
| 42 | days_past_due | float | Current/peak delinquency in days | ~4.3% missing |
| 43 | npa_flag | string | Yes if days_past_due ≥ 90 | |
| 44 | recovery_amount | float | Amount recovered post-default (₹) | ~4.0% missing |
| 45 | loan_officer_id | string | Processing officer code (`OFFxxxx`, 150 officers) | FK to officer dimension |
| 46 | loan_officer_name | string | Officer name | |
| 47 | payment_history_score | float | Internal behavioral score (100–900) | ~3.8% missing |
| 48 | bounce_count | int | Number of EMI payment bounces | |
| 49 | risk_category | string | Low / Medium / High / Very High | Derived from underlying default probability |
| 50 | customer_segment | string | Mass Market / Mass Affluent / Premium | Based on income band |
| 51 | is_fraud_suspected | string | Yes/No | ~0.4% flagged Yes |
| 52 | kyc_verified | string | Yes/No | ~1.5% flagged No |
| 53 | channel | string | Branch Walk-in / Digital App / DSA Referral / Tele-calling / Corporate Tie-up | |

---

## 2. Data Quality Report

| Issue | Where | Magnitude | Why it's there |
|---|---|---|---|
| Missing values | 10 columns (annual_income, monthly_income, credit_score, employer_name, years_with_employer, co_applicant_flag, payment_history_score, days_past_due, recovery_amount, collateral_value) | 3.2%–4.9% per column | Simulates incomplete core-banking sync / applicant non-disclosure |
| Duplicate rows | Scattered across dataset | ~0.6% (708 rows) | Simulates a batch resync/export error |
| Inconsistent date formats | application_date, approval_date, disbursal_date | 5 different formats mixed randomly | Simulates multi-source system export (core banking + digital app + DSA feed) |
| Outliers | monthly_income (~0.2%), loan_amount (~0.15%) | Extreme values 15–40x normal | Simulates data-entry errors / unverified declared income |
| Fraud flags | is_fraud_suspected | ~0.42% (510 rows) | Simulates rare but real fraud incidence, partly rule-based (loan-to-income > 18x) and partly random |
| Class imbalance | default_flag | ~5.3% positive class | Realistic for a lending portfolio — must be handled (stratified sampling / class weighting) in any ML step |

**Recommended cleaning order:** deduplicate → standardize dates (use `dateutil.parser` or explicit format detection) → impute missing numerics by employment_type+branch median → cap outliers at 99.5th percentile → validate referential integrity (branch_id, loan_officer_id) against dimension tables.

---

## 3. Business Assumptions

1. **Portfolio window:** Loans disbursed between Jan 2023 and Jun 2026 (reporting date assumed 30 Jun 2026).
2. **Default definition:** A loan is flagged `default_flag = 1` if its status is "Default" or "Written-Off" (i.e., 90+ DPD with no cure, per standard NBFC provisioning norms).
3. **Loss Given Default (LGD):** Not stored directly — assume 60% for unsecured products (Personal/Business Loan) and 35% for secured products (Auto/Gold Loan) when computing Expected Credit Loss, reflecting collateral recovery.
4. **Branch risk is structural, not random:** 4 branches (BR003, BR009, BR014, BR022) were deliberately calibrated with a higher underlying risk multiplier to simulate a real "problem branch" pattern for the analysis to discover.
5. **Officer performance varies:** Each of the 150 loan officers has a latent skill/diligence multiplier — some officers' portfolios will show statistically elevated default rates purely from underwriting quality, independent of branch or product.
5. **Income is self-declared and unverified** in ~0.2% of rows by design (outliers) — mirrors real-world declared-income risk in NBFC lending, especially for self-employed segments.
6. **Currency:** All monetary values in Indian Rupees (₹), not lakhs/crores, for direct SQL/BI aggregation.
