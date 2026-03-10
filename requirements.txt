import streamlit as st
import random
import datetime

# إعدادات الصفحة بلمسة Hyper Torque
st.set_page_config(page_title="Hyper Torque Academy", page_icon="⚡", layout="wide")

# --- CSS لتجميل الواجهة وجعلها احترافية ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { border-radius: 10px; height: 3em; background-color: #1E1E1E; color: white; }
    .house-box { padding: 20px; border-radius: 15px; text-align: center; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- محاكاة لقاعدة البيانات (Activity Feed) ---
if 'history' not in st.session_state:
    st.session_state.history = []
if 'scores' not in st.session_state:
    st.session_state.scores = {"Gryffindor 🦁": 0, "Slytherin 🐍": 0, "Hufflepuff 🦡": 0}

# --- القائمة الجانبية (Sidebar) للرقابة والعدل ---
with st.sidebar:
    st.image("https://img.icons8.com/ios-filled/100/ffffff/lightning-bolt.png", width=100)
    st.title("🛡️ Integrity Hub")
    
    st.markdown("### 🟢 Recent Activity")
    if not st.session_state.history:
        st.write("No activity yet. Be the first!")
    for act in st.session_state.history[-5:]: # عرض آخر 5 دخلوا
        st.caption(f"{act['time']} - {act['house']} {act['name']} joined.")
    
    st.markdown("---")
    st.markdown("### 🎲 Challenge Tool")
    if st.button("Generate Random Number (1-20)"):
        num = random.randint(1, 20)
        st.header(f"🎯 Number: {num}")
        st.balloons()

# --- الجزء الرئيسي للموقع ---
st.title("⚡ Hyper Torque Academy: Fluid Mechanics")
st.write("Welcome to the Hogwarts of Engineering. Solve, Lead, and Earn Points for your House.")

# --- تسجيل الدخول ---
with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input("Full Name:")
    with col2:
        student_class = st.text_input("Class:")
    with col3:
        house = st.selectbox("Your House:", ["Gryffindor 🦁", "Slytherin 🐍", "Hufflepuff 🦡"])

# إضافة الدخول لشريط النشاط
if name and house and (not st.session_state.history or st.session_state.history[-1]['name'] != name):
    now = datetime.datetime.now().strftime("%H:%M")
    st.session_state.history.append({"name": name, "house": house, "time": now})

# --- أوضاع اللعب (Class vs Homework) ---
tab1, tab2 = st.tabs(["🔒 Live Class Activity", "📚 Homework & Achievements"])

with tab1:
    st.header("Live Challenge")
    code = st.text_input("Enter Session Password (From Eng. Mohamed):", type="password")
    
    if code == "Hyper2026": # كلمة السر للحصة
        st.success("Access Granted. Points are 2X in Live Mode!")
        
        # بنك أسئلة بسيط للمثال
        quiz_data = [
            {"q": "What stays constant in Pascal's Principle?", "options": ["Force", "Pressure", "Area"], "a": "Pressure"},
            {"q": "Continuity Equation is about conservation of...?", "options": ["Energy", "Mass", "Volume"], "a": "Mass"}
        ]
        
        with st.form("live_quiz"):
            score = 0
            for i, q in enumerate(quiz_data):
                ans = st.radio(f"Question {i+1}: {q['q']}", q['options'])
                if ans == q['a']: score += 20 # نقط مضاعفة في الحصة
            
            if st.form_submit_button("Submit Live Answers"):
                st.session_state.scores[house] += score
                st.success(f"House {house} gained {score} points!")
    else:
        st.warning("Locked. This section opens only during the session.")

with tab2:
    st.header("Practice & Achievements")
    st.info("Complete this to strengthen your house points. (One-time achievement per week)")
    
    if st.button("Start Weekly Practice"):
        st.write("Questions Loading based on Chapter 8 Material...")
        # هنا تضع الـ 10 أسئلة اللي جهزناهم
        st.write("✅ Practice complete. Your skills are growing!")

# --- لوحة المتصدرين (Leaderboard) ---
st.markdown("---")
st.header("🏆 House Leaderboard")
c1, c2, c3 = st.columns(3)
houses = list(st.session_state.scores.keys())
c1.metric(houses[0], f"{st.session_state.scores[houses[0]]} pts")
c2.metric(houses[1], f"{st.session_state.scores[houses[1]]} pts")
c3.metric(houses[2], f"{st.session_state.scores[houses[2]]} pts")
