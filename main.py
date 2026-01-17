import streamlit as st
from google import genai
import PIL.Image

# 1. Initialize Gemini Client
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("API Key missing in Streamlit Secrets!")

# 2. Page Configuration
st.set_page_config(page_title="OmniHealth AI", layout="wide", page_icon="⚕️")

# ⚡ NUCLEAR RESET (Sidebar) - Clears "Standby" loop
with st.sidebar:
    st.title("Admin Panel")
    if st.button("🚨 NUCLEAR RESET CACHE"):
        st.cache_resource.clear()
        st.session_state.clear()
        st.rerun()
    st.info("Use this if the app is stuck or you changed the API key.")

# 3. iOS Glassmorphism UI Styling
st.markdown("""
    <style>
    /* Clean Header/Footer */
    [data-testid="stHeader"] { background-color: rgba(0,0,0,0) !important; color: white !important; }
    .stDeployButton { display: none; }
    footer {visibility: hidden;}
    
    /* 🌌 Background & Glass Panel */
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #020617 100%); }
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(45px) saturate(160%);
        border-radius: 35px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 40px;
        box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.7);
        margin: 10px auto;
        color: white;
    }
    
    /* 🔘 iOS Style Buttons */
    .stButton>button {
        width: 100% !important;
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. Main UI Dashboard
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

# Header
h1, h2 = st.columns([4, 1])
with h1:
    st.title("⚕️ OmniHealth AI")
    st.caption("Context-Aware Medical Analysis • Apple Glass Design")
with h2:
    st.write("🟢 **System Live**")

st.divider()

#  Step 1: Patient Profile Manager
st.subheader("👤 Patient Profile")
p1, p2, p3, p4 = st.columns(4)
with p1:
    age = st.number_input("Age", 0, 120, 25)
with p2:
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
with p3:
    ctx_opts = ["None", "Pregnant", "Breastfeeding", "Puberty"] if gender == "Female" else ["None", "Puberty"]
    context = st.selectbox("Context", ctx_opts)
with p4:
    allergies = st.text_input("Allergies", placeholder="e.g. Penicillin")

st.divider()

#  Step 2: Analysis Area
c1, c2 = st.columns(2)

with c1:
    st.subheader("Input")
    query = st.text_input("Symptom or Medicine", placeholder="What are we checking?")
    uploaded_file = st.file_uploader("Scan Image", type=["jpg", "png"])
    
    b1, b2, _ = st.columns([2, 1, 1])
    with b1:
        run = st.button("Analyze Now 🔍")
    with b2:
        if st.button("Reset"):
            if 'report' in st.session_state: del st.session_state.report
            st.rerun()

with c2:
    st.subheader("Clinical Report")
    # SAFE DISPLAY LOGIC: Fixes the 'NoneType' attribute error
    if 'report' in st.session_state and st.session_state.report:
        report_text = str(st.session_state.report)
        
        # 🚨 Triage Safety Check
        if any(w in report_text.lower() for w in ["emergency", "urgent", "doctor immediately"]):
            st.error("🚨 URGENT: CONSULT A DOCTOR IMMEDIATELY")
        
        st.write(st.session_state.report)
    else:
        st.info("Awaiting medical input... Use the 'Analyze' button to start.")

st.markdown('</div>', unsafe_allow_html=True)

# 5. Analysis Engine
if run:
    with st.spinner("🧬 Processing Neural Request..."):
        try:
            # Build the personalized prompt
            prompt = (f"Act as a professional medical assistant. Analyze for a {age}y/o {gender} "
                      f"with context '{context}' and allergies '{allergies}'. Input: {query}.")
            
            if uploaded_file:
                img = PIL.Image.open(uploaded_file)
                response = client.models.generate_content(model="gemini-2.0-flash-lite", contents=[img, prompt])
            else:
                response = client.models.generate_content(model="gemini-2.0-flash-lite", contents=[prompt])
            
            # Store result in session state
            st.session_state.report = response.text
            st.rerun()
            
        except Exception as e:
            st.error(f"Engine Error: {str(e)}")
            if "429" in str(e):
                st.warning("⚠️ Quota Exhausted. Ensure you are using a fresh API key in Secrets.")

st.caption("DISCLAIMER: This is a hackathon MVP. Not for actual medical diagnosis.")
