
import streamlit as st
import datetime
import re

# ------------------ Page Setup ------------------
st.set_page_config(page_title="BD Assistant", layout="centered")
st.title("📄 Business Development Assistant")
st.write("Assess incoming RFPs and generate timeline, fees & roadmap.")

# ------------------ Input Area ------------------
st.subheader("1. Paste RFP or Upload File")

rfp_text = st.text_area("Paste RFP content here", height=200)

uploaded_file = st.file_uploader("Or upload a .txt file", type=["txt"])
if uploaded_file:
    rfp_text = uploaded_file.read().decode("utf-8")

if not rfp_text:
    st.info("Please enter or upload RFP content above.")
    st.stop()

# ------------------ Scope Detection ------------------
st.subheader("2. Detected Scope")

scopes = [
    "organizational development",
    "strategy",
    "operational excellence",
    "transformation",
    "corporate governance",
    "data analytics"
]

detected_scopes = [scope for scope in scopes if re.search(rf"\b{re.escape(scope)}\b", rfp_text, re.IGNORECASE)]
if detected_scopes:
    st.success(f"Detected scope(s): {', '.join(detected_scopes)}")
else:
    st.warning("No clear scope detected. Please review the RFP or assign manually.")

# ------------------ Client Profile ------------------
st.subheader("3. Client Profile")

location = st.selectbox("Location", ["EGYPT", "UAE", "KSA"])
revenue = st.selectbox("Client Top Line Revenue", ["< $5M", "$5M–$50M", "$50M–$500M", "> $500M"])
industry = st.selectbox("Industry", ["Non-Profit", "Government/Public", "Manufacturing", "Financial Services", "Tech/Startup"])
employees = st.selectbox("Employee Count", ["< 50", "50–500", "> 500"])

# ------------------ Base Rates ------------------
currency_map = {"EGYPT": "USD", "UAE": "AED", "KSA": "SAR"}
daily_rate_map = {"EGYPT": 1100, "UAE": 10000, "KSA": 12500}
currency = currency_map[location]
base_daily_rate = daily_rate_map[location]

# Revenue Multiplier
revenue_multiplier = {"< $5M": 0.8, "$5M–$50M": 1.0, "$50M–$500M": 1.2, "> $500M": 1.5}[revenue]

# Industry Multiplier
industry_multiplier = {
    "Non-Profit": 0.9,
    "Government/Public": 1.0,
    "Manufacturing": 1.1,
    "Financial Services": 1.3,
    "Tech/Startup": 1.2
}[industry]

# Adjusted daily rate
adjusted_daily_rate = base_daily_rate * revenue_multiplier * industry_multiplier

# ------------------ Estimate Timeline ------------------
st.subheader("4. Estimated Timeline")

word_count = len(rfp_text.split())
base_weeks = min(12, max(4, word_count // 300))

# Adjust based on employee count
if employees == "< 50":
    estimated_weeks = base_weeks
elif employees == "50–500":
    estimated_weeks = base_weeks + 1
else:  # > 500
    estimated_weeks = base_weeks + 2

timeline_text = f"Estimated project duration: **{estimated_weeks} weeks**"

# ------------------ Fee Estimate ------------------
estimated_days = estimated_weeks * 5
total_fees = adjusted_daily_rate * estimated_days
fees_text = f"Estimated total fees: **{currency} {total_fees:,.0f}**"

# ------------------ Roadmap ------------------
st.subheader("5. Suggested Roadmap")

phases = [
    "1. Kickoff & Research",
    "2. Stakeholder Interviews",
    "3. Analysis & Insights",
    "4. Draft Report",
    "5. Final Presentation"
]

phase_weeks = estimated_weeks // len(phases)
roadmap = ""
for i, phase in enumerate(phases):
    start = i * phase_weeks + 1
    end = start + phase_weeks - 1
    roadmap += f"- {phase} ({start}–{end} week)\n"

# ------------------ Display Results ------------------
st.markdown("### 🗓️ Project Timeline")
st.markdown(timeline_text)

st.markdown("### 💵 Fee Estimate")
st.markdown(fees_text)

st.markdown("### 🧭 Project Roadmap")
st.markdown(roadmap)

# ------------------ Downloadable Summary ------------------
from io import StringIO
import base64

summary = f"""PROJECT ASSESSMENT SUMMARY

Detected Scope(s): {', '.join(detected_scopes) if detected_scopes else 'Not detected'}
Location: {location}
Currency: {currency}
Base Daily Rate: {base_daily_rate:,}
Adjusted Daily Rate: {adjusted_daily_rate:,.2f}
Revenue Tier: {revenue}
Industry: {industry}
Employee Count: {employees}
Estimated Weeks: {estimated_weeks}
Estimated Days: {estimated_days}
Estimated Fees: {currency} {total_fees:,.0f}

ROADMAP:
{roadmap}
"""

b64 = base64.b64encode(summary.encode()).decode()
href = f'<a href="data:file/txt;base64,{b64}" download="project_summary.txt">📥 Download Summary</a>'
st.markdown(href, unsafe_allow_html=True)
