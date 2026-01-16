import streamlit as st
from google import genai
import PIL.Image

# 1. Setup Client
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
st.set_page_config(page_title="OmniHealth AI", layout="wide")

# 2. Force Clean iOS UI (Removes all default Streamlit boxes/headers)
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
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
        padding: 60px;
        width: 85%;
        margin: 5vh auto;
        box-shadow: 0 20px 60px rgba(0,0,0,0.8);
        color: white;
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
        white-space: nowrap !important;
        background: rgba(255, 255, 255, 0.1) !important;
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

# 3. App Content
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

col_h1, col_h2 = st.columns([4, 1])
with col_h1:
    st.title("⚕️ OmniHealth AI")
    st.caption("Apple Glass Design • Context-Aware Medical Engine")
with col_h2:
    st.write("🟢 **System Live**")

st.markdown("<br>", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    st.subheader("Input")
    manual_input = st.text_input("Product", placeholder="Type symptoms or medicine name...", label_visibility="collapsed")
    uploaded = st.file_uploader("Scan Image", type=["jpg", "png"], label_visibility="collapsed")
    
    b1, b2, _ = st.columns([2, 1, 1])
    with b1:
        run = st.button("Analyze Now 🔍")
    with b2:
        reset = st.button("Reset")

with c2:
    st.subheader("Report")
    if 'output' in st.session_state:
        st.write(st.session_state.output)
    else:
        st.info("Awaiting input for analysis.")

st.markdown('</div>', unsafe_allow_html=True)

if run:
    st.session_state.output = "Engine active. Analyzing your medical request..."
if reset:
    if 'output' in st.session_state:
        del st.session_state.output
    st.rerun()
