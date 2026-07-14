import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AI Customer Intelligence Dashboard",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Customer Intelligence Dashboard")
st.write(
    "AI-powered customer view combining CRM, support tickets, and email insights."
)

# Load datasets
crm = pd.read_csv("crm_data.csv")
support = pd.read_csv("support_data.csv")
emails = pd.read_csv("email_data.csv")

# Combine customer information
customer_data = crm.merge(support, on="Customer")
customer_data = customer_data.merge(emails, on="Customer")


st.subheader("📊 Unified Customer View")

st.dataframe(customer_data)


# Select customer
customer = st.selectbox(
    "Select Customer",
    customer_data["Customer"]
)

selected = customer_data[
    customer_data["Customer"] == customer
].iloc[0]


# Customer Summary
st.subheader("🧠 AI Customer Summary")

summary = f"""
**Customer Name:** {selected['Customer']}

**Industry:** {selected['Industry']}

**Subscription Plan:** {selected['Plan']}

**Status:** {selected['Status']}

**Support History:** {selected['Issue']}

**Customer Communication:** {selected['Email_Context']}
"""

st.markdown(summary)


# Risk Analysis
st.subheader("⚠️ Risk Analysis")

if "failure" in selected["Issue"].lower():
    risk = "High"
    reason = "Customer reported a payment/product issue."
elif "cancellation" in selected["Email_Context"].lower():
    risk = "High"
    reason = "Customer is considering cancellation."
else:
    risk = "Low"
    reason = "No major risk signals detected."

st.write("Risk Level:", risk)
st.write("Reason:", reason)


# Opportunity
st.subheader("🚀 Business Opportunity")

if "upgrade" in selected["Email_Context"].lower():
    opportunity = "Potential premium upgrade opportunity."
elif "demo" in selected["Email_Context"].lower():
    opportunity = "Opportunity to convert customer after product demo."
else:
    opportunity = "Build engagement and identify customer needs."

st.success(opportunity)


# Next Action
st.subheader("✅ Next Best Action")

action = [
    "Contact customer within 24 hours",
    "Address reported concerns",
    "Discuss suitable product improvements",
    "Track customer satisfaction"
]

for item in action:
    st.write("✔️", item)


# Download report
st.subheader("📥 Download Customer Report")

report = f"""
Customer Intelligence Report

Customer:
{selected['Customer']}

Industry:
{selected['Industry']}

Risk:
{risk}

Reason:
{reason}

Opportunity:
{opportunity}

Recommended Actions:
- Contact customer
- Resolve issues
- Follow up
"""

st.download_button(
    label="Download Report",
    data=report,
    file_name="customer_report.txt",
    mime="text/plain"
)