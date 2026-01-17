import streamlit as st
from google import genai
import PIL.Image

# 1. Setup - This MUST be at the very top
st.set_page_config(page_title="OmniHealth AI", layout="wide")

# ⚡ FORCE CACHE CLEAR (This fixes your standby loop)
if st.sidebar.button("🚨 NUCLEAR RESET (Click if stuck)"):
    st.cache_resource.clear()
    st.session_state.clear()
    st.rerun()

# 2. Initialize Client with the NEW key
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# 3. iOS Glass UI Styling (Clean & Box-Free)
st.markdown("""
    <style>
    header {visibility: hidden;} footer {visibility: hidden;}
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #020617 100%); }
    .glass-card {
        background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(50px);
        border-radius: 35px; border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 40px; margin: 20px auto; color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. App Content
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.title("⚕️ OmniHealth AI")

# Profile Row
p1, p2, p3 = st.columns(3)
with p1: age = st.number_input("Age", 0, 120, 25)
with p2: gender = st.selectbox("Gender", ["Male", "Female"])
with p3: allergies = st.text_input("Allergies", "None")

st.divider()

c1, c2 = st.columns(2)
with c1:
    query = st.text_input("Query", placeholder="What are you checking?")
    uploaded = st.file_uploader("Upload Image", type=["jpg", "png"])
    if st.button("Analyze Now 🔍"):
        with st.spinner("Calling AI Engine..."):
            try:
                prompt = f"Medical triage for {age}y/o {gender} with {allergies} allergies. Query: {query}"
                if uploaded:
                    img = PIL.Image.open(uploaded)
                    res = client.models.generate_content(model="gemini-2.0-flash-lite", contents=[img, prompt])
                else:
                    res = client.models.generate_content(model="gemini-2.0-flash-lite", contents=[prompt])
                st.session_state.report = res.text
            except Exception as e:
                st.session_state.report = f"⚠️ Engine Error: {str(e)}"

with c2:
    st.subheader("Report")
    if 'report' in st.session_state:
        st.write(st.session_state.report)
    else:
        st.info("Awaiting input...")

st.markdown('</div>', unsafe_allow_html=True)
