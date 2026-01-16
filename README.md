# OmniHealthAI
OmniHealth AI is an advanced health-tech solution designed to provide personalized, safety-first analysis of medical products and symptoms. Unlike standard AI wrappers, OmniHealth utilizes a multi-layered logic system to ensure user safety and data accuracy.

Key Features
Multi-User Profile Management: Supports multiple profiles (e.g., family members) with individual data for age, gender, allergies, and chronic conditions.

Contextual Analysis Engine: Injects user health data directly into the AI prompt to provide personalized dosage and safety warnings.

Dual-Input Logic: Seamlessly switches between Computer Vision (label scanning) and Manual Entry for maximum reliability.

Independent Safety Guardrails: A hard-coded Python triage system that scans AI output for "danger words" and triggers high-visibility emergency alerts.

Self-Correction & Confidence Scoring: The AI provides a confidence percentage (0-100%) for every identification, encouraging users to verify low-confidence results.

🛠️ Technical Stack
Frontend: Streamlit (Python)

AI Model: Google Gemini 2.5 Flash-Lite

Deployment: Streamlit Community Cloud

Data Handling: Session State-based local memory

🛡️ Safety Disclaimer
This tool is for educational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult with a licensed healthcare provider before making medical decisions.
