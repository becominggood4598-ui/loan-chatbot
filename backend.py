import math
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("Enter your API key here"))


# ---------------- EMI CALCULATION ----------------
def calculate_emi(principal, annual_rate, tenure_months):
    monthly_rate = annual_rate / 12 / 100

    emi = (principal * monthly_rate * (1 + monthly_rate) ** tenure_months) / \
          ((1 + monthly_rate) ** tenure_months - 1)

    return round(emi, 2)


# ---------------- LOAN LOGIC ----------------
def analyze_loan(income, loan, tenure, cibil):

    annual_rate = 8.5
    emi = calculate_emi(loan, annual_rate, tenure)

    annual_income = income * 12
    foir = (emi / income) * 100
    lti = loan / annual_income

    # Approval Decision
    if cibil < 650:
        status = "Rejected"
    elif foir > 50:
        status = "Rejected"
    elif lti > 5:
        status = "Rejected"
    else:
        status = "Approved"

    # Risk Score
    risk = 0

    if cibil >= 750:
        risk += 10
    elif cibil >= 700:
        risk += 30
    elif cibil >= 650:
        risk += 50
    else:
        risk += 80

    if foir > 45:
        risk += 20
    elif foir > 35:
        risk += 10

    if lti > 4:
        risk += 15

    risk = min(risk, 100)

    return {
        "emi": emi,
        "foir": round(foir, 2),
        "lti": round(lti, 2),
        "status": status,
        "risk": risk
    }


# ---------------- AI EXPLANATION ----------------
def generate_explanation(data):

    prompt = f"""
You are a banking assistant in India.
All currency is INR ₹.

Loan decision is FINAL. Do NOT change approval status.

Income: ₹{data['income']}
Loan Amount: ₹{data['loan']}
EMI: ₹{data['emi']}
FOIR: {data['foir']}%
Loan-to-Income Ratio: {data['lti']}
CIBIL: {data['cibil']}
Internal Risk Score (0 = lowest risk, 100 = highest risk): {data['risk']}
This is NOT the CIBIL score.
CIBIL Score: {data['cibil']} (range 300-900)

Status: {data['status']}

Explain clearly:
1. Why loan is approved/rejected
2. What EMI means
3. What risk score indicates
4. One suggestion to improve eligibility
"""

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return completion.choices[0].message.content



