import streamlit as st
from google import genai
from google.genai import types # Add this line

# --- 1. ZENTREXO BRANDING ---
st.set_page_config(page_title="Zentrexo | AI Forensic Audit", page_icon="🎯", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #050505; color: white; }
    .stButton>button { background-color: #3b82f6; color: white; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 Zentrexo Audit Engine")
st.subheader("Autonomous Revenue Recovery for Logistics")
st.write("---")

# --- 2. SECURE 2026 CONNECTION ---
if "GEMINI_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Missing API Key in Streamlit Secrets.")
    st.stop()

# --- 3. THE INTERFACE ---
uploaded_file = st.file_uploader("Upload a Carrier Invoice (PDF)", type="pdf")

if uploaded_file is not None:
    if st.button("🚀 Run Forensic Analysis"):
        with st.spinner("Zentrexo Agents are scrutinizing line items..."):
            try:
                # 1. Capture the file data
                file_bytes = uploaded_file.read()
                file_type = uploaded_file.type # Automatically gets 'application/pdf' or 'image/png'

                # 2. Wrap the data in a 2026 "Part" object
                invoice_part = types.Part.from_bytes(
                    data=file_bytes,
                    mime_type=file_type
                )

                # 3. Send to the 2026 Workhorse Model
                response = client.models.generate_content(
                    model="gemini-2.0-flash", # The stable 2026 engine
                    contents=[
                        "You are the Zentrexo Forensic Auditor. Analyze this invoice for revenue leakage. "
                        "Check for: Fuel Surcharges > 12%, duplicate handling fees, and PSS charges outside peak months. "
                        "Format the output as a professional Recovery Report.",
                        invoice_part
                    ]
                )
                
                st.success("Audit Complete!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Audit Error: {e}")

st.caption("Zentrexo Proprietary Engine v2.0 | Confidential")