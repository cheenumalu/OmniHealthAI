import streamlit as st
from google import genai
import PIL.Image

# 1. Initialize Client with Space-Stripping Safety
try:
    # .strip() handles any accidental spaces in your Secrets dashboard
    api_key = st.secrets["GEMINI_API_KEY"].strip()
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error("🔑 API Key Missing or Invalid in Streamlit Secrets!")

# 2. Page Configuration
st.set_page_config(page_title="OmniHealth AI", layout="wide", page_icon="⚕️")

# ⚡ NUCLEAR RESET (Sidebar): Clears persistent standby loops
with st.sidebar:
    st.title("System Admin")
    if st.button("🚨 NUCLEAR RESET CACHE"):
        st.cache_resource.clear()
        st.session_state.clear()
        st.rerun()

# 3. iOS Glassmorphism UI
st.markdown("""
    <style>
    [data-testid="stHeader"] { background-color: rgba(0,0,0,0) !important; }
    footer {visibility: hidden;}
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #020617 100%); }
    .glass-card {
        background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(45px) saturate(160%);
        border-radius: 35px; border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 40px; margin: 10px auto; color: white;
    }
    .stButton>button { 
        width: 100% !important; border-radius: 12px !important; 
        background: rgba(255, 255, 255, 0.08) !important; color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. Main UI Dashboard
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.title("⚕️ OmniHealth AI")
st.caption("Apple Glass Medical Triage • Powered by Gemini 2.0")

st.divider()

#  Patient Profile
st.subheader("👤 Patient Profile")
p1, p2, p3, p4 = st.columns(4)
with p1: age = st.number_input("Age", 0, 120, 25)
with p2: gender = st.selectbox("Gender", ["Male", "Female", "Other"])
with p3: 
    ctx_opts = ["None", "Pregnant", "Breastfeeding", "Puberty"] if gender == "Female" else ["None", "Puberty"]
    context = st.selectbox("Context", ctx_opts)
with p4: allergies = st.text_input("Allergies", placeholder="e.g. Penicillin")

st.divider()

#  Input & Output Columns
c1, c2 = st.columns(2)
with c1:
    st.subheader("Medical Input")
    query = st.text_input("Symptom/Medicine", placeholder="What should we analyze?")
    uploaded = st.file_uploader("Scan Label/Prescription", type=["jpg", "png", "jpeg"])
    
    col_b1, col_b2, _ = st.columns([2, 1, 1])
    with col_b1:
        run = st.button("Analyze Now 🔍")
    with col_b2:
        if st.button("Reset"):
            if 'report' in st.session_state: del st.session_state.report
            st.rerun()

with c2:
    st.subheader("Clinical Report")
    # ✅ Safety Shield: Check for 'report' before processing
    if 'report' in st.session_state and st.session_state.report:
        report_text = str(st.session_state.report)
        
        # Emergency Red Alert Detection
        if any(w in report_text.lower() for w in ["emergency", "urgent", "doctor immediately"]):
            st.error("🚨 URGENT: CONSULT A DOCTOR IMMEDIATELY")
            
        st.write(st.session_state.report)
    else:
        st.info("System Ready. Please provide input to generate report.")

st.markdown('</div>', unsafe_allow_html=True)

# 5. Analysis Logic
if run:
    with st.spinner("🧬 Neural Engine Processing..."):
        try:
            prompt = (f"Act as a professional medical assistant. Analyze for a {age}y/o {gender} "
                      f"with context '{context}' and allergies '{allergies}'. Input: {query}.")
            
            if uploaded:
                img = PIL.Image.open(uploaded)
                res = client.models.generate_content(model="gemini-2.0-flash-lite", contents=[img, prompt])
            else:
                res = client.models.generate_content(model="gemini-2.0-flash-lite", contents=[prompt])
            
            st.session_state.report = res.text
            st.rerun()
        except Exception as e:
            # Handle API errors without crashing the UI
            st.error(f"Engine Error: {str(e)}")
            if "429" in str(e):
                st.warning("⚠️ Rate limit reached. Consider switching to Demo Mode for the presentation.")

st.caption("DISCLAIMER: Hackathon Project MVP. Not for clinical use.")
