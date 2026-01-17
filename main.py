import streamlit as st
from google import genai
import PIL.Image

# 1. Initialize Gemini Client (Background)
try:
    api_key = st.secrets["GEMINI_API_KEY"].strip()
    client = genai.Client(api_key=api_key)
except Exception:
    pass 

st.set_page_config(page_title="OmniHealth AI", layout="wide", page_icon="⚕️")

# ⚡ SIDEBAR CONTROLS
with st.sidebar:
    st.title("Settings")
    demo_mode = st.toggle("Enable Live Demo Mode", value=True)
    st.divider()
    if st.button("🚨 CLEAR SYSTEM CACHE"):
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
        border-radius: 35px; border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 40px; margin: 10px auto; color: white;
    }
    .stButton>button { width: 100% !important; border-radius: 12px !important; color: white !important;}
    </style>
    """, unsafe_allow_html=True)

# 3. Main Dashboard UI
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.title("⚕️ OmniHealth AI")
status = "🔵 DEMO MODE ACTIVE" if demo_mode else "🟢 SYSTEM LIVE"
st.caption(f"{status} • Contextual Pre-Consultation Triage")

st.divider()

# 👤 Patient Profile Section
st.subheader("👤 Patient Profile")
p1, p2, p3, p4 = st.columns(4)
with p1: age = st.number_input("Age", 0, 120, 25)
with p2: gender = st.selectbox("Gender", ["Male", "Female", "Other"])
with p3: 
    ctx_opts = ["None", "Pregnant", "Breastfeeding"] if gender == "Female" else ["None"]
    context = st.selectbox("Context", ctx_opts)
with p4: allergies = st.text_input("Allergies", value="None")

st.divider()

c1, c2 = st.columns(2)
with c1:
    st.subheader("Medical Input")
    query = st.text_input("Symptom or Concern", placeholder="e.g., persistent dry cough for 3 days")
    uploaded = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    
    if st.button("Analyze Now 🔍"):
        if demo_mode:
            with st.spinner("🧬 Consulting Neural Engine..."):
                # Enhanced Pre-Consultation Response
                st.session_state.report = f"""
### 📋 Clinical Triage Report
**Target Patient:** {age}y/o {gender} | **Allergies:** {allergies}

**1. Preliminary Risk Assessment**
Based on the input '{query}', your profile suggests a **Moderate** priority level. No immediate red-flag indicators (like respiratory distress or high fever) were detected in the text.

**2. Potential Causes to Discuss with a Doctor**
* **Environmental:** Possible reaction to allergens or seasonal changes.
* **Infectious:** Early-stage viral irritation (common for this age group).

**3. Home-Care Guidance (Pre-Consultation)**
* **Hydration:** Increase fluid intake to 2.5L daily to soothe membranes.
* **Monitoring:** Record your temperature twice daily to provide data for your physician.
* **Safety Check:** Since you mentioned **{allergies}** as an allergy, avoid any over-the-counter meds containing these ingredients.

**4. When to Seek Urgent Care**
Immediately visit an ER if you experience chest pain, difficulty breathing, or a fever exceeding 103°F (39.4°C).

**Status:** ⚠️ STABLE - SCHEDULE CONSULTATION
                """
                st.rerun()
        else:
            with st.spinner("🧬 Processing Live API..."):
                try:
                    prompt = f"Medical pre-consultation triage for {age}y/o {gender} with {allergies} allergies. Query: {query}"
                    res = client.models.generate_content(model="gemini-2.0-flash-lite", contents=[prompt])
                    st.session_state.report = res.text
                    st.rerun()
                except Exception as e:
                    st.error(f"API Error: {str(e)}")

with c2:
    st.subheader("Clinical Report")
    if 'report' in st.session_state and st.session_state.report:
        st.markdown("""<div style="background:rgba(255,255,255,0.05); padding:25px; border-radius:15px; border:1px solid rgba(255,255,255,0.1);">""", unsafe_allow_html=True)
        st.markdown(st.session_state.report)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("System Ready. Enter details to receive pre-consultation guidance.")

st.markdown('</div>', unsafe_allow_html=True)
st.caption("DISCLAIMER: This is a pre-consultation triage tool for educational purposes. It does not provide medical diagnoses.")
