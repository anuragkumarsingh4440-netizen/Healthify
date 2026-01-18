# Import libraries
import streamlit as st
import google.generativeai as genai
import pandas as pd

# Page config
# This block sets up the page layout and title
st.set_page_config(
    page_title="HEALTHIFY - AI Health Assistant",
    page_icon="💊",
    layout="wide"
)

# Custom CSS for full dark mode
# This block applies black background and bright text for all components
st.markdown("""
    <style>
        /* Set background to black */
        body, .stApp {
            background-color: #000000;
            color: #FFFFFF;
        }

        /* Bright text for headings */
        h1, h2, h3, h4, h5, h6, p, label {
            color: #FFFFFF !important;
        }

        /* Style buttons */
        .stButton>button {
            background-color: #1E90FF;
            color: #FFFFFF;
            border-radius: 8px;
            border: 1px solid #FFFFFF;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #FF4500;
            color: #FFFFFF;
        }

        /* Style text inputs */
        .stTextInput>div>div>input {
            background-color: #111111;
            color: #FFFFFF;
            border: 1px solid #FFFFFF;
        }

        /* Style select boxes */
        .stSelectbox>div>div>select {
            background-color: #111111;
            color: #FFFFFF;
            border: 1px solid #FFFFFF;
        }

        /* Style sliders */
        .stSlider>div>div>div {
            color: #FFFFFF;
        }

        /* Sidebar styling */
        .css-1d391kg, .stSidebar {
            background-color: #000000 !important;
            color: #FFFFFF !important;
        }
    </style>
""", unsafe_allow_html=True)

# API Key configuration
api = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api)

# Initialize Gemini model
model = genai.GenerativeModel(model_name="gemini-2.5-flash-lite")

# Main heading block
st.markdown('<div style="background-color:#1E90FF; padding:20px; border-radius:10px; text-align:center; font-size:40px; font-weight:bold; color:white;">HEALTHIFY — AI Powered Personal Health Assistant</div>', unsafe_allow_html=True)

# Intro text
st.markdown("### 🧠 Your Smart Medical Companion\nAsk any health-related question and get **personalized guidance** instantly.")

# Sidebar inputs
st.sidebar.header("📝 Enter Your Details")
name = st.sidebar.text_input("👤 Name")
gender = st.sidebar.selectbox("⚧ Gender", ["Male", "Female", "Other"])
age = st.sidebar.text_input("🎂 Age (yrs)")
weight = st.sidebar.text_input("⚖️ Weight (kg)")
height = st.sidebar.text_input("📏 Height (cm)")
fitness = st.sidebar.slider("💪 Rate your fitness (0-5)", 0, 5, step=1)

# BMI calculation
try:
    weight_val = pd.to_numeric(weight)
    height_val = pd.to_numeric(height)
    if height_val > 0:
        bmi = weight_val / (height_val/100)**2
    else:
        bmi = None
except Exception:
    bmi = None

if bmi:
    st.sidebar.success(f"✅ {name}, your BMI is: **{round(bmi,2)} Kg/m²**")

# User query
user_query = st.text_input("💬 Enter your health question here:")

prompt = f"""
Assume you are a health expert. Use the following details:
- Name: {name}
- Gender: {gender}
- Age: {age}
- Weight: {weight} kg
- Height: {height} cm
- BMI: {bmi} kg/m²
- Fitness rating: {fitness}/5

Answer the user's query: {user_query}
"""

if user_query:
    response = model.generate_content(prompt)
    st.markdown("## 🩺 AI Health Guidance")
    st.write(response.candidates[0].content.parts[0].text)
