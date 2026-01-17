import streamlit as st
from openai import OpenAI
import PIL.Image
import base64
import io

# 1. Initialize OpenAI Client
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"].strip())
except Exception as e:
    st.error("🔑 OpenAI API Key Missing in Streamlit Secrets!")

st.set_page_config(page_title="OmniHealth AI", layout="wide", page_icon="⚕️")

# ⚡ NUCLEAR RESET (Sidebar)
with st.sidebar:
    st.title("Admin Panel")
    if st.button("🚨 NUCLEAR RESET CACHE"):
        st.session_state.clear()
        st.rerun()

# 2. iOS Glassmorphism UI
st.markdown("""
    <style>
    [data-testid="stHeader"] { background-color: rgba(0,0,0,0) !important; }
    footer {visibility: hidden;}
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #020617 100%); }
    .glass-card {
        background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(45px) saturate(160%);
        border-radius: 35px; border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 40px; margin: 10px auto; color: white;
    }
    .stButton>button { width: 100% !important; border-radius: 12px !important; font-weight: 600 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. UI Dashboard
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.title("⚕️ OmniHealth AI")
st.caption("ChatGPT-Powered Triage • Apple Glass Design")

st.divider()

#  Patient Profile Row
st.subheader("👤 Patient Profile")
p1, p2, p3, p4 = st.columns(4)
with p1: age = st.number_input("Age", 0, 120, 25)
with p2: gender = st.selectbox("Gender", ["Male", "Female", "Other"])
with p3: 
    ctx_opts = ["None", "Pregnant", "Breastfeeding", "Puberty"] if gender == "Female" else ["None", "Puberty"]
    context = st.selectbox("Context", ctx_opts)
with p4: allergies = st.text_input("Allergies", placeholder="e.g. Penicillin")

st.divider()

#  Analysis Section
c1, c2 = st.columns(2)
with c1:
    st.subheader("Input")
    query = st.text_input("Symptom or Medication", placeholder="What are we checking?")
    uploaded = st.file_uploader("Scan Medicine/Prescription", type=["jpg", "png", "jpeg"])
    
    col_b1, col_b2, _ = st.columns([2, 1, 1])
    with col_b1:
        run = st.button("Analyze Now 🔍")
    with col_b2:
        if st.button("Reset"):
            if 'report' in st.session_state: del st.session_state.report
            st.rerun()

with c2:
    st.subheader("Clinical Report")
    if 'report' in st.session_state and st.session_state.report:
        report_text = str(st.session_state.report)
        if any(w in report_text.lower() for w in ["emergency", "urgent", "doctor immediately"]):
            st.error("🚨 URGENT: CONSULT A DOCTOR IMMEDIATELY")
        st.write(st.session_state.report)
    else:
        st.info("Ready. Please provide input and click Analyze.")

st.markdown('</div>', unsafe_allow_html=True)

# 4. Helper: Convert Image to Base64 for OpenAI
def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

# 5. Execution Logic (OpenAI Integration)
if run:
    with st.spinner("🧬 ChatGPT Neural Engine Processing..."):
        try:
            prompt = (f"Act as a professional medical assistant. Analyze for a {age}y/o {gender} "
                      f"with context '{context}' and allergies '{allergies}'. Input: {query}.")
            
            messages = [{"role": "user", "content": [{"type": "text", "text": prompt}]}]
            
            if uploaded:
                base64_image = encode_image(uploaded)
                messages[0]["content"].append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                })

            response = client.chat.completions.create(
                model="gpt-4o-mini", # High speed, low cost for hackathons
                messages=messages,
                max_tokens=500
            )
            
            st.session_state.report = response.choices[0].message.content
            st.rerun()
        except Exception as e:
            st.error(f"Engine Error: {str(e)}")

st.caption("DISCLAIMER: Hackathon MVP using OpenAI API. Not for clinical diagnosis.")
