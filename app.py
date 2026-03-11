import streamlit as st
import random
import time
from datetime import datetime

# 1. إعدادات الصفحة والتصميم (The Branding & Design)
st.set_page_config(page_title="Hyper Torque Academy", page_icon="⚡", layout="wide")

# تصميم CSS احترافي للخلفية والألوان (Dark & Sleek Theme)
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border: none;
    }
    .stTextInput>div>div>input {
        background-color: #262730;
        color: white;
        border-radius: 10px;
    }
    .house-card {
        padding: 20px;
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
    }
    h1 { color: #ff4b4b; text-align: center; font-family: 'Arial Black'; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. البيانات الأساسية ---
if 'global_scores' not in st.session_state:
    st.session_state.global_scores = {"Gryffindor 🦁": 0, "Slytherin 🐍": 0, "Hufflepuff 🦡": 0}
if 'student_logs' not in st.session_state:
    st.session_state.student_logs = []

# --- 3. لوحة تحكم المدرس (Sidebar Admin) ---
with st.sidebar:
    st.markdown("# ⚡ Hyper Torque")
    st.markdown("---")
    admin_pass = st.text_input("Teacher Access:", type="password")
    if admin_pass == "Admin2026":
        st.success("Admin Mode Active")
        mode = st.radio("Navigation:", ["Student View", "Teacher Dashboard", "Points Control"])
    else:
        mode = "Student View"

# --- 4. وضع الطالب (Main View) ---
if mode == "Student View":
    # عرض اللوجو والترحيب
    st.markdown("<h1>⚡ HYPER TORQUE ACADEMY</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>Excellence in Physics & Engineering</p>", unsafe_allow_html=True)
    
    if 'registered' not in st.session_state:
        st.session_state.registered = False

    if not st.session_state.registered:
        with st.container():
            st.markdown("### 📝 Enter Your Credentials")
            name = st.text_input("Full Official Name:")
            s_class = st.selectbox("Your Class:", ["Grade 12 A", "Grade 12 B", "Grade 12 C"])
            house = st.selectbox("House Alignment:", ["Gryffindor 🦁", "Slytherin 🐍", "Hufflepuff 🦡"])
            
            if st.button("Initialize"):
                if name:
                    st.session_state.user_name, st.session_state.user_class, st.session_state.user_house, st.session_state.registered = name, s_class, house, True
                    st.rerun()
    else:
        # الترحيب الشخصي "أهلاً بك يا فلان"
        st.markdown(f"### 🎊 Welcome, **{st.session_state.user_name}**")
        st.markdown(f"🛡️ Member of House: **{st.session_state.user_house}** | 📍 Class: **{st.session_state.user_class}**")
        
        # بوابة الباسورد
        if 'quiz_started' not in st.session_state:
            st.session_state.quiz_started = False
        
        if not st.session_state.quiz_started:
            st.markdown("---")
            pwd = st.text_input("Session Authorization Code:", type="password")
            if st.button("Start Challenge"):
                if pwd == "Hyper2026":
                    st.session_state.quiz_started = True
                    st.session_state.start_time = time.time()
                    st.rerun()
                else:
                    st.error("Access Denied.")
        else:
            # تايمر حي وأسئلة
            rem = (15 * 60) - (time.time() - st.session_state.start_time)
            if rem <= 0:
                st.error("🛑 Time's up! Session Terminated.")
                st.stop()
            
            st.sidebar.metric("⏳ Timer", f"{int(rem//60)}:{int(rem%60):02d}")
            
            st.markdown("### 📝 Fluid Mechanics Quiz")
            # بنك الأسئلة (نفس الـ 10 السابقة)
            quiz_bank = [
                {"q": "What is the SI unit of density?", "options": ["kg/m2", "kg/m3", "N/m2"], "a": "kg/m3"},
                {"q": "Continuity equation is based on?", "options": ["Energy", "Mass", "Volume"], "a": "Mass"},
                {"q": "Pascal's Principle applies to?", "options": ["Solids", "Gases", "Confined Fluids"], "a": "Confined Fluids"},
                {"q": "Buoyant force direction?", "options": ["Down", "Up", "Side"], "a": "Up"},
                {"q": "If Area decreases, Velocity?", "options": ["Up", "Down", "Same"], "a": "Up"},
                {"q": "Archimedes' measures?", "options": ["Gravity", "Buoyant", "Friction"], "a": "Buoyant"},
                {"q": "Why is blood a fluid?", "options": ["Red", "Flows", "Iron"], "a": "Flows"},
                {"q": "If Area doubles, Velocity?", "options": ["Double", "Half", "Same"], "a": "Half"},
                {"q": "100 cm2 to m2?", "options": ["0.1", "0.01", "1.0"], "a": "0.01"},
                {"q": "Pressure = Force / ?", "options": ["Mass", "Volume", "Area"], "a": "Area"}
            ]

            if 'random_q' not in st.session_state:
                st.session_state.random_q = random.sample(quiz_bank, 10)

            with st.form("quiz"):
                ans = {}
                for i, q in enumerate(st.session_state.random_q):
                    ans[i] = st.radio(f"Q{i+1}: {q['q']}", q['options'], key=f"q{i}")
                
                if st.form_submit_button("Submit Deployment"):
                    score = sum(1 for i, q in enumerate(st.session_state.random_q) if ans[i] == q['a'])
                    # تسجيل البيانات
                    st.session_state.student_logs.append({
                        "Student": st.session_state.user_name, "Class": st.session_state.user_class,
                        "House": st.session_state.user_house, "Score": score,
                        "Time": datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    st.session_state.global_scores[st.session_state.user_house] += score
                    st.success(f"Mission Accomplished! Score: {score}/10")
                    st.balloons()

# --- 5. لوحة التحكم (Dashboard View) ---
elif mode == "Teacher Dashboard":
    st.header("📊 Intelligence Report")
    import pandas as pd
    if st.session_state.student_logs:
        df = pd.DataFrame(st.session_state.student_logs)
        selected_cls = st.selectbox("Class Filter:", ["All"] + list(df['Class'].unique()))
        if selected_cls != "All":
            df = df[df['Class'] == selected_cls]
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No active logs yet.")

elif mode == "Points Control":
    st.header("⚖️ Score Adjustment")
    h = st.selectbox("Select House:", list(st.session_state.global_scores.keys()))
    val = st.number_input("Points Adjustment:", value=0)
    if st.button("Update"):
        st.session_state.global_scores[h] += val
        st.success(f"Modified {h} by {val} pts.")
