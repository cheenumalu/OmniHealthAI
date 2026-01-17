import streamlit as st
from google import genai
import PIL.Image
import re

# 1. Initialize Gemini Client (Uses Secret Key)
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("Missing GEMINI_API_KEY in Streamlit Secrets!")

# 2. Page Configuration
st.set_page_config(page_title="OmniHealth AI", layout="wide", page_icon="⚕️")

# 3. iOS Glassmorphism UI + JavaScript Effects 🎨
st.markdown("""
    <style>
    /* 🛠️ RESTORE MENU: Hide white bar but keep the 3 dots button visible */
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
        color: white !important;
    }
    .stDeployButton { display: none; }
    footer {visibility: hidden;}
    .block-container {padding-top: 2rem !important;} 

    /* 🌌 Clean iOS Dark Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
    }

    /* ✨ Smooth Cursor Glow */
    #cursor-glow {
        position: fixed;
        width: 600px;
        height: 600px;
        background: radial-gradient(circle, rgba(56, 189, 248, 0.1) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
        transform: translate(-50%, -50%);
        z-index: 1;
    }

    /*  iOS Glass Panel */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(45px) saturate(160%);
        -webkit-backdrop-filter: blur(45px) saturate(160%);
        border-radius: 35px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 40px;
        box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.7);
        margin: 10px auto;
        color: white;
    }

    /* 🔘 Glossy Buttons */
    .stButton>button {
        width: 100% !important;
        white-space: nowrap !important;
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
        border-radius: 14px !important;
        padding: 12px 20px !important;
        font-weight: 600 !important;
        transition: 0.2s;
    }
    .stButton>button:hover {
        background: rgba(255, 255, 255, 0.15) !important;
        transform: scale(1.02);
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

# 4. Persistence & State Management
if 'report' not in st.session_state:
    st.session_state.report = None

# --- MAIN UI DASHBOARD ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

# Header
h1, h2 = st.columns([4, 1])
with h1:
    st.title("⚕️ OmniHealth AI")
    st.caption("Context-Aware Medical Analysis • iOS Glassmorphism Design")
with h2:
    st.markdown("<br>", unsafe_allow_html=True)
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
    allergies = st.text_input("Allergies", placeholder="e.g. Nuts, Penicillin")

st.divider()

#  Step 2: Input & Analysis
c1, c2 = st.columns([1.2, 1])

with c1:
    st.subheader("Input")
    query = st.text_input("Symptom or Medicine:", placeholder="What are you checking?")
    uploaded_file = st.file_uploader("Scan Medicine/Prescription", type=["jpg", "png", "jpeg"])
    
    b1, b2, _ = st.columns([2, 1, 1])
    with b1:
        run_analysis = st.button("Run Advanced Analysis 🔍")
    with b2:
        if st.button("Reset"):
            st.session_state.report = None
            st.rerun()

with c2:
    st.subheader("Clinical Report")
    if st.session_state.report:
        # Emergency Red Alert Logic
        if any(word in st.session_state.report.lower() for word in ["emergency", "urgent", "doctor immediately"]):
            st.error("🚨 URGENT: MEDICAL CONSULTATION REQUIRED")
        
        # Display the formatted report
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.1);">
            {st.session_state.report}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Awaiting medical input for neural processing...")

st.markdown('</div>', unsafe_allow_html=True)

# 5. Analysis Logic
if run_analysis:
    with st.spinner("🧬 Consulting AI Engine..."):
        try:
            # Construction of a personalized prompt
            prompt = (f"Act as a professional medical triage assistant. Analyze this for a {age} year old {gender} "
                      f"with context '{context}' and allergies '{allergies}'. "
                      f"Input: {query}. If an image is provided, analyze the text and visuals. "
                      f"Format: 1. Safety Status, 2. Key Findings, 3. Guidance, 4. When to see a doctor.")
            
            if uploaded_file:
                img = PIL.Image.open(uploaded_file)
                response = client.models.generate_content(model="gemini-2.0-flash-lite", contents=[img, prompt])
            else:
                response = client.models.generate_content(model="gemini-2.0-flash-lite", contents=[prompt])
            
            st.session_state.report = response.text
            st.rerun()
            
        except Exception as e:
            st.error(f"Engine Error: {str(e)}")
            if "429" in str(e):
                st.warning("⚠️ API Quota Exhausted. Switching to backup key recommended.")

st.divider()
st.caption("DISCLAIMER: Educational tool for hackathon demo. Not a substitute for professional medical advice.")
