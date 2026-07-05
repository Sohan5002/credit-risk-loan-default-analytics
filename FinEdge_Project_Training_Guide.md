# Learn the FinEdge Capital Project — From Zero to Data Analyst

*A complete, beginner-friendly walkthrough of the "Credit Risk & Loan Default Analytics" project*

This guide teaches you the **actual files you uploaded**:
- `README.md`
- `01_Data_Dictionary_and_Quality_Report.md`
- `02_ER_Diagram_StarSchema_and_SQL_DDL.md`
- `generate_dataset.py`
- `finedge_loan_portfolio.csv` / `.xlsx` (120,720 rows × 53 columns)

We go step by step, in plain English, like you have never seen a data project before.

---

## 1. Project Overview

### What is this project?

Imagine a company that lends money to people — for buying a car, starting a business, or covering a medical emergency. This company keeps a giant record of every loan it has ever given: who took it, how much, whether they paid it back on time, and whether they defaulted (failed to repay).

This project takes that giant record (called a **loan portfolio dataset**) and teaches you to:
1. Clean it (fix messy data),
2. Organize it in a database (SQL),
3. Analyze it in Python (find patterns),
4. Build dashboards in Power BI (show it visually to managers),
5. Write business insights (tell the story behind the numbers).

Think of it like being handed a messy Excel export from a real bank and being asked: **"Tell us who is likely to not pay us back, and why."**

### Why was it created?

In real lending companies, one of the biggest costs is **bad loans** — money given out that never comes back. If a company can predict *before* trouble starts which loans are risky, it can:
- Lend more carefully,
- Charge the right interest rate for the risk,
- Catch problem branches/officers early,
- Recover money faster.

This project simulates exactly that real-world need, using a fake (synthetic) but statistically realistic dataset, so you can practice the full job of a Data Analyst without touching confidential real customer data (real bank data is protected by law).

### What business problem does it solve?

**The core question:** *"Which loans are likely to default, and what patterns explain it?"*

Simple real-life analogy: Imagine you run a small chit fund (informal lending group) in your neighborhood. Some people always pay you back on time. Others disappear after taking money. Over time, you'd notice patterns: maybe people with unstable jobs are riskier, or people who already owe a lot of money elsewhere are riskier. This project does that same pattern-finding, but at the scale of 120,720 loans, using data instead of gut feeling.

### Who would use this project in a real company?

| Role | How they use this |
|---|---|
| **Data Analyst** | Cleans data, writes SQL queries, builds Power BI dashboards |
| **Risk Manager** | Uses default rate trends to tighten/loosen lending rules |
| **Branch Manager** | Checks their branch's performance vs other branches |
| **Collections Team** | Uses days-past-due and recovery data to prioritize follow-ups |
| **Senior Management / CXOs** | Look at dashboards to decide company strategy |
| **Credit Policy Team** | Uses credit score/DTI patterns to set approval rules |

**Summary of Section 1:** This project mimics a real NBFC's loan book. Your job as the analyst is to clean it, study it, and explain *why* some loans go bad — so the business can lend smarter.

---

## 2. Company Background

### The fictional company: FinEdge Capital

FinEdge Capital is a made-up Indian lending company used only for this project (it does not exist in real life — this avoids using real confidential bank data). It has:
- 25 branches across India (North, South, East, West, Central regions)
- 150 loan officers (6 per branch)
- 4 loan products: Personal Loan, Auto Loan, Business Loan, Gold Loan
- A loan book covering applications from **January 2023 to June 2026**

### What is an NBFC?

**NBFC = Non-Banking Financial Company.**

In simple words: it's a company that lends money and offers financial services, **but it is not a full bank**. It cannot accept regular savings deposits the way a bank does (like SBI or HDFC Bank), but it can give loans, leases, and other credit products.

Real-life examples of NBFCs in India: Bajaj Finance, Muthoot Finance, Shriram Finance, HDB Financial Services.

**Simple analogy:** Think of a bank as a full grocery store — it sells everything (savings accounts, loans, deposits, cards). An NBFC is more like a specialty store — it focuses mainly on lending, often to customers a big bank might consider too "small" or "risky" (self-employed individuals, gold-loan borrowers, small business owners).

### Why does an NBFC need this analysis?

NBFCs usually lend to a slightly riskier customer base than traditional banks (more self-employed people, less formal paperwork, smaller ticket sizes). Because of this:
- Their default rates are naturally a bit higher.
- They must watch credit risk **very closely** — one bad batch of loans can hurt profits badly.
- Regulators (like the RBI — Reserve Bank of India) require NBFCs to track and report on Non-Performing Assets (NPAs) — loans that have gone bad.

**Real example:** If FinEdge gives out ₹100 crore in Personal Loans and 8% default, that's ₹8 crore potentially lost. Understanding *which* branches, officers, or customer types cause that 8% helps FinEdge fix the problem before it grows.

**Summary of Section 2:** FinEdge Capital is a pretend NBFC — a lending-focused financial company. NBFCs need risk analysis because their business model depends heavily on correctly pricing and managing loan default risk.

---

## 3. Dataset Explanation

### What is the dataset?

The dataset (`finedge_loan_portfolio.csv`) has **120,720 rows and 53 columns**. It's a synthetic (fake, computer-generated) dataset — but it was built with real statistical logic baked in, so your analysis produces real, meaningful patterns, not just random noise.

**Grain of the data** (a very important data concept): "Grain" means *what does one single row represent?* Here, **one row = one loan application/account**. This matters because it tells you what level you can analyze at (per loan) vs what needs aggregation (per branch, per officer, per month).

### Why does it have so many rows and columns?

- **Rows (120,720):** A real NBFC processes thousands of loans over multiple years. This scale makes your analysis statistically meaningful — with only 100 rows, patterns could just be luck. With 120,720 rows, patterns are trustworthy.
- **Columns (53):** A single loan actually touches many types of information — who the person is, what they wanted the money for, how the company evaluated them, what happened after disbursal, and how it ended. 53 columns capture all these angles.

### What does each major section of the dataset represent?

Think of the 53 columns in 8 logical groups:

| Group | What it covers | Example columns |
|---|---|---|
| 1. Applicant identity | Who is the borrower | applicant_id, customer_name, gender, age |
| 2. Applicant financial profile | Their money situation | annual_income, employment_type, years_with_employer |
| 3. Location | Where they are | city, state, pincode, region |
| 4. Branch & staff | Who at FinEdge handled it | branch_id, loan_officer_id |
| 5. Loan terms | What was borrowed | loan_amount, interest_rate, tenure_months, emi_amount |
| 6. Risk indicators | How risky the loan looked | credit_score, debt_to_income_ratio, risk_category |
| 7. Lifecycle dates & status | What happened over time | application_date, disbursal_date, loan_status |
| 8. Outcome | Did it go bad, was it recovered | default_flag, days_past_due, recovery_amount |

**Real-life analogy:** Imagine filling a loan application form at a branch. Section 1–3 is basically the personal-details page. Section 4 is "who is processing my file." Section 5 is "what am I borrowing." Section 6 is the internal risk-check the bank does behind the scenes. Section 7–8 is the story of what happens *after* you get the money — do you pay on time, or not.

**Summary of Section 3:** The dataset is one big flat table (like a giant Excel export from a bank's system) where each row is a loan, and the 53 columns describe the borrower, the loan, the risk, and the outcome.

---

## 4. Column Explanation (all 53 columns)

For each column: **meaning → why it matters → business use → real-life example.**

### Group 1 — Applicant Identity

| Column | Meaning | Why important | Business use | Example |
|---|---|---|---|---|
| `loan_id` | Unique code for each loan (LNxxxxxx) | Needed to identify one exact loan record | Primary key — used to join/track a specific loan everywhere | LN157322 is one specific personal loan |
| `applicant_id` | Unique code for each borrower (APxxxxxx) | One person can take multiple loans over time | Used to see a customer's full loan history / repeat borrowing | AP257322 might have taken 2 loans in 3 years |
| `customer_name` | Borrower's full name | Human-readable identity | Customer service, KYC, communication | "Sunil Mukherjee" |
| `gender` | Male/Female | Used for fairness/segment analysis | Check if lending or default patterns differ by gender (for policy fairness checks) | Helps confirm no gender-based bias in approvals |
| `date_of_birth` | Borrower's birth date | Used to calculate age, check eligibility (must be 21+) | Age-based risk segmentation | 1998-10-02 |
| `age` | Age in years at time of data | Younger vs older borrowers behave differently | Age-band risk analysis | A 23-year-old vs 58-year-old borrower profile |
| `marital_status` | Married/Single/Divorced/Widowed | Correlates with financial stability in some markets | Segment-level risk study | Married applicants may have dual income support |
| `education` | Highest qualification | Indicates earning potential | Used with income/employment to assess repayment capacity | Post Graduate vs Graduate |
| `occupation` | Specific job/role | Detailed employment info | Fine-grained risk modeling | "Chartered Accountant" |
| `employment_type` | Salaried / Self-Employed Professional / Self-Employed Business / Business Owner | **Key risk driver** — self-employed income is less predictable | Sets underwriting rules (income proof needed, risk premium) | Business Owners may show more income volatility |
| `employer_name` | Employer name (or "Self Employed") | Shows job stability, reputation of employer | Bigger, stable employers = lower risk | "Tata Motors", "Accenture" |
| `years_with_employer` | Tenure at job/business | Job stability signal | Longer tenure often = lower default risk | 7.8 years |
| `annual_income` | Yearly declared income (₹) | Core affordability check | Determines loan eligibility and amount | ₹816,000/year |
| `monthly_income` | Monthly declared income (₹) | Used for EMI affordability (EMI should be a safe % of income) | Directly used in Debt-to-Income ratio | ₹43,900/month |

**Real-life example:** A bank clerk checks: "This applicant earns ₹43,900/month, works as a Business Owner, has been in business 7.8 years." That single glance already forms a rough risk opinion — this is exactly what these columns encode as data.

### Group 2 — Location

| Column | Meaning | Why important | Business use | Example |
|---|---|---|---|---|
| `city` | Applicant's city | Geographic risk & market analysis | City-wise portfolio performance | Gurugram |
| `state` | Applicant's state | State-level regulation/economic differences | Regional strategy | Haryana |
| `pincode` | Postal code | Fine-grained location analysis | Hyperlocal marketing/risk | 140909 |

**Example:** FinEdge might notice loans in one city have higher bounce rates due to local economic slowdown — location data helps spot this.

### Group 3 — Branch & Staff

| Column | Meaning | Why important | Business use | Example |
|---|---|---|---|---|
| `branch_id` | Branch code (BRxxx, 25 branches) | Identifies which branch handled the loan | Branch performance comparison | BR013 |
| `branch_name` | Branch's name | Human-readable branch identity | Reporting | "Gurugram City Branch" |
| `region` | North/South/East/West/Central | Groups branches for regional reporting | Regional risk & growth strategy | North |
| `loan_officer_id` | Officer code (OFFxxxx, 150 officers) | Identifies who processed/approved the loan | Officer performance tracking | OFF0073 |
| `loan_officer_name` | Officer's name | Human-readable | HR/performance reviews | "Vivaan Kulkarni" |

**Real-life example:** If Branch BR003 consistently shows high defaults across many officers, that points to a **branch-level** problem (maybe weak local underwriting culture, or a tough local economy) — not just one bad employee. This dataset intentionally has 4 such branches baked in (explained more in Section 6).

### Group 4 — Loan Terms

| Column | Meaning | Why important | Business use | Example |
|---|---|---|---|---|
| `loan_product` | Personal Loan / Auto Loan / Business Loan / Gold Loan | Different products carry different risk & collateral | Product-level risk pricing | "Personal Loan" |
| `loan_purpose` | Why the loan was taken | Purpose can hint at urgency/risk (e.g. medical emergency vs travel) | Purpose-based risk study | "Medical Emergency" |
| `loan_amount` | Amount requested (₹) | The size of exposure | Portfolio size, risk exposure | ₹552,000 |
| `sanctioned_amount` | Amount approved (₹) | May differ from requested (bank may approve less) | Shows underwriting caution | ₹542,000 |
| `disbursed_amount` | Amount actually paid out (₹) | The real money at risk | Used in loss calculations | ₹539,000 |
| `interest_rate` | Annual interest rate (%) | Price of the loan; reflects risk pricing | Revenue and risk-based pricing | 18.32% |
| `tenure_months` | Loan duration in months | Longer tenure = more time for something to go wrong | Risk & cash-flow planning | 48 months |
| `emi_amount` | Monthly installment (₹) | What the customer pays monthly | Affordability checks, EMI-to-income tracking | ₹15,923 |
| `processing_fee` | One-time fee (₹) | Extra revenue for the company | Revenue tracking | ₹6,594 |

**Real-life example:** Two customers ask for ₹5 lakh. One gets approved for the full amount; another only gets ₹4.5 lakh sanctioned because the bank judged them slightly riskier — that's exactly what `loan_amount` vs `sanctioned_amount` capture.

### Group 5 — Risk Indicators

| Column | Meaning | Why important | Business use | Example |
|---|---|---|---|---|
| `credit_score` | Bureau score, 300–900 (like a CIBIL score in India) | **Very strong predictor of default** | Approval decision, interest rate setting | 697 |
| `debt_to_income_ratio` (DTI) | (existing EMI + new EMI) ÷ monthly income | **Key risk driver** — shows how stretched the borrower already is | Affordability & approval decisions | 0.756 means EMIs eat 75.6% of income — very risky |
| `existing_loans_count` | Number of loans the person already has | More existing debt = more risk | Cross-check total exposure | 2 |
| `existing_emi_obligations` | Total of existing EMIs (₹) | Used to calculate DTI | Affordability check | ₹17,250 |
| `collateral_type` | None / Vehicle Hypothecation / Gold Ornaments | Secured loans are safer for the lender | Determines Loss Given Default assumptions | "Gold Ornaments" |
| `collateral_value` | Value of pledged item (₹) | Shows how much can be recovered if default happens | Recovery estimation | ₹0 if unsecured |
| `co_applicant_flag` | Yes/No — is there a co-borrower | Co-applicants add repayment security | Risk mitigation factor | "Yes" |

**Real-life example:** A credit score of 900 is like a straight-A student — very trustworthy. A score around 500 means the lender should be cautious, maybe charge higher interest or ask for collateral.

### Group 6 — Lifecycle Dates & Status

| Column | Meaning | Why important | Business use | Example |
|---|---|---|---|---|
| `application_date` | When the loan was applied for | Start of loan lifecycle | Turnaround-time analysis | 21 Sep 2025 |
| `approval_date` | When it was approved | Measures processing speed | Operational efficiency (approval TAT) | 09/27/2025 |
| `disbursal_date` | When money was actually given | Start of the repayment clock | Vintage/cohort analysis | 01-10-2025 |
| `loan_status` | Active / Closed / Default / Written-Off | Current state of the loan | Portfolio health snapshot | "Default" |

**Note:** These three date columns are **intentionally messy** — stored in 5 different formats (this is explained fully in Section 6, Data Quality Report). This forces you to practice real-world data cleaning.

### Group 7 — Outcome / Default Tracking

| Column | Meaning | Why important | Business use | Example |
|---|---|---|---|---|
| `default_flag` | 1 if status is Default/Written-Off, else 0 | **The target variable** — what we are ultimately trying to predict/explain | Core KPI: default rate | 1 |
| `days_past_due` (DPD) | How many days payment is overdue | Shows severity of delinquency | Collections prioritization | 228 days overdue = very serious |
| `npa_flag` | Yes if DPD ≥ 90 days | Standard regulatory definition of a bad loan | Regulatory reporting (RBI norms) | "Yes" |
| `recovery_amount` | Amount recovered after default (₹) | Shows how much loss was actually realized | Loss calculation, collections performance | ₹95,223 recovered out of a bigger default |
| `payment_history_score` | Internal behavior score, 100–900 | FinEdge's own scoring of repayment behavior (not bureau) | Early warning signal | 446 (weak) vs 900 (excellent) |
| `bounce_count` | Number of EMI payment bounces (failed auto-debits) | Early sign of financial stress | Early-warning/collections trigger | 5 bounces = red flag |
| `risk_category` | Low / Medium / High / Very High | Simplified risk label derived from underlying probability | Quick filtering for management/dashboards | "Low" |
| `customer_segment` | Mass Market / Mass Affluent / Premium | Income-based customer tiering | Marketing, pricing, prioritization | "Mass Market" |
| `is_fraud_suspected` | Yes/No | Flags potential fraud | Fraud investigation trigger | ~0.42% flagged "Yes" |
| `kyc_verified` | Yes/No | Whether identity was properly verified | Compliance/regulatory requirement | "Yes" |
| `channel` | Branch Walk-in / Digital App / DSA Referral / Tele-calling / Corporate Tie-up | How the loan was sourced | Channel performance & cost-effectiveness | "Digital App" |

**Real-life example:** `days_past_due` = 90+ is the exact global standard banks use to call a loan an **NPA (Non-Performing Asset)** — this is not made up, it's real RBI/international banking terminology baked into this dataset.

**Summary of Section 4:** Every column either describes **who the borrower is**, **what the loan looks like**, **how risky it seemed at approval**, or **what actually happened afterward**. The most powerful columns for predicting trouble are `credit_score`, `debt_to_income_ratio`, `employment_type`, `branch_id`, and `loan_officer_id`.

---

## 5. Business Process — The Complete Loan Lifecycle

Here is the journey of one loan, step-by-step, connected to the actual columns:

```
Customer → Loan Application → Approval → EMI Payment → Delinquency → Default → Recovery → Loan Closure
```

| Stage | What happens | Key columns involved |
|---|---|---|
| **1. Customer** | A person (applicant) with a certain income, job, and credit history walks in or applies online | applicant_id, employment_type, credit_score, channel |
| **2. Loan Application** | They request a loan amount for a purpose | application_date, loan_amount, loan_purpose |
| **3. Approval** | FinEdge checks credit score, DTI, income — decides how much to sanction | approval_date, sanctioned_amount, credit_score, debt_to_income_ratio |
| **4. Disbursal** | Approved money is transferred | disbursal_date, disbursed_amount |
| **5. EMI Payment** | Customer pays monthly installments | emi_amount, bounce_count |
| **6. Delinquency** | Customer starts missing payments | days_past_due, payment_history_score |
| **7. Default / Write-Off** | Payment stops for 90+ days (NPA) or the loan is written off as a loss | npa_flag, default_flag, loan_status = "Default"/"Written-Off" |
| **8. Recovery** | Collections team recovers whatever is possible (selling collateral, settlements, legal action) | recovery_amount, collateral_value |
| **9. Loan Closure** | Loan ends — either fully repaid ("Closed") or resolved after default | loan_status = "Closed" |

**Real-life analogy:** Think of lending money to a friend for a business.
1. They ask you for ₹50,000 (**application**).
2. You check if they're trustworthy, maybe ask for something as security (**approval**).
3. You give them the money (**disbursal**).
4. They pay you back ₹5,000 every month (**EMI**).
5. One month they're late (**delinquency**).
6. After months of no payment, you accept they might not pay (**default**).
7. You take back whatever security they gave you, or negotiate a partial payment (**recovery**).
8. The matter is finally settled (**closure**).

FinEdge does this at the scale of 120,720 loans instead of one friend.

**Summary of Section 5:** A loan is not a one-time event — it's a lifecycle with multiple stages, and each stage generates data. Understanding this flow is what lets you connect *why* a column exists to *what business moment* it represents.

---

## 6. Documentation — Understanding Every File

### `README.md`
**What it is:** The "front door" of the project. It's the first file anyone opens.
**Why it exists:** In any real company project (or GitHub repository), the README explains: what this is, why it was built, what files exist, and how to use them — without needing to read all the code.
**Real company use:** When a new analyst joins the risk team, they read the README first to understand the dataset before touching anything.

**Key facts this README tells us:**
- Overall default rate is baked in at **~5.3%**, with a project narrative describing a rise from 4.1% to 7.8% over time (a worsening trend you're expected to discover in your cohort analysis).
- **4 branches (BR003, BR009, BR014, BR022)** were deliberately made structurally riskier — a "problem branch" pattern for you to find.
- **Credit score is a strong predictor**: the worst score group defaults at ~9.3%, the best group at ~2.5%.
- **Personal Loan and Business Loan are riskier** than Auto Loan and Gold Loan (because the latter two are secured by collateral).
- **150 loan officers** each have a hidden "skill multiplier" — some officers are simply better at screening applicants, creating real (not random) officer-level variance.
- **~0.42% of loans are fraud-flagged**, often linked to a loan-to-income ratio above 18x.

### `01_Data_Dictionary_and_Quality_Report.md`
**What it is:** A column-by-column explanation of the dataset (Section 4 above is built from this), plus a report on data problems and business assumptions.
**Why it exists:** No analyst should ever start working on data blindly. In real companies, the Data Dictionary is the map that says what each field means, and the Data Quality Report tells you what's broken and needs fixing before analysis.
**Real company use:** Data engineers and analysts refer to this before writing any SQL/Python — it prevents wrong assumptions (e.g., mistaking `loan_amount` for `disbursed_amount`).

**Key data quality issues documented (and why they exist):**

| Issue | Magnitude | Simulates |
|---|---|---|
| Missing values (10 columns like income, credit_score) | 3.2%–4.9% each | Incomplete system sync, applicants not disclosing info |
| Duplicate rows | ~0.6% (708 rows) | A batch resync/export error |
| Mixed date formats (application/approval/disbursal dates) | 5 formats mixed | Data coming from multiple systems (core banking + app + partner feed) |
| Outliers in income/loan amount | ~0.15–0.2% | Data entry mistakes / unverified self-declared income |
| Fraud flags | ~0.42% | Realistic rare fraud incidence |
| Class imbalance in `default_flag` | ~5.3% positive | Real lending books always have far more good loans than bad ones |

**Recommended cleaning order (given in the file):** deduplicate → standardize dates → impute missing numeric values (by employment_type + branch median) → cap outliers at the 99.5th percentile → check that branch_id/loan_officer_id values are valid.

**Business assumptions worth knowing (hidden logic):**
1. Portfolio covers loans from **Jan 2023 to Jun 2026** (report date assumed 30 Jun 2026).
2. `default_flag = 1` only when status is "Default" or "Written-Off" (matches the 90+ DPD no-cure standard).
3. **Loss Given Default (LGD)** assumption (not stored as a column, you must apply it yourself): 60% loss assumed for unsecured loans (Personal/Business), 35% for secured loans (Auto/Gold) — because secured loans can recover value through collateral.
4. Branch risk (BR003/BR009/BR014/BR022) and officer skill differences are **intentional, not noise** — a real pattern for you to detect statistically.
5. ~0.2% of income values are unrealistic outliers by design, mimicking unverified self-declared income (common issue with self-employed applicants).
6. All money values are in plain Rupees (not lakhs/crores) so SQL/BI tools can directly sum/average them without unit conversion.

### `02_ER_Diagram_StarSchema_and_SQL_DDL.md`

**What it is:** This file has three parts:
1. An **ER Diagram** (Entity-Relationship Diagram) of the raw data.
2. A **Star Schema** design (how to reorganize the data for Power BI).
3. **SQL DDL** (Data Definition Language — the `CREATE TABLE` code) for both the raw staging table and the final star schema.

**What is an ER Diagram?**
It's a visual map showing what "things" (entities) exist in your data and how they relate. Here, the entities are: Applicant, Branch, Loan Officer, Product, Loan, and Default Event. For example: "One Applicant can apply for many Loans" (one-to-many relationship) — shown as `APPLICANT ||--o{ LOAN`.

**What is a Star Schema, and why is it needed for Power BI?**
The raw CSV is a **flat table** — everything mixed into one wide sheet. This is fine for a first look, but for a fast, professional Power BI dashboard, data should be split into:
- **1 Fact table** (`fact_loans`) — contains the *measurable numeric events* (loan amount, EMI, default flag, DPD, recovery amount).
- **5 Dimension tables** (`dim_branch`, `dim_product`, `dim_officer`, `dim_applicant`, `dim_date`) — contain the *descriptive labels* you slice/filter by (branch name, product type, officer name, applicant details, calendar attributes).

**Real-life analogy:** Imagine a shop's daily sales register (the fact — how much was sold, when) versus a separate product catalog (the dimension — what each product is called, its category). Keeping them separate makes reporting faster and prevents repeating the same product name thousands of times.

**Why this matters for performance:** With 120,720 rows, a flat wide table repeats branch name, region, product name, etc. on every single row — wasteful. A star schema stores each branch's details *once* in `dim_branch`, and `fact_loans` just references it with a small key number. This makes Power BI faster and its time-based calculations (like "default rate this year vs last year") work correctly.

**What is SQL DDL?**
DDL = Data Definition Language — the SQL commands that *create the structure* of database tables (as opposed to DML, which reads/inserts/updates data). The `CREATE TABLE stg_loans_raw (...)` command builds an empty table shaped exactly like the CSV, ready to be loaded (this is the "staging" step — raw data landing zone before cleaning). The second set of `CREATE TABLE` statements builds the clean star schema tables.

**Real company use:** A Data Engineer would run this DDL first to create tables in a database like PostgreSQL/SQL Server, then load the CSV into `stg_loans_raw`, clean it, and populate the star schema tables — exactly the order suggested in the README's "Suggested next steps."

### `generate_dataset.py`
**What it is:** The actual Python program that created the dataset from scratch using randomness plus statistical rules.
**Why it exists:** This is the "recipe" behind the data. It proves the dataset isn't just random junk — it has a real mathematical model behind default risk. For example, this script contains a formula like:

```
logit = -3.85 + 0.55*credit_score_effect + 0.55*DTI_effect + 0.5*income_effect
        + 0.6*branch_effect + 0.5*product_effect + 0.4*employment_effect
        + 0.5*officer_effect + 0.3*tenure_effect
default_probability = 1 / (1 + e^-logit)
```

This is a **logistic regression formula** (a well-known statistics technique for predicting yes/no outcomes, here "will this loan default or not"). In plain English: it says "the chance a loan defaults goes up if the credit score is bad, the debt-to-income ratio is high, the branch is a risky one, the officer is less careful, etc." — each factor pushes the risk up or down, and the formula combines them into one final probability.

There's also fraud logic: a loan is more likely flagged as fraud-suspected if `loan_amount / monthly_income > 18` (someone asking for a loan 18 times their monthly income is suspicious), plus a small random chance for any loan.

**Real company use:** In a real setting, this script would be like a company's internal risk model or simulation engine used for stress-testing ("what happens to our default rate if the economy worsens?"). For a learner, re-running it with different settings lets you create new scenarios (e.g., a recession scenario with higher default rates) to practice analysis on.

**Summary of Section 6:** Every file has a specific job — README orients you, the Data Dictionary/Quality Report tells you what the columns mean and what's broken, the ER/Star Schema/DDL file tells you how to structure the data for databases and BI tools, and the generator script proves the patterns in the data are real and intentional, not random.

---

## 7. SQL Part

### What analysis should be done?

SQL (Structured Query Language) is used to ask direct, precise questions of the data stored in a database. After loading and cleaning the data into the star schema, typical SQL analysis includes:

| Analysis | Example SQL idea |
|---|---|
| Overall default rate | `SELECT AVG(default_flag) FROM fact_loans;` |
| Default rate by branch | `GROUP BY branch_id` — to find BR003, BR009, BR014, BR022 |
| Default rate by product | `GROUP BY loan_product` — Personal/Business vs Auto/Gold |
| Default rate by credit score band | `CASE WHEN credit_score < 600 THEN 'Poor' ... END` |
| Officer-level performance | `GROUP BY loan_officer_id`, compare default rates |
| Monthly/quarterly disbursal trend | `GROUP BY DATE_TRUNC('month', disbursal_date)` |
| Loan approval turnaround time | `approval_date - application_date` |
| NPA portfolio value | `SUM(disbursed_amount) WHERE npa_flag = 'Yes'` |
| Recovery effectiveness | `SUM(recovery_amount) / SUM(disbursed_amount) WHERE default_flag = 1` |
| High-risk customer segments | `GROUP BY customer_segment, risk_category` |

### Why is it done?

SQL is the fastest, most reliable way to summarize millions of rows into clear numbers ("what is our default rate this quarter?"). Every dashboard and every business decision ultimately traces back to a SQL query running behind the scenes.

### Which business questions will SQL answer?

- "Which branches have default rates above the company average?" → Finds BR003/BR009/BR014/BR022.
- "Is Personal Loan riskier than Auto Loan?" → Confirms product-level risk difference.
- "Which loan officers consistently show poor portfolios?" → Flags officers needing training or review.
- "Has our default rate worsened over the last 3 years?" → Confirms the 4.1% → 7.8% trend mentioned in the README.
- "How much money have we recovered from defaulted loans?" → Measures collections effectiveness.
- "Are digitally-sourced loans (Digital App/DSA) riskier than branch walk-ins?" → Channel risk comparison.

**Summary of Section 7:** SQL is used to slice the huge dataset into clear, grouped summaries (by branch, product, officer, time, segment) that directly answer "where is our risk coming from?"

---

## 8. Python Part

### What does EDA mean?

**EDA = Exploratory Data Analysis.** In simple words: before building any fancy model, you first *look* at the data carefully — check distributions, spot patterns, find outliers, and understand relationships between columns. It's like a doctor doing an initial check-up before deciding on treatment.

### What charts should be created?

| Chart | What it shows | Why it matters |
|---|---|---|
| Histogram of `credit_score` | Distribution of borrower credit quality | Shows if most borrowers are decent-risk or risky |
| Histogram of `debt_to_income_ratio` | Distribution of financial stress | Spots how many borrowers are over-leveraged |
| Bar chart: default rate by `loan_product` | Compares risk across products | Confirms Personal/Business Loan riskier than Auto/Gold |
| Bar chart: default rate by `branch_id` | Compares branch risk | Surfaces the 4 problem branches |
| Line chart: default rate over time (monthly/quarterly) | Trend of portfolio health | Shows if risk is rising or falling (the 4.1%→7.8% story) |
| Box plot: `monthly_income` by `employment_type` | Income spread and outliers per job type | Flags unrealistic income outliers |
| Correlation heatmap (credit_score, DTI, income, default_flag) | Shows which numeric factors move together | Confirms credit_score & DTI are strong default predictors |
| Scatter plot: `credit_score` vs `default_flag` (or binned default rate) | Visualizes the monotonic relationship | Confirms lower score = higher default risk |
| Pie/bar chart: `loan_status` breakdown | Active/Closed/Default/Written-Off proportions | Quick portfolio health snapshot |
| Bar chart: fraud-suspected rate by loan-to-income band | Shows fraud concentration | Supports fraud-detection policy |

### Why each chart is important

Charts turn thousands of numbers into a shape the human eye can instantly understand. A manager won't read 120,720 rows, but they will glance at a bar chart and immediately see "branch BR003's bar is much taller than the rest — something's wrong there."

**Statistical tests worth mentioning** (referenced in the README as validation tools):
- **Chi-square test:** Checks if two categorical variables (e.g., loan_product and default_flag) are related.
- **T-test:** Compares the average of a numeric variable (e.g., credit_score) between two groups (defaulters vs non-defaulters).
- **Logistic regression:** Models the probability of default based on multiple factors at once — mirrors the exact formula used to generate this dataset, so your model's coefficients should sensibly match the baked-in ground truths.

**Summary of Section 8:** EDA is your "getting to know the data" phase in Python — using charts and simple statistical tests to confirm what factors truly drive default risk, before building anything more advanced.

---

## 9. Power BI Part

### Which dashboards should be built?

| Dashboard | Purpose |
|---|---|
| **Portfolio Overview Dashboard** | High-level health check: total loans, total disbursed amount, overall default rate, NPA amount |
| **Branch Performance Dashboard** | Compare branches on default rate, disbursal volume, recovery rate |
| **Product Risk Dashboard** | Compare Personal/Auto/Business/Gold Loan performance |
| **Officer Performance Dashboard** | Track each loan officer's book size and default rate |
| **Risk & Credit Score Dashboard** | Show default rate by credit score band, DTI band |
| **Collections & Recovery Dashboard** | Track days-past-due buckets, recovery amounts, write-offs |
| **Trend Dashboard** | Default rate and disbursal volume over months/quarters/years |

### Why does management need them?

Senior managers don't have time to run SQL queries or read Python notebooks. A well-built Power BI dashboard lets them **click, filter, and see the story instantly** — e.g., filter by "North Region" and immediately see if the North's default rate is higher than other regions.

### Which KPIs should be displayed?

| KPI | Formula (concept) | Why it matters |
|---|---|---|
| Overall Default Rate | defaulted loans ÷ total loans | Core health metric |
| Gross NPA % | NPA loan value ÷ total disbursed value | Regulatory-style risk metric |
| Total Disbursed Amount | Sum of disbursed_amount | Business scale |
| Average Credit Score | Avg(credit_score) | Portfolio quality indicator |
| Average DTI | Avg(debt_to_income_ratio) | Borrower stress indicator |
| Recovery Rate | recovery_amount ÷ defaulted disbursed amount | Collections effectiveness |
| Approval Turnaround Time | approval_date − application_date | Operational efficiency |
| Branch-wise Default Rate | default_flag avg per branch | Identify problem branches |
| Officer-wise Default Rate | default_flag avg per officer | Identify underwriting quality issues |
| Fraud Rate | fraud-suspected loans ÷ total loans | Compliance/fraud monitoring |

**Summary of Section 9:** Power BI turns your SQL/Python findings into interactive, visual dashboards so that non-technical managers can make fast, informed decisions — tracking KPIs like default rate, NPA%, and recovery rate at a glance.

---

## 10. Business Insights

Here are the kinds of insights a good Data Analyst should extract from this exact dataset, with real examples:

1. **"Our overall default rate is around 5.3%, but it has been rising — from about 4.1% a couple of years ago to nearly 7.8% in recent cohorts."**
 → *Business action:* Investigate what changed in underwriting or the economy during that period.

2. **"Branches BR003, BR009, BR014, and BR022 show default rates well above the network average."**
 → *Business action:* Audit these branches' underwriting practices; consider retraining staff or tightening approval rules locally.

3. **"Borrowers in the lowest credit-score quintile default at ~9.3%, compared to ~2.5% for the top quintile."**
 → *Business action:* Consider raising the minimum credit score threshold, or charging risk-based higher interest for low-score approvals.

4. **"Personal Loans and Business Loans default more often than Auto Loans and Gold Loans."**
 → *Business action:* Since Auto/Gold Loans are secured by collateral, they're safer — FinEdge could grow these product lines more aggressively, or require more collateral/co-applicants for unsecured products.

5. **"Some loan officers consistently show higher default rates in their portfolios, even accounting for branch and product."**
 → *Business action:* This points to underwriting skill/diligence differences — an opportunity for officer training or stricter review of high-risk officer approvals.

6. **"About 0.42% of loans are fraud-suspected, and many of these have a loan amount far higher than the applicant's monthly income."**
 → *Business action:* Add an automated flag/hold for any application where loan amount exceeds ~18x monthly income for manual fraud review.

7. **"Digitally-sourced loans (Digital App/DSA Referral) may show different risk profiles compared to Branch Walk-ins."**
 → *Business action:* Adjust channel-specific underwriting rules or partner (DSA) quality checks.

**Summary of Section 10:** A great analyst doesn't just report numbers — they connect each number to a *specific action* the business can take (tighten a rule, train a branch, adjust pricing).

---

## 11. Recruiter Perspective — Why This Project is Valuable

### Why is this valuable for a Data Analyst portfolio?

Because it mirrors a **real, high-value industry use case** (credit risk analytics is one of the most in-demand analytics domains in India's BFSI — Banking, Financial Services, Insurance — sector), and it covers the **entire analytics pipeline**, not just one tool.

### Which skills does it demonstrate?

| Skill | Demonstrated by |
|---|---|
| Data cleaning | Handling missing values, duplicate rows, mixed date formats, outliers |
| Data modeling | Understanding/building a star schema (fact & dimension tables) |
| SQL | Writing grouped, filtered, joined queries for business questions |
| Python / EDA | Creating and interpreting charts and statistical tests |
| Statistics fundamentals | Chi-square, t-test, logistic regression, correlation |
| Business acumen | Translating numbers into real recommendations (NBFC/credit domain knowledge) |
| Dashboarding | Building KPI-driven Power BI reports for management |
| Domain knowledge | Understanding of NBFC lending lifecycle, NPA norms, risk categories |
| Storytelling | Turning a messy dataset into a clear narrative of "why defaults happen" |

This combination — technical tool skills **plus** financial-domain understanding **plus** business storytelling — is exactly what recruiters at banks, NBFCs, fintechs, and consulting firms look for in a Data Analyst.

**Summary of Section 11:** This project proves you can take messy raw data all the way to a decision-ready business dashboard — a complete, end-to-end skill set, not just isolated tool knowledge.

---

## 12. Interview Questions (with Answers)

### Beginner Level

**Q1. What is the grain of this dataset?**
A: One row represents one loan application/account.

**Q2. What does `default_flag = 1` mean in this dataset?**
A: It means the loan's status is "Default" or "Written-Off" — i.e., the borrower failed to repay as agreed.

**Q3. What is an NBFC?**
A: A Non-Banking Financial Company — a company that offers loans and financial services but cannot accept regular savings deposits like a bank.

**Q4. Name two data quality issues present in this dataset.**
A: Missing values in columns like income and credit_score, and inconsistent date formats across application_date, approval_date, and disbursal_date (also duplicate rows and outliers).

**Q5. What is the difference between `loan_amount`, `sanctioned_amount`, and `disbursed_amount`?**
A: `loan_amount` is what the customer requested, `sanctioned_amount` is what the company approved (may be less), and `disbursed_amount` is what was actually paid out.

### Intermediate Level

**Q6. Why do we convert a flat CSV into a star schema before loading into Power BI?**
A: To improve performance at scale, avoid repeating descriptive data on every row, and enable clean time-intelligence calculations (like year-over-year comparisons) via a proper `dim_date` table.

**Q7. How would you calculate the default rate by branch using SQL?**
A: Group by `branch_id` and calculate the average of `default_flag` (or count of defaulted loans divided by total loans) per branch.

**Q8. What is Debt-to-Income Ratio (DTI) and why is it important?**
A: DTI = (existing EMI + new EMI) ÷ monthly income. It shows how much of a borrower's income is already committed to loan payments. A high DTI means the borrower is financially stretched and more likely to default.

**Q9. Why might Personal Loans have a higher default rate than Gold Loans?**
A: Personal Loans are unsecured (no collateral), so the borrower has less at stake if they stop paying, and the lender can't easily recover the money. Gold Loans are secured by collateral (gold), which reduces both the borrower's incentive to default and the lender's ultimate loss.

**Q10. What does NPA mean, and how is it defined here?**
A: NPA = Non-Performing Asset — a loan where the borrower has stopped paying. In this dataset (and in standard banking practice), a loan is marked NPA when `days_past_due` reaches 90 or more.

### Advanced Level

**Q11. This dataset has a ~5.3% default rate — what data science challenge does this create, and how would you handle it?**
A: This is class imbalance — far fewer default cases than non-default cases. If building a predictive ML model, this can cause the model to be biased toward predicting "no default." Solutions include stratified sampling, class weighting, oversampling techniques (like SMOTE), or focusing on metrics like recall/precision/AUC instead of plain accuracy.

**Q12. How would you use logistic regression here, and what would the coefficients tell you?**
A: Logistic regression can model the probability of `default_flag = 1` based on predictors like credit_score, DTI, branch, product, and employment_type. Each coefficient tells you the direction and strength of that factor's effect on default risk — e.g., a negative coefficient on credit_score means higher scores reduce default odds.

**Q13. Four branches in this dataset are structurally riskier by design. How would you statistically confirm this isn't just random noise?**
A: Run a hypothesis test (e.g., chi-square test of independence between branch and default_flag, or compare each branch's default rate against the overall average with a proportions z-test / confidence interval) to check if the difference is statistically significant, not just due to chance.

**Q14. How would you estimate Expected Credit Loss (ECL) for this portfolio?**
A: ECL ≈ Probability of Default (PD) × Exposure at Default (EAD, roughly the disbursed/outstanding amount) × Loss Given Default (LGD). Per the project's own assumption, LGD is ~60% for unsecured products (Personal/Business Loan) and ~35% for secured products (Auto/Gold Loan), since collateral reduces the actual loss.

**Q15. Why is it important to standardize dates before doing any time-based analysis?**
A: Because `application_date`, `approval_date`, and `disbursal_date` are stored in 5 different formats. If not converted to one consistent date type, sorting, filtering, calculating durations (like turnaround time), or grouping by month/year will silently produce wrong results.

**Summary of Section 12:** These questions cover definitions (beginner), applied SQL/business logic (intermediate), and statistical/modeling reasoning (advanced) — exactly the range interviewers use to judge a Data Analyst candidate.

---

## 13. End-to-End Workflow

Here is how everything connects, start to finish, in a real company setting:

```
1. RAW DATA (CSV/XLSX)
   ↓  (Load into staging table: stg_loans_raw)
2. DATA CLEANING
   - Deduplicate
   - Standardize date formats
   - Impute missing values (by employment_type + branch median)
   - Cap outliers (99.5th percentile)
   ↓
3. DATA MODELING (Star Schema)
   - Build dim_branch, dim_product, dim_officer, dim_applicant, dim_date
   - Build fact_loans referencing all dimension keys
   ↓
4. SQL ANALYSIS
   - Default rate by branch, product, officer, time
   - Turnaround time, NPA value, recovery performance
   ↓
5. PYTHON / EDA & STATISTICS
   - Distributions, correlations, charts
   - Chi-square, t-test, logistic regression to validate risk drivers
   ↓
6. POWER BI DASHBOARDS
   - Portfolio Overview, Branch Performance, Product Risk,
     Officer Performance, Collections & Recovery, Trends
   - KPIs: Default Rate, NPA%, Recovery Rate, Avg Credit Score, Avg DTI
   ↓
7. BUSINESS INSIGHTS
   - Identify problem branches/officers/products
   - Quantify risk drivers (credit score, DTI, employment type)
   - Recommend concrete actions (policy changes, training, pricing)
   ↓
8. FINAL PRESENTATION
   - Summarize findings for management in simple business language
   - Back every claim with a chart, KPI, or SQL result
   - End with clear, actionable recommendations
```

**Real-life analogy:** This is exactly like a hospital's process — raw patient data (checkup) → organizing records (modeling) → running tests (SQL/Python analysis) → showing results to the doctor on a clean chart (Power BI) → the doctor explaining findings and next steps to the patient (business insights/presentation). Each step depends on the one before it being done correctly.

**Summary of Section 13:** The project is one continuous pipeline — messy raw data becomes clean structured data, which becomes SQL/Python findings, which become visual dashboards, which become real business decisions. Master each link in this chain, and you have mastered the full Data Analyst job.

---

## Final Note

You now have a complete mental map of this project:
- **What** the data is (a synthetic but realistic NBFC loan book),
- **Why** it exists (to practice real credit-risk analytics),
- **How** every column and file fits together,
- **What** the full lifecycle of a loan looks like,
- **How** to move from raw CSV → SQL → Python → Power BI → business insight → presentation.

If you'd like, I can next help you actually **write the cleaning script**, **build the SQL queries**, **create the Python EDA notebook**, or **design the Power BI dashboard** for this exact dataset — just tell me which one to start with.
