import streamlit as st
import google.generativeai as genai

# --- 1. ZENTREXO BRANDING ---
st.set_page_config(page_title="Zentrexo | AI Forensic Audit", page_icon="🎯", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #002D62; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 Zentrexo Audit Engine")
st.subheader("Autonomous Revenue Recovery for Logistics")
st.write("---")

# --- 2. SECURE API CONNECTION ---
# This looks for the key you will save in "Streamlit Secrets"
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Missing API Key. Please add 'GEMINI_API_KEY' to your Streamlit Secrets.")
    st.stop()

# --- 3. THE FORENSIC RULEBOOK (The "Expert" Logic) ---
MASTER_PROMPT = """
You are the Zentrexo Lead Forensic Auditor. Your goal is to identify revenue leakage in logistics invoices.

CRITICAL RULES:
1. Fuel Surcharge Cap: Any fuel surcharge exceeding 12% of the Base Rate is a violation.
2. Duplicate Fees: If 'Handling' or 'Documentation' is listed twice, or as a separate line item when the contract says 'All-Inclusive', flag it.
3. The 'Ghost' Fee: Look for 'Peak Season Surcharges' (PSS). If the invoice date is between January and August, flag PSS as a potential error.
4. Math Verification: Recalculate the Total. If the carrier's total is higher than the sum of line items, flag it.

OUTPUT FORMAT:
- List each Error Type.
- State the 'Evidence' (Line item name/amount).
- Calculate the 'Recoverable Amount'.
- Show the Zentrexo 30% Success Fee.
"""

# --- 4. THE INTERFACE ---
uploaded_file = st.file_uploader("Upload a Carrier Invoice (PDF)", type="pdf")

if uploaded_file is not None:
    st.info("Invoice received. Ready to audit.")
    
    if st.button("🚀 Run Forensic Analysis"):
        with st.spinner("Zentrexo Agents are scrutinizing line items..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash') # Using the 2026 workhorse
                
                # Convert the uploaded file to the format Gemini needs
                pdf_data = uploaded_file.read()
                contents = [
                    MASTER_PROMPT,
                    {"mime_type": "application/pdf", "data": pdf_data}
                ]
                
                response = model.generate_content(contents)
                
                st.success("Audit Complete!")
                st.write("### 📋 Recovery Report")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"An error occurred during the audit: {e}")

st.write("---")
st.caption("Zentrexo Proprietary Audit Engine v1.0 | Confidential & Secure")