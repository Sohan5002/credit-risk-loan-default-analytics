"""
FinEdge Capital - Synthetic NBFC Loan Portfolio Generator
Generates a production-quality, intentionally messy 120,000+ row dataset
for the Credit Risk & Loan Default Analytics project.
"""
import numpy as np
import pandas as pd
import random
from datetime import datetime, timedelta

RNG = np.random.default_rng(42)
random.seed(42)

N = 120000

# ---------------------------------------------------------------------------
# 1. REFERENCE DATA
# ---------------------------------------------------------------------------
MALE_FIRST = ["Aarav","Vivaan","Aditya","Vihaan","Arjun","Reyansh","Sai","Krishna","Ishaan","Rohan",
    "Kabir","Aryan","Dhruv","Karan","Rahul","Amit","Vikram","Sanjay","Rajesh","Suresh",
    "Manoj","Anil","Deepak","Ashok","Ravi","Naveen","Praveen","Sunil","Gaurav","Nikhil",
    "Abhishek","Siddharth","Varun","Ajay","Vijay","Harish","Mahesh","Ramesh","Dinesh","Yash"]
FEMALE_FIRST = ["Saanvi","Ananya","Diya","Ira","Myra","Aadhya","Kiara","Riya","Ishita","Pooja",
    "Neha","Priya","Sneha","Anjali","Kavya","Divya","Shreya","Swati","Meera","Rekha",
    "Sunita","Anita","Kavita","Sangeeta","Nisha","Preeti","Ritu","Deepika","Simran","Manisha",
    "Aishwarya","Radhika","Vidya","Lakshmi","Geeta","Usha","Seema","Rashmi","Poonam","Komal"]
LAST_NAMES = ["Sharma","Verma","Gupta","Kumar","Singh","Patel","Reddy","Rao","Nair","Menon",
    "Iyer","Iyengar","Joshi","Mehta","Shah","Chopra","Malhotra","Kapoor","Agarwal","Bansal",
    "Mishra","Tiwari","Pandey","Dubey","Yadav","Chauhan","Rathore","Thakur","Naidu","Pillai",
    "Desai","Bhatt","Trivedi","Saxena","Srivastava","Sinha","Ghosh","Banerjee","Chatterjee","Mukherjee",
    "Das","Bose","Dutta","Kulkarni","Deshmukh","Jadhav","Patil","Gaikwad","More","Chavan"]

STATE_CITIES = {
    "Maharashtra": ["Mumbai","Pune","Nagpur","Nashik"],
    "Karnataka": ["Bengaluru","Mysuru","Hubli"],
    "Delhi": ["New Delhi","Dwarka","Rohini"],
    "Tamil Nadu": ["Chennai","Coimbatore","Madurai"],
    "Telangana": ["Hyderabad","Warangal"],
    "Gujarat": ["Ahmedabad","Surat","Vadodara"],
    "West Bengal": ["Kolkata","Howrah"],
    "Rajasthan": ["Jaipur","Jodhpur","Udaipur"],
    "Uttar Pradesh": ["Lucknow","Kanpur","Noida","Ghaziabad"],
    "Punjab": ["Ludhiana","Amritsar","Chandigarh"],
    "Madhya Pradesh": ["Bhopal","Indore","Gwalior"],
    "Kerala": ["Kochi","Thiruvananthapuram"],
    "Haryana": ["Gurugram","Faridabad"],
    "Bihar": ["Patna"],
    "Andhra Pradesh": ["Visakhapatnam","Vijayawada"],
}
REGION_MAP = {
    "Maharashtra":"West","Gujarat":"West","Rajasthan":"North","Karnataka":"South","Tamil Nadu":"South",
    "Telangana":"South","Andhra Pradesh":"South","Kerala":"South","Delhi":"North","Uttar Pradesh":"North",
    "Punjab":"North","Haryana":"North","Madhya Pradesh":"Central","West Bengal":"East","Bihar":"East",
}

# 25 branches spread across states, each with a baked-in risk multiplier
BRANCH_STATES = list(STATE_CITIES.keys())
branches = []
for i in range(1, 26):
    state = BRANCH_STATES[(i - 1) % len(BRANCH_STATES)]
    city = STATE_CITIES[state][(i - 1) % len(STATE_CITIES[state])]
    # 4 deliberately "high risk" branches (as required by the project narrative)
    risk_mult = 1.9 if i in (3, 9, 14, 22) else round(RNG.uniform(0.8, 1.3), 2)
    branches.append({
        "branch_id": f"BR{i:03d}",
        "branch_name": f"{city} {'Main' if i % 5 == 0 else 'City'} Branch",
        "city": city, "state": state, "region": REGION_MAP[state],
        "branch_risk_mult": risk_mult,
    })
branch_df = pd.DataFrame(branches)

# ~150 loan officers, 6 per branch, each with a performance/skill multiplier
officers = []
oid = 1
for b in branches:
    for _ in range(6):
        skill = round(RNG.uniform(0.7, 1.4), 2)  # <1 = better than average (fewer defaults)
        gname = random.choice(MALE_FIRST + FEMALE_FIRST)
        lname = random.choice(LAST_NAMES)
        officers.append({
            "loan_officer_id": f"OFF{oid:04d}",
            "loan_officer_name": f"{gname} {lname}",
            "branch_id": b["branch_id"],
            "officer_skill_mult": skill,
        })
        oid += 1
officer_df = pd.DataFrame(officers)

PRODUCTS = {
    "Personal Loan": {"rate": (13, 22), "tenure": (12, 60), "risk": 1.5, "secured": False},
    "Auto Loan": {"rate": (9, 14), "tenure": (12, 84), "risk": 0.8, "secured": True},
    "Business Loan": {"rate": (12, 19), "tenure": (12, 72), "risk": 1.3, "secured": False},
    "Gold Loan": {"rate": (7, 12), "tenure": (6, 36), "risk": 0.5, "secured": True},
}
PRODUCT_NAMES = list(PRODUCTS.keys())
LOAN_PURPOSES = {
    "Personal Loan": ["Medical Emergency","Wedding Expenses","Home Renovation","Travel","Debt Consolidation","Education"],
    "Auto Loan": ["New Car Purchase","Used Car Purchase","Two-Wheeler Purchase"],
    "Business Loan": ["Working Capital","Equipment Purchase","Business Expansion","Inventory Financing"],
    "Gold Loan": ["Agricultural Needs","Emergency Cash Need","Business Working Capital"],
}
EMPLOYMENT_TYPES = ["Salaried","Self-Employed Professional","Self-Employed Business","Business Owner"]
EMPLOYMENT_RISK = {"Salaried": 0.8, "Self-Employed Professional": 1.1, "Self-Employed Business": 1.4, "Business Owner": 1.3}
EDUCATION = ["High School","Graduate","Post Graduate","Professional Degree","Diploma"]
OCCUPATIONS_BY_EMP = {
    "Salaried": ["Software Engineer","Bank Employee","Government Employee","Teacher","Accountant","Sales Executive","Manager","Nurse","Civil Engineer"],
    "Self-Employed Professional": ["Doctor","Chartered Accountant","Lawyer","Architect","Consultant"],
    "Self-Employed Business": ["Shop Owner","Trader","Contractor","Freelancer"],
    "Business Owner": ["Manufacturing Business Owner","Retail Business Owner","Restaurant Owner","Trading Company Owner"],
}
EMPLOYERS = ["Infosys Ltd","TCS","Wipro","HDFC Bank","ICICI Bank","State Bank of India","Reliance Industries",
    "Tata Motors","Mahindra & Mahindra","L&T","Self Employed","Government of India","Adani Group",
    "Bajaj Auto","Hindustan Unilever","Local Business","Own Enterprise","Cognizant","Accenture","HCL Technologies"]
CHANNELS = ["Branch Walk-in","Digital App","DSA Referral","Tele-calling","Corporate Tie-up"]
COLLATERAL_TYPES = {"Auto Loan": "Vehicle Hypothecation", "Gold Loan": "Gold Ornaments",
                     "Business Loan": "None", "Personal Loan": "None"}

# ---------------------------------------------------------------------------
# 2. CORE GENERATION
# ---------------------------------------------------------------------------
gender = RNG.choice(["Male", "Female"], size=N, p=[0.63, 0.37])
first_names = np.where(gender == "Male",
                        RNG.choice(MALE_FIRST, size=N),
                        RNG.choice(FEMALE_FIRST, size=N))
last_names = RNG.choice(LAST_NAMES, size=N)
customer_name = [f"{f} {l}" for f, l in zip(first_names, last_names)]

age = RNG.integers(21, 65, size=N)
dob_year = 2026 - age
dob = [datetime(int(y), random.randint(1, 12), random.randint(1, 28)) for y in dob_year]

marital_status = RNG.choice(["Married", "Single", "Divorced", "Widowed"], size=N, p=[0.58, 0.32, 0.07, 0.03])
education = RNG.choice(EDUCATION, size=N, p=[0.12, 0.42, 0.28, 0.13, 0.05])
employment_type = RNG.choice(EMPLOYMENT_TYPES, size=N, p=[0.55, 0.15, 0.20, 0.10])
occupation = [random.choice(OCCUPATIONS_BY_EMP[e]) for e in employment_type]
employer_name = [random.choice(EMPLOYERS) if e == "Salaried" else "Self Employed" for e in employment_type]
years_with_employer = np.clip(RNG.normal(5, 3.5, N), 0.5, 30).round(1)

# Income: lognormal, employment-type dependent
base_income = RNG.lognormal(mean=10.9, sigma=0.55, size=N)  # monthly income baseline
emp_income_mult = np.array([1.15 if e == "Salaried" else 1.35 if e == "Business Owner" else 1.0 for e in employment_type])
monthly_income = np.round(base_income * emp_income_mult, -2)
monthly_income = np.clip(monthly_income, 15000, 900000)
annual_income = (monthly_income * 12).round(0)

branch_choice_idx = RNG.integers(0, len(branch_df), size=N)
branch_row = branch_df.iloc[branch_choice_idx].reset_index(drop=True)
city, state, region, branch_id, branch_name = (
    branch_row["city"].values, branch_row["state"].values, branch_row["region"].values,
    branch_row["branch_id"].values, branch_row["branch_name"].values,
)
branch_risk = branch_row["branch_risk_mult"].values
pincode = RNG.integers(110001, 700099, size=N)

# Assign an officer that belongs to the applicant's branch
officer_by_branch = {b: officer_df[officer_df.branch_id == b].reset_index(drop=True) for b in branch_df.branch_id}
loan_officer_id, loan_officer_name, officer_skill = [], [], []
for b in branch_id:
    pool = officer_by_branch[b]
    row = pool.iloc[random.randrange(len(pool))]
    loan_officer_id.append(row.loan_officer_id)
    loan_officer_name.append(row.loan_officer_name)
    officer_skill.append(row.officer_skill_mult)
officer_skill = np.array(officer_skill)

loan_product = RNG.choice(PRODUCT_NAMES, size=N, p=[0.40, 0.25, 0.20, 0.15])
loan_purpose = [random.choice(LOAN_PURPOSES[p]) for p in loan_product]
product_risk = np.array([PRODUCTS[p]["risk"] for p in loan_product])
collateral_type = [COLLATERAL_TYPES[p] for p in loan_product]

interest_rate = np.array([round(RNG.uniform(*PRODUCTS[p]["rate"]), 2) for p in loan_product])
tenure_months = np.array([RNG.integers(PRODUCTS[p]["tenure"][0], PRODUCTS[p]["tenure"][1] + 1) for p in loan_product])

# Loan amount scaled to income and product
income_mult_for_loan = RNG.uniform(3, 14, size=N)
loan_amount = np.round(monthly_income * income_mult_for_loan / 1000) * 1000
loan_amount = np.clip(loan_amount, 50000, 7500000)
sanctioned_amount = np.round(loan_amount * RNG.uniform(0.9, 1.0, size=N) / 1000) * 1000
disbursed_amount = np.round(sanctioned_amount * RNG.uniform(0.97, 1.0, size=N) / 1000) * 1000

# EMI (standard amortization formula)
r = interest_rate / 1200
emi_amount = np.round((disbursed_amount * r * (1 + r) ** tenure_months) / ((1 + r) ** tenure_months - 1), 0)
processing_fee = np.round(sanctioned_amount * RNG.uniform(0.005, 0.02, size=N), 0)

# Credit score: correlated inversely with eventual risk factors, some noise
credit_score = np.clip(RNG.normal(680, 90, size=N), 300, 900).round(0).astype(int)

existing_loans_count = RNG.poisson(1.1, size=N).clip(0, 6)
existing_emi_obligations = np.round(existing_loans_count * RNG.uniform(2000, 15000, size=N), 0)
debt_to_income_ratio = np.round(np.clip((existing_emi_obligations + emi_amount) / monthly_income, 0.02, 1.4), 3)

collateral_value = np.where(
    np.isin(loan_product, ["Auto Loan", "Gold Loan"]),
    np.round(disbursed_amount * RNG.uniform(1.0, 1.4, size=N), 0), 0
)
co_applicant_flag = RNG.choice(["Yes", "No"], size=N, p=[0.28, 0.72])

# ---------------------------------------------------------------------------
# 3. DATES (seasonal demand + inconsistent formats baked in)
# ---------------------------------------------------------------------------
start_date = datetime(2023, 1, 1)
month_weights = np.array([0.7, 0.7, 0.8, 0.8, 0.9, 0.9, 0.9, 0.9, 1.1, 1.5, 1.6, 1.3])  # Oct-Dec festive spike
day_offsets = []
for _ in range(N):
    m = RNG.choice(36, p=np.tile(month_weights, 3) / np.tile(month_weights, 3).sum())
    base = start_date + timedelta(days=int(m * 30.4))
    day_offsets.append(base + timedelta(days=int(RNG.integers(0, 28))))
application_date = day_offsets
approval_lag = RNG.integers(1, 10, size=N)
disbursal_lag = RNG.integers(1, 5, size=N)
approval_date = [d + timedelta(days=int(a)) for d, a in zip(application_date, approval_lag)]
disbursal_date = [d + timedelta(days=int(dl)) for d, dl in zip(approval_date, disbursal_lag)]

# ---------------------------------------------------------------------------
# 4. DEFAULT PROBABILITY MODEL (the core business logic)
# ---------------------------------------------------------------------------
z_credit = (700 - credit_score) / 100          # higher when score is low
z_dti = (debt_to_income_ratio - 0.35) * 3.2    # higher when DTI is high
z_income = -(np.log(monthly_income) - 10.9) * 0.9  # higher when income is low
z_branch = (branch_risk - 1.0) * 1.4
z_product = (product_risk - 1.0) * 0.9
z_emp = np.array([EMPLOYMENT_RISK[e] for e in employment_type])
z_emp = (z_emp - 1.0) * 0.8
z_officer = (officer_skill - 1.0) * 1.1
z_tenure = (tenure_months - 36) / 100

logit = -3.85 + 0.55*z_credit + 0.55*z_dti + 0.5*z_income + 0.6*z_branch + 0.5*z_product + 0.4*z_emp + 0.5*z_officer + 0.3*z_tenure
default_prob = 1 / (1 + np.exp(-logit))
default_flag = (RNG.uniform(size=N) < default_prob).astype(int)

months_on_book = pd.Series(((datetime(2026, 6, 30) - pd.to_datetime(disbursal_date)).days // 30)).clip(lower=1)
days_past_due = np.where(
    default_flag == 1,
    RNG.integers(31, 361, size=N),
    np.where(RNG.uniform(size=N) < 0.06, RNG.integers(1, 30, size=N), 0)  # minor delinquency noise
)
npa_flag = np.where(days_past_due >= 90, "Yes", "No")

loan_status = []
for i in range(N):
    if default_flag[i] == 1:
        loan_status.append("Written-Off" if days_past_due[i] > 300 and RNG.uniform() < 0.4 else "Default")
    elif months_on_book.iloc[i] >= tenure_months[i]:
        loan_status.append("Closed")
    else:
        loan_status.append("Active")

recovery_amount = np.where(
    np.isin(loan_status, ["Default", "Written-Off"]),
    np.round(disbursed_amount * RNG.uniform(0.05, 0.55, size=N), 0), 0
)

payment_history_score = np.clip(np.round(900 - days_past_due * 1.8 - z_dti * 40 + RNG.normal(0, 30, N)), 100, 900).astype(int)
bounce_count = np.where(default_flag == 1, RNG.integers(2, 12, size=N), RNG.poisson(0.4, size=N)).clip(0, 15)

risk_category = pd.cut(default_prob, bins=[-0.01, 0.15, 0.35, 0.6, 1.01], labels=["Low", "Medium", "High", "Very High"])
customer_segment = np.where(monthly_income > 150000, "Premium",
                    np.where(monthly_income > 60000, "Mass Affluent", "Mass Market"))

# Fraud: rare, concentrated in mismatched income/loan-amount + specific channel
fraud_score = ((loan_amount / (monthly_income + 1)) > 18).astype(int) + (RNG.uniform(size=N) < 0.004).astype(int)
is_fraud_suspected = np.where(fraud_score >= 1, "Yes", "No")
kyc_verified = np.where(RNG.uniform(size=N) < 0.985, "Yes", "No")
channel = RNG.choice(CHANNELS, size=N, p=[0.35, 0.30, 0.20, 0.10, 0.05])

# ---------------------------------------------------------------------------
# 5. ASSEMBLE DATAFRAME
# ---------------------------------------------------------------------------
df = pd.DataFrame({
    "loan_id": [f"LN{100000+i}" for i in range(N)],
    "applicant_id": [f"AP{200000+i}" for i in range(N)],
    "customer_name": customer_name,
    "gender": gender,
    "date_of_birth": [d.strftime("%Y-%m-%d") for d in dob],
    "age": age,
    "marital_status": marital_status,
    "education": education,
    "occupation": occupation,
    "employment_type": employment_type,
    "employer_name": employer_name,
    "years_with_employer": years_with_employer,
    "annual_income": annual_income,
    "monthly_income": monthly_income,
    "city": city,
    "state": state,
    "pincode": pincode,
    "branch_id": branch_id,
    "branch_name": branch_name,
    "region": region,
    "loan_product": loan_product,
    "loan_purpose": loan_purpose,
    "loan_amount": loan_amount,
    "sanctioned_amount": sanctioned_amount,
    "disbursed_amount": disbursed_amount,
    "interest_rate": interest_rate,
    "tenure_months": tenure_months,
    "emi_amount": emi_amount,
    "processing_fee": processing_fee,
    "credit_score": credit_score,
    "debt_to_income_ratio": debt_to_income_ratio,
    "existing_loans_count": existing_loans_count,
    "existing_emi_obligations": existing_emi_obligations,
    "collateral_type": collateral_type,
    "collateral_value": collateral_value,
    "co_applicant_flag": co_applicant_flag,
    "application_date": application_date,
    "approval_date": approval_date,
    "disbursal_date": disbursal_date,
    "loan_status": loan_status,
    "default_flag": default_flag,
    "days_past_due": days_past_due,
    "npa_flag": npa_flag,
    "recovery_amount": recovery_amount,
    "loan_officer_id": loan_officer_id,
    "loan_officer_name": loan_officer_name,
    "payment_history_score": payment_history_score,
    "bounce_count": bounce_count,
    "risk_category": risk_category.astype(str),
    "customer_segment": customer_segment,
    "is_fraud_suspected": is_fraud_suspected,
    "kyc_verified": kyc_verified,
    "channel": channel,
})

# ---------------------------------------------------------------------------
# 6. INTENTIONAL DATA QUALITY ISSUES (as required by project spec)
# ---------------------------------------------------------------------------
# 6a. Format dates inconsistently for a subset of rows (simulate multi-source export)
def messy_date(d, fmt_choice):
    formats = ["%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%m/%d/%Y", "%d %b %Y"]
    return d.strftime(formats[fmt_choice])

for col in ["application_date", "approval_date", "disbursal_date"]:
    fmt_idx = RNG.integers(0, 5, size=N)
    df[col] = [messy_date(d, f) for d, f in zip(df[col], fmt_idx)]

# 6b. Missing values: 3-5% across a realistic subset of columns
missing_cols = ["monthly_income", "annual_income", "credit_score", "collateral_value",
                 "employer_name", "years_with_employer", "co_applicant_flag",
                 "payment_history_score", "days_past_due", "recovery_amount"]
for col in missing_cols:
    frac = RNG.uniform(0.03, 0.05)
    idx = RNG.choice(N, size=int(N * frac), replace=False)
    df.loc[idx, col] = np.nan

# 6c. Duplicate records (<1%) - genuine full-row duplicates simulating a resync error
dup_idx = RNG.choice(N, size=int(N * 0.006), replace=False)
df = pd.concat([df, df.loc[dup_idx]], ignore_index=True)

# 6d. Outliers: a few extreme incomes / loan amounts (data entry errors)
outlier_idx = RNG.choice(len(df), size=int(N * 0.002), replace=False)
df.loc[outlier_idx, "monthly_income"] = df.loc[outlier_idx, "monthly_income"] * RNG.uniform(15, 40)
outlier_idx2 = RNG.choice(len(df), size=int(N * 0.0015), replace=False)
df.loc[outlier_idx2, "loan_amount"] = df.loc[outlier_idx2, "loan_amount"] * RNG.uniform(8, 15)

# 6e. Shuffle final row order so it doesn't look artificially generated in sequence
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# ---------------------------------------------------------------------------
# 7. SAVE OUTPUTS
# ---------------------------------------------------------------------------
df.to_csv("/mnt/user-data/outputs/finedge_loan_portfolio.csv", index=False, encoding="utf-8")
print("Rows:", len(df), "Columns:", len(df.columns))
print(df.isna().mean().sort_values(ascending=False).head(12))
df.to_pickle("/home/claude/finedge_df.pkl")
