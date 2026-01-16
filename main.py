import streamlit as st
from google import genai
import PIL.Image
import re

# 1. Setup Client
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
st.set_page_config(page_title="OmniHealth AI", layout="wide")

# 2. iOS Glass Styling (No extra boxes, no bars) 
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {padding: 0rem !important;} 

    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(50px) saturate(180%);
        -webkit-backdrop-filter: blur(50px) saturate(180%);
        border-radius: 40px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 50px;
        width: 90%;
        margin: 5vh auto;
        box-shadow: 0 20px 60px rgba(0,0,0,0.8);
        color: white;
    }

    /* Standardizes inputs for iOS feel */
    input, select, .stSelectbox {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
    }

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
    
    .stButton>button {
        width: 100% !important;
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: 600;
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

# 3. Initialization
if 'output' not in st.session_state: st.session_state.output = None

# --- MAIN DASHBOARD ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

#  Header
h1, h2 = st.columns([4, 1])
with h1:
    st.title("⚕️ OmniHealth AI")
    st.caption("Apple Glass Design • Context-Aware Medical Engine")
with h2:
    st.write("🟢 **System Live**")

st.divider()

#  Step 1: Integrated Profile Manager (The "Disappeared" Part)
st.subheader("👤 Patient Profile")
p1, p2, p3, p4 = st.columns(4)
with p1:
    age = st.number_input("Age", 0, 120, 25)
with p2:
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
with p3:
    # Logic: Only show pregnancy options for Female
    ctx_opts = ["None", "Pregnant", "Breastfeeding", "Puberty"] if gender == "Female" else ["None", "Puberty"]
    context = st.selectbox("Medical Context", ctx_opts)
with p4:
    allergies = st.text_input("Allergies", placeholder="e.g. Penicillin")

st.divider()

#  Step 2: Analysis Area
c1, c2 = st.columns(2)
with c1:
    st.subheader("Medical Input")
    manual_input = st.text_input("Symptom or Medicine", placeholder="What are we checking?", label_visibility="collapsed")
    uploaded = st.file_uploader("Upload Image", type=["jpg", "png"], label_visibility="collapsed")
    
    b1, b2, _ = st.columns([2, 1, 1])
    with b1:
        run = st.button("Run Advanced Analysis 🔍")
    with b2:
        if st.button("Reset"):
            st.session_state.output = None
            st.rerun()

with c2:
    st.subheader("Clinical Report")
    if st.session_state.output:
        # Check for safety alerts in output
        if "emergency" in st.session_state.output.lower():
            st.error("🚨 URGENT: CONSULT A DOCTOR")
        st.write(st.session_state.output)
    else:
        st.info("Awaiting medical data for processing...")

st.markdown('</div>', unsafe_allow_html=True)

# 4. Analysis Logic
if run:
    with st.spinner("🧬 Processing through medical engine..."):
        # Combine profile data with query for the AI
        st.session_state.output = f"Analyzing for {age}y/o {gender} with {allergies} allergies. Engine Standby: Verify Gemini API key."

st.caption("DISCLAIMER: Educational project. Not for real medical diagnosis.")
