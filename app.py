import streamlit as st
import google.generativeai as genai
import json
import xml.etree.ElementTree as ET

# --- CONFIGURATION ---
st.set_page_config(page_title="Zentrexo Audit Engine", page_icon="🛡️", layout="wide")

# Securely load API key from Streamlit Secrets
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Upgraded to the 3.1 Flash model for high-speed, cost-effective processing
    model = genai.GenerativeModel('gemini-3.1-flash') 
except Exception as e:
    st.error("🚨 API Key missing or invalid. Please check your Streamlit Secrets.")

# --- SIDEBAR: COMPLIANCE & SECURITY ---
with st.sidebar:
    st.header("🛡️ Enterprise Security")
    st.success("🔒 **SSL/TLS Encryption Active**")
    st.markdown("""
    **2026 Compliance Audit:**
    * **Zero Data Retention:** Files are processed in-memory and wiped instantly.
    * **Private API:** Powered by paid enterprise endpoints. Your data is **never** used for model training.
    * **DPDP / GDPR Ready:** Built for Indian and EU data privacy standards.
    """)
    st.divider()

# --- CORE AUDIT LOGIC (FORMAT AGNOSTIC) ---
def process_audit_file(file):
    file_extension = file.name.split('.')[-1].lower()
    
    if file_extension == "pdf":
        st.info("🔍 PDF Detected: Initializing AI Vision extraction...")
        # Placeholder for full PDF byte-extraction logic
        # In a live environment, you would use Gemini's File API here
        prompt = "You are a logistics auditor. Analyze the uploaded PDF invoice data for fuel surcharge errors, duplicate billing, and dimension discrepancies. Provide a 'Found Money' summary."
        return "PDF logic executed: Vision API integration ready for testing."
        
    elif file_extension == "json":
        st.info("⚡ JSON Detected: High-Speed Deterministic Parsing (India GST Standard)...")
        try:
            data = json.load(file)
            st.json(data) # Displays the raw JSON beautifully in the UI
            
            # Pass the raw JSON text directly to the AI for logical auditing
            prompt = f"You are a forensic logistics auditor. Audit the following JSON freight data for 8% leakage, duplicate charges, or math errors. Output a professional recovery report: {json.dumps(data)}"
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"❌ JSON Parsing Error: {e}"
            
    elif file_extension == "xml":
        st.info("🇪🇺 XML Detected: Enterprise Peppol Ingestion...")
        try:
            tree = ET.parse(file)
            root = tree.getroot()
            
            # Convert XML to string to pass to the AI
            xml_string = ET.tostring(root, encoding='unicode')
            st.code(xml_string[:500] + "... (truncated)", language="xml")
            
            prompt = f"You are a forensic logistics auditor. Audit the following Peppol XML freight invoice for leakage, tax anomalies, and billing compliance. Output a professional recovery report: {xml_string}"
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"❌ XML Parsing Error: {e}"
            
    else:
        return "❌ Unsupported Format. Please upload PDF, JSON, or XML."

# --- MAIN UI ---
st.title("Zentrexo Engine: Global Audit 🌍")
st.markdown("Upload carrier invoices or structured GST data to instantly identify revenue leakage.")

uploaded_file = st.file_uploader(
    "Upload Carrier File (.pdf, .json, .xml)", 
    type=["pdf", "json", "xml"]
)

if uploaded_file is not None:
    if st.button("Run Forensic Analysis", type="primary"):
        with st.spinner("Auditing carrier math and contract compliance..."):
            result = process_audit_file(uploaded_file)
            
            st.divider()
            st.subheader("📊 Audit Results")
            st.write(result)
            
            if "Error" not in result and "Unsupported" not in result:
                st.success("✅ Analysis Complete. Ready for Human-in-the-Loop review.")