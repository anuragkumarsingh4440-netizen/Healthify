# Importing required libraries
import streamlit as st
import google.generativeai as genai
import pandas as pd

# Page configuration
# This block sets the page title, icon, and layout
st.set_page_config(
    page_title="HEALTHIFY - AI Health Assistant",
    page_icon="💊",
    layout="wide"
)

# Custom CSS styling
# This block applies black background, white text, and rectangle box for heading
st.markdown("""
    <style>
        body {
            background-color: black;
            color: white;
        }
        .main-title {
            background-color: #1E90FF;
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-size: 40px;
            font-weight: bold;
        }
        h2, h3, h4 {
            color: orange !important;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# API Key configuration
# This block loads API key securely from Streamlit secrets
api = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api)

# Initialize Gemini model
# This block initializes the generative AI model
model = genai.GenerativeModel(model_name="gemini-2.5-flash-lite")

# Main heading block
# This block displays the main title inside a rectangle box
st.markdown('<div class="main-title">HEALTHIFY — AI Powered Personal Health Assistant</div>', unsafe_allow_html=True)

# Introduction block
# This block explains the purpose of the app
st.markdown("""
### 🧠 Your Smart Medical Companion
Welcome to **HEALTHIFY**, your AI-powered personal health assistant.  
Ask any health-related question and get **personalized, expert-style guidance** instantly.
""")

# Sidebar block
# This block collects user details
st.sidebar.header("📝 Enter Your Details")
name = st.sidebar.text_input("👤 Name")
gender = st.sidebar.selectbox("⚧ Gender", ["Male", "Female", "Other"])
age = st.sidebar.text_input("🎂 Age (yrs)")
weight = st.sidebar.text_input("⚖️ Weight (kg)")
height = st.sidebar.text_input("📏 Height (cm)")
fitness = st.sidebar.slider("💪 Rate your fitness (0-5)", 0, 5, step=1)

# BMI calculation block
# This block calculates BMI safely with error handling
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

# User query block
# This block takes user health question input
user_query = st.text_input("💬 Enter your health question here:")

# Prompt block
# This block prepares the prompt for AI model
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

Format:
* Start with a short comment on the details provided.
* Explain the real problem based on the query.
* Possible reasons for the problem.
* Possible solutions.
* Mention which doctor (specialization) to consult if needed.
* Strictly do not recommend medicines.
* Use bullet points and tables wherever required.
* End with a 5–7 line summary.
"""

# Response block
# This block generates AI response and displays it
if user_query:
    response = model.generate_content(prompt)
    st.markdown("## 🩺 AI Health Guidance")
    st.write(response.candidates[0].content.parts[0].text)

# Health insights block
# This block shows BMI and fitness insights
st.markdown("## 📊 Health Insights Dashboard")

col1, col2 = st.columns(2)

with col1:
    if bmi:
        if bmi < 18.5:
            st.warning("⚠️ Underweight: Consider balanced diet & strength training.")
        elif 18.5 <= bmi < 24.9:
            st.success("✅ Normal BMI: Keep maintaining your lifestyle!")
        elif 25 <= bmi < 29.9:
            st.warning("⚠️ Overweight: Focus on cardio & calorie control.")
        else:
            st.error("🚨 Obese: Consult a nutritionist & doctor.")

with col2:
    st.info(f"🏋️ Fitness Score: {fitness}/5")
    if fitness <= 2:
        st.write("👉 Start with light exercises like walking or yoga.")
    elif fitness <= 4:
        st.write("👉 Mix cardio + strength training for better results.")
    else:
        st.write("🔥 Excellent! Keep challenging yourself with advanced workouts.")

# Lifestyle tips block
# This block provides extra lifestyle recommendations
st.markdown("## 🌱 Lifestyle Recommendations")
st.write("""
- Drink at least 2–3 liters of water daily  
- Sleep 7–8 hours regularly  
- Include fruits and vegetables in diet  
- Avoid junk food and excess sugar  
- Practice meditation or breathing exercises  
""")

# Motivation block
# This block shows motivational quote
st.markdown("## 🌟 Daily Motivation")
st.success("“Your health is your wealth. Invest in it wisely!”")
