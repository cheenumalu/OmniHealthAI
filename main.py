import streamlit as st
from google import genai
import PIL.Image
import re

# 1. Initialize Client (Uses Streamlit Secrets for Deployment)
# Make sure to add GEMINI_API_KEY to your Streamlit Cloud Secrets!
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# 2. Session State Initialization 🧠
if 'profiles' not in st.session_state:
    st.session_state.profiles = {
        "Default User": {"age": 25, "gender": "Male", "context": "None", "allergies": "None", "chronic": "None"}
    }
if 'current_user' not in st.session_state:
    st.session_state.current_user = "Default User"
if 'analysis_output' not in st.session_state:
    st.session_state.analysis_output = None

# --- SIDEBAR: Multi-User Profile Manager 👥 ---
with st.sidebar:
    st.title("👥 Profile Manager")
    
    # Switch User dropdown
    selected_user = st.selectbox("Active Profile", options=list(st.session_state.profiles.keys()))
    st.session_state.current_user = selected_user
    
    # Edit current profile form
    user_data = st.session_state.profiles[st.session_state.current_user]
    with st.form("edit_profile"):
        st.markdown(f"**Settings for: {st.session_state.current_user}**")
        age = st.number_input("Age", 0, 120, user_data['age'])
        gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(user_data['gender']))
        
        # 🚺 Conditional Logic: Men don't see Pregnancy options
        if gender == "Female":
            hormonal = st.selectbox("Special Context", ["None", "Pregnant", "Breastfeeding", "Puberty", "Menopause"])
        else:
            hormonal = st.selectbox("Special Context", ["None", "Puberty", "Other"])
            
        allergies = st.text_input("Allergies", user_data['allergies'])
        chronic = st.text_input("Chronic Conditions", user_data['chronic'])
        
        if st.form_submit_button("Save & Update Profile"):
            st.session_state.profiles[st.session_state.current_user] = {
                "age": age, "gender": gender, "context": hormonal, "allergies": allergies, "chronic": chronic
            }
            st.success("Profile Updated!")

    # Add New User section
    new_user_name = st.text_input("Create New Profile Name:")
    if st.button("➕ Add Profile") and new_user_name:
        if new_user_name not in st.session_state.profiles:
            st.session_state.profiles[new_user_name] = {"age": 25, "gender": "Male", "context": "None", "allergies": "None", "chronic": "None"}
            st.rerun()

    st.divider()
    language = st.selectbox("Response Language", ["English", "Hindi", "Spanish", "French"])
    if st.button("Reset Analysis 🗑️"):
        st.session_state.analysis_output = None
        st.rerun()

# --- EMERGENCY LOGIC 🚨 ---
def check_emergency(text):
    danger_words = ["emergency", "severe", "anaphylaxis", "difficulty breathing", "chest pain", "poisoning", "urgent"]
    return [word for word in danger_words if word in text.lower()]

# --- MAIN INTERFACE 🎯 ---
l, mid, r = st.columns([1, 5, 1])

with mid:
    st.title("⚕️ OmniHealth AI")
    st.caption(f"Currently Analyzing for: **{st.session_state.current_user}**")
    
    # Dual Input Methods
    uploaded_file = st.file_uploader("Option 1: Scan Medicine or Symptom", type=["jpg", "jpeg", "png"])
    manual_name = st.text_input("Option 2: Type Product or Symptom Name:")

    if st.button("Deep Medical Analysis 🔍"):
        active_p = st.session_state.profiles[st.session_state.current_user]
        with st.spinner("Analyzing with personalized safety data..."):
            try:
                # Optimized, concise prompt
                prompt = f"""
                Analyze for a {active_p['age']}y/o {active_p['gender']} (Context: {active_p['context']}). 
                Allergies: {active_p['allergies']}. Chronic Conditions: {active_p['chronic']}.
                
                Be concise and direct. Structure the response:
                1. CONFIDENCE SCORE: (0-100%)
                2. SUMMARY: Product Category, Ingredients, and Primary Use.
                3. PERSONALIZED DOSAGE: Specific guidelines for this user.
                4. SAFETY CHECK: Conflicts with {active_p['allergies']} or {active_p['chronic']}.
                5. FIRST AID: 3 immediate 'Do's and Don'ts'.
                6. SOURCE: A Mayo Clinic/WHO search query for verification.
                
                Respond in {language}. If urgent, start with 'EMERGENCY'.
                """
                
                if uploaded_file:
                    img = PIL.Image.open(uploaded_file)
                    response = client.models.generate_content(model="gemini-2.0-flash-lite", contents=[img, prompt])
                elif manual_name:
                    response = client.models.generate_content(model="gemini-2.0-flash-lite", contents=[f"Item: {manual_name}. " + prompt])
                else:
                    st.warning("Please provide an input (Photo or Text).")
                    response = None

                if response:
                    st.session_state.analysis_output = response.text
            except Exception as e:
                st.error(f"Error: {e}")

    # --- CONCISE DASHBOARD UI 🚦 ---
    if st.session_state.analysis_output:
        st.divider()
        
        # Extract metadata for the Dashboard
        dangers = check_emergency(st.session_state.analysis_output)
        score_match = re.search(r"CONFIDENCE SCORE:\s*(\d+)%", st.session_state.analysis_output)
        
        # Metric Row
        col_a, col_b = st.columns(2)
        with col_a:
            if score_match:
                score = int(score_match.group(1))
                st.metric("AI Confidence", f"{score}%")
                st.progress(score / 100)
            else:
                st.metric("AI Confidence", "N/A")
        
        with col_b:
            if dangers:
                st.error(f"🚨 URGENT ALERT: {', '.join(dangers)}")
            else:
                st.success("✅ STABLE: No immediate danger detected")

        # Detailed Report
        st.subheader("📋 Personalized Medical Summary")
        with st.expander("Click to view full clinical details", expanded=True):
            st.write(st.session_state.analysis_output)

st.divider()
st.info("DISCLAIMER: For educational use only. Not a medical diagnosis. Always consult a physician.")
