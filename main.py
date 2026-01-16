import streamlit as st
from google import genai
import PIL.Image
import re

# 1. Initialize Client
# IMPORTANT: Secure your API key before deploying!
genai.configure(api_key="YOUR_ACTUAL_API_KEY_HERE")
model = genai.GenerativeModel("gemini-1.5-flash")

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
    
    # Switch User
    selected_user = st.selectbox("Switch Active Profile", options=list(st.session_state.profiles.keys()))
    st.session_state.current_user = selected_user
    
    # Edit current profile
    user_data = st.session_state.profiles[st.session_state.current_user]
    with st.form("edit_profile"):
        st.markdown(f"**Settings for: {st.session_state.current_user}**")
        age = st.number_input("Age", 0, 120, user_data['age'])
        gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(user_data['gender']))
        
        # Conditional Logic for Gender 🚺
        if gender == "Female":
            hormonal = st.selectbox("Special Context", ["None", "Pregnant", "Breastfeeding", "Puberty", "Menopause"])
        else:
            hormonal = st.selectbox("Special Context", ["None", "Puberty", "Other"])
            
        allergies = st.text_input("Allergies", user_data['allergies'])
        chronic = st.text_input("Chronic Conditions", user_data['chronic'])
        
        if st.form_submit_button("Update Profile"):
            st.session_state.profiles[st.session_state.current_user] = {
                "age": age, "gender": gender, "context": hormonal, "allergies": allergies, "chronic": chronic
            }
            st.success("Profile Updated!")

    # Add New User
    new_user_name = st.text_input("Create New Profile Name:")
    if st.button("➕ Add Profile") and new_user_name:
        if new_user_name not in st.session_state.profiles:
            st.session_state.profiles[new_user_name] = {"age": 25, "gender": "Male", "context": "None", "allergies": "None", "chronic": "None"}
            st.rerun()

    st.divider()
    language = st.selectbox("App Language", ["English", "Hindi", "Spanish", "French"])
    if st.button("Clear Results 🗑️"):
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
    st.caption(f"Active Profile: **{st.session_state.current_user}**")
    
    uploaded_file = st.file_uploader("Option 1: Scan Medicine or Symptom", type=["jpg", "jpeg", "png"])
    manual_name = st.text_input("Option 2: Type Product or Symptom Name:")

    if st.button("Run Advanced Analysis 🔍"):
        active_p = st.session_state.profiles[st.session_state.current_user]
        with st.spinner("Consulting Medical Engine..."):
            try:
                prompt = f"""
                Analyze for a {active_p['age']}y/o {active_p['gender']} (Context: {active_p['context']}). 
                Allergies: {active_p['allergies']}. Chronic Conditions: {active_p['chronic']}.
                
                Provide:
                1. CONFIDENCE SCORE: (0-100%)
                2. INFO: Category & Ingredients.
                3. PERSONALIZED ADVICE: Dosage/Application for this specific profile.
                4. FIRST AID: 3 immediate Do's and Don'ts.
                5. SOURCE: Search query for Mayo Clinic/WHO.
                6. SAFETY: Conflicts with {active_p['allergies']}.
                
                Respond in {language}. If urgent, start with 'EMERGENCY'.
                """
                
                if uploaded_file:
                    img = PIL.Image.open(uploaded_file)
                    response = client.models.generate_content(model="gemini-2.5-flash-lite", contents=[img, prompt])
                elif manual_name:
                    response = model.generate_content(f"Item: {manual_name}. {prompt}")
                else:
                    st.warning("Please provide an input.")
                    response = None

                if response:
                    st.session_state.analysis_output = response.text
            except Exception as e:
                st.error(f"Error: {e}")

    if st.session_state.analysis_output:
        st.divider()
        dangers = check_emergency(st.session_state.analysis_output)
        if dangers:
            st.error(f"🚨 **URGENT ALERT**: Found {', '.join(dangers)}.")
        
        score_match = re.search(r"CONFIDENCE SCORE:\s*(\d+)%", st.session_state.analysis_output)
        if score_match:
            score = int(score_match.group(1))
            st.write(f"**AI Confidence:** {score}%")
            st.progress(score / 100)

        st.subheader("📋 Personalized Medical Report")
        st.write(st.session_state.analysis_output)

st.divider()
st.info("DISCLAIMER: Educational tool only. Always consult a doctor.")