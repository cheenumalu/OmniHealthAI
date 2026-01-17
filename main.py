import streamlit as st
from google import genai
import PIL.Image

# 1. Initialize Client with Safety Logic
try:
    # .strip() removes any accidental spaces from your Streamlit Secrets dashboard
    api_key = st.secrets["GEMINI_API_KEY"].strip()
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error("🔑 API Key Missing or Invalid in Streamlit Secrets!")

# 2. Page Config
st.set_page_config(page_title="OmniHealth AI", layout="wide", page_icon="⚕️")

# ⚡ NUCLEAR RESET: Clears stuck cache and ghost data
with st.sidebar:
    st.title("Admin Tools")
    if st.button("🚨 NUCLEAR RESET CACHE"):
        st.cache_resource.clear()
        st.session_state.clear()
        st.rerun()
    st.info("Click this if you get a 'Resource Exhausted' or 'Engine Standby' message.")

# 3. iOS Glassmorphism UI
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

# 4. Main UI Dashboard
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.title("⚕️ OmniHealth AI")
st.caption("Context-Aware Triage • Apple Glass Design")

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
    query = st.text_input("Query", placeholder="Symptoms or medication...")
    uploaded = st.file_uploader("Scan Image", type=["jpg", "png", "jpeg"])
    
    col_b1, col_b2, _ = st.columns([2, 1, 1])
    with col_b1:
        run = st.button("Analyze Now 🔍")
    with col_b2:
        if st.button("Reset"):
            if 'report' in st.session_state: del st.session_state.report
            st.rerun()

with c2:
    st.subheader("Clinical Report")
    # ✅ FIX: Safely check if report exists before processing
    if 'report' in st.session_state and st.session_state.report:
        report_text = str(st.session_state.report)
        
        # Emergency Red Alert
        if any(w in report_text.lower() for w in ["emergency", "urgent", "doctor immediately"]):
            st.error("🚨 URGENT: CONSULT A DOCTOR IMMEDIATELY")
            
        st.write(st.session_state.report)
    else:
        st.info("Ready. Please provide input and click Analyze.")

st.markdown('</div>', unsafe_allow_html=True)

# 5. Execution Logic
if run:
    with st.spinner("🧬 Neural Engine Processing..."):
        try:
            prompt = (f"Act as a medical assistant. Analyze for a {age}y/o {gender} "
                      f"with context '{context}' and allergies '{allergies}'. Input: {query}.")
            
            if uploaded:
                img = PIL.Image.open(uploaded)
                res = client.models.generate_content(model="gemini-2.0-flash-lite", contents=[img, prompt])
            else:
                res = client.models.generate_content(model="gemini-2.0-flash-lite", contents=[prompt])
            
            st.session_state.report = res.text
            st.rerun()
        except Exception as e:
            st.error(f"Engine Error: {str(e)}")

st.caption("DISCLAIMER: Hackathon MVP. Not for clinical diagnosis.")
