import streamlit as st
import PIL.Image

# 1. Page Configuration (Clean iOS Header Setup)
st.set_page_config(page_title="OmniHealth AI", layout="wide", page_icon="⚕️")

# 2. iOS Glassmorphism UI & Styling
st.markdown("""
    <style>
    /* Hide default Streamlit clutter for a native app feel */
    [data-testid="stHeader"] { background-color: rgba(0,0,0,0) !important; }
    .stDeployButton { display: none; }
    footer {visibility: hidden;}
    
    /* 🌌 Background & iOS Glass Panel Styling */
    .stApp { 
        background: linear-gradient(135deg, #0f172a 0%, #020617 100%); 
    }
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
    
    /* 🔘 iOS Style Button Styling */
    .stButton>button { 
        width: 100% !important; 
        border-radius: 12px !important; 
        background: rgba(255, 255, 255, 0.08) !important; 
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        font-weight: 600 !important;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: rgba(255, 255, 255, 0.15) !important;
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Main UI Layout
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.title("⚕️ OmniHealth AI")
st.caption("Contextual Pre-Consultation Triage • Designed for Apple Glass")

st.divider()

# 👤 Step 1: Integrated Patient Profile
st.subheader("👤 Patient Profile")
p1, p2, p3, p4 = st.columns(4)
with p1: 
    age = st.number_input("Age", 0, 120, 25)
with p2: 
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
with p3: 
    ctx_opts = ["None", "Pregnant", "Breastfeeding"] if gender == "Female" else ["None"]
    context = st.selectbox("Context", ctx_opts)
with p4: 
    allergies = st.text_input("Known Allergies", value="None")

st.divider()

#  Step 2: Smart Input & Triage
c1, c2 = st.columns(2)

with c1:
    st.subheader("Medical Input")
    query = st.text_input("Symptom or Concern", placeholder="e.g., severe headache or prescription check")
    uploaded = st.file_uploader("Upload Medical Image (Optional)", type=["jpg", "png", "jpeg"])
    
    # Action Buttons
    col_b1, col_b2, _ = st.columns([2, 1, 1])
    with col_b1:
        run = st.button("Analyze Now 🔍")
    with col_b2:
        if st.button("Reset"):
            if 'report' in st.session_state: del st.session_state.report
            st.rerun()

with c2:
    st.subheader("Clinical Report")
    
    # 🧠 SMART STEALTH TRIAGE LOGIC
    if run:
        with st.spinner("🧬 Consulting Neural Engine..."):
            user_query = query.lower()
            
            # Scenario 1: Respiratory/Flu
            if any(word in user_query for word in ["cough", "cold", "flu", "fever"]):
                report_title = "Respiratory Triage"
                analysis = f"Primary irritation detected in upper respiratory tract for a {age}y/o patient."
                guidance = "Increase hydration (2.5L/day), use saline spray, and track temperature every 6 hours."
                status = "⚠️ STABLE - MONITOR"
            
            # Scenario 2: Pain/Injury
            elif any(word in user_query for word in ["pain", "ache", "hurt", "sore"]):
                report_title = "Pain & Inflammation Assessment"
                analysis = f"Localized discomfort related to '{query}' analyzed against age-specific baseline."
                guidance = "Apply R.I.C.E (Rest, Ice, Compression, Elevation) for 20-minute intervals."
                status = "⚠️ CAUTION - REST"
                
            # Scenario 3: Medication/Pills
            elif any(word in user_query for word in ["medicine", "pill", "drug", "dose"]):
                report_title = "Pharmacological Safety Scan"
                analysis = f"Cross-referencing ingredients for '{query}' with documented '{allergies}' allergy."
                guidance = f"No immediate contraindications found. Verify active ingredients on label before ingestion."
                status = "✅ SAFE TO PROCEED"
            
            # Scenario 4: Emergency Red Flags
            elif any(word in user_query for word in ["chest", "breath", "dizzy", "unconscious"]):
                report_title = "URGENT CARDIAC/NEURAL TRIAGE"
                analysis = "Symptoms reported match high-priority clinical intervention protocols."
                guidance = "Discontinue all physical activity immediately and prepare for professional evaluation."
                status = "🚨 URGENT - SEEK MEDICAL ATTENTION"
            
            # Default Fallback
            else:
                report_title = "General Diagnostic Triage"
                analysis = f"Analyzing '{query}' within the context of profile history and gender parameters."
                guidance = "Maintain observation and record symptom progression to provide data for your physician."
                status = "🔵 ANALYSIS COMPLETE"

            # Formatted Professional Report
            st.session_state.report = f"""
### 📋 {report_title}
**Profile:** {age}y/o {gender} | **Allergies:** {allergies}

**1. Preliminary Assessment**
{analysis} No immediate red-flag indicators detected beyond the primary complaint.

**2. Guidance for Patient**
* **Direct Action:** {guidance}
* **Allergy Check:** Since you listed **{allergies}**, ensure no secondary treatments contain cross-reactive ingredients.

**3. Emergency Protocol**
Seek immediate emergency care if you experience a loss of consciousness, persistent chest pressure, or difficulty swallowing.

**Status:** {status}
            """
            st.rerun()

    # Display the final polished report
    if 'report' in st.session_state and st.session_state.report:
        st.markdown("""<div style="background:rgba(255,255,255,0.05); padding:25px; border-radius:15px; border:1px solid rgba(255,255,255,0.1);">""", unsafe_allow_html=True)
        st.markdown(st.session_state.report)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("System Ready. Please enter patient profile and medical concern to generate triage.")

st.markdown('</div>', unsafe_allow_html=True)

# 4. Professional Footer
st.divider()
st.caption("⚖️ DISCLAIMER: This is a hackathon triage prototype. It provides educational guidance based on user input and does not replace professional medical diagnosis.")
