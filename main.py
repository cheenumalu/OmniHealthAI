import streamlit as st
from google import genai
import PIL.Image

# 1. Initialize Gemini Client
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("API Key missing in Secrets!")

# 2. Page Configuration
st.set_page_config(page_title="OmniHealth AI", layout="wide", page_icon="⚕️")

# ⚡ NUCLEAR RESET: Clears all ghost data/cache without touching the UI
with st.sidebar:
    st.title("Admin Tools")
    if st.button("🚨 NUCLEAR RESET CACHE"):
        st.cache_resource.clear()
        st.session_state.clear()
        st.rerun()
    st.info("Use this if the engine stays in 'Standby' mode.")

# 3. iOS Glassmorphism UI + Cursor Glow
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {padding-top: 2rem !important;} 
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #020617 100%); }

    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(45px) saturate(160%);
        -webkit-backdrop-filter: blur(45px) saturate(160%);
        border-radius: 35px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 40px;
        box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.7);
        margin: 10px auto;
        color: white;
    }

    #cursor-glow {
        position: fixed; width: 600px; height: 600px;
        background: radial-gradient(circle, rgba(56, 189, 248, 0.1) 0%, transparent 70%);
        border-radius: 50%; pointer-events: none;
        transform: translate(-50%, -50%); z-index: 1;
    }
    
    .stButton>button {
        width: 100% !important;
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 12px !important;
    }
    </style>
    <div id="cursor-glow"></div>
    <script>
    const glow = document.getElementById('cursor-glow');
    document.addEventListener('mousemove', (e) => {
        window.requestAnimationFrame(() => {
            glow.style.left = e.clientX + 'px';
            glow.style.top = e.clientY + 'px';
        });
    });
    </script>
    """, unsafe_allow_html=True)

# 4. Main Glass Dashboard
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

# Header
h1, h2 = st.columns([4, 1])
with h1:
    st.title("⚕️ OmniHealth AI")
    st.caption("Context-Aware Medical Analysis • Apple Glass Design")
with h2:
    st.write("🟢 **System Live**")

st.divider()

#  Step 1: Patient Profile Row
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

#  Step 2: Input & Analysis
c1, c2 = st.columns(2)

with c1:
    st.subheader("Input")
    query = st.text_input("Symptom/Medicine", placeholder="What are you checking?")
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
    if 'report' in st.session_state:
        # Triage Red Alert Logic
        if any(w in st.session_state.report.lower() for w in ["emergency", "urgent", "doctor immediately"]):
            st.error("🚨 URGENT: CONSULT A DOCTOR")
        st.write(st.session_state.report)
    else:
        st.info("Awaiting medical input...")

st.markdown('</div>', unsafe_allow_html=True)

# 5. Engine Logic
if run:
    with st.spinner("🧬 Consulting AI Engine..."):
        try:
            prompt = (f"Act as a professional medical triage assistant. Analyze for a {age}y/o {gender} "
                      f"with context '{context}' and allergies '{allergies}'. Input: {query}.")
            
            if uploaded_file:
                img = PIL.Image.open(uploaded_file)
                response = client.models.generate_content(model="gemini-2.0-flash-lite", contents=[img, prompt])
            else:
                response = client.models.generate_content(model="gemini-2.0-flash-lite", contents=[prompt])
            
            st.session_state.report = response.text
            st.rerun()
        except Exception as e:
            st.error(f"Engine Error: {str(e)}")

st.caption("DISCLAIMER: Educational tool for OmniHealth AI project. Always consult a physician.")
