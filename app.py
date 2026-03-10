import streamlit as st
import random
from datetime import datetime, timedelta
import time

# إعدادات الصفحة بلمسة هندسية
st.set_page_config(page_title="Hyper Torque Academy", page_icon="⚡", layout="wide")

# --- 1. قاعدة بيانات النقاط (تجمع النقاط طالما التطبيق يعمل) ---
if 'global_scores' not in st.session_state:
    st.session_state.global_scores = {"Gryffindor 🦁": 0, "Slytherin 🐍": 0, "Hufflepuff 🦡": 0}

# --- 2. بنك الأسئلة (10 أسئلة - النتيجة من 10) ---
quiz_bank = [
    {"q": "What is the SI unit of density?", "options": ["kg/m2", "kg/m3", "N/m2"], "a": "kg/m3"},
    {"q": "The continuity equation results from ____ conservation.", "options": ["Energy", "Mass", "Volume"], "a": "Mass"},
    {"q": "Pascal's Principle applies to?", "options": ["Solids", "Gases only", "Confined Fluids"], "a": "Confined Fluids"},
    {"q": "Buoyant force acts in which direction?", "options": ["Downward", "Sideways", "Upward"], "a": "Upward"},
    {"q": "If Area decreases, Velocity ____?", "options": ["Increases", "Decreases", "Stays same"], "a": "Increases"},
    {"q": "Archimedes' principle measures ____ force?", "options": ["Gravity", "Buoyant", "Friction"], "a": "Buoyant"},
    {"q": "Blood is considered a fluid because it?", "options": ["Is red", "Can flow", "Contains iron"], "a": "Can flow"},
    {"q": "In A1v1 = A2v2, if A2 is double A1, v2 is?", "options": ["Double v1", "Half v1", "Same as v1"], "a": "Half v1"},
    {"q": "100 cm2 is equal to how many m2?", "options": ["0.1", "0.01", "1.0"], "a": "0.01"},
    {"q": "Pressure is equal to Force divided by?", "options": ["Mass", "Volume", "Area"], "a": "Area"}
]

# --- 3. إدارة الحالة (State Management) ---
if 'registered' not in st.session_state:
    st.session_state.registered = False
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

st.title("⚡ Hyper Torque Academy")

# --- المرحلة الأولى: التسجيل ---
if not st.session_state.registered:
    st.info("⚠️ Note: Use official school name. Class format: 10-A.")
    name = st.text_input("Full Name:")
    s_class = st.text_input("Class (e.g. 10-A):")
    house = st.selectbox("House:", ["Gryffindor 🦁", "Slytherin 🐍", "Hufflepuff 🦡"])
    if st.button("Join House"):
        if name and s_class:
            st.session_state.user_name, st.session_state.user_house, st.session_state.registered = name, house, True
            st.rerun()
        else:
            st.error("Please fill in all details.")

# --- المرحلة الثانية: الباسورد والتايمر ---
else:
    st.success(f"Hi {st.session_state.user_name} | {st.session_state.user_house}")
    
    if not st.session_state.quiz_started:
        pwd = st.text_input("Enter Session Password to Start (15 min):", type="password")
        if pwd == "Hyper2026":
            st.session_state.quiz_started = True
            st.session_state.start_time = time.time()
            st.rerun()
        elif pwd != "":
            st.error("Wrong Password!")
    else:
        # حساب الوقت المتبقي
        time_limit = 15 * 60
        elapsed = time.time() - st.session_state.start_time
        remaining = time_limit - elapsed
        
        if remaining <= 0:
            st.error("🛑 Time's up! Session ended.")
            st.stop()
        
        # عرض التايمر في الجانب
        st.sidebar.metric("⏳ Time Remaining", f"{int(remaining // 60)}m {int(remaining % 60)}s")
        
        # --- المرحلة الثالثة: حل الكويز ---
        if not st.session_state.submitted:
            if 'random_q' not in st.session_state:
                st.session_state.random_q = random.sample(quiz_bank, 10)
            
            with st.form("quiz_form"):
                user_answers = {}
                for i, q in enumerate(st.session_state.random_q):
                    user_answers[i] = st.radio(f"Q{i+1}: {q['q']}", q['options'], key=f"q{i}")
                
                if st.form_submit_button("Submit Final Answers"):
                    current_score = 0
                    for i, q in enumerate(st.session_state.random_q):
                        if user_answers[i] == q['a']:
                            current_score += 1 # السؤال بنقطة واحدة
                    
                    st.session_state.final_score = current_score
                    st.session_state.global_scores[st.session_state.user_house] += current_score
                    st.session_state.submitted = True
                    st.rerun()
        
        # --- المرحلة الرابعة: النتيجة والـ Leaderboard ---
        else:
            st.header(f"🎯 Your Result: {st.session_state.final_score} / 10 Points")
            st.balloons()
            
            st.markdown("---")
            st.header("🏆 Live House Leaderboard (Weekly Total)")
            cols = st.columns(3)
            for i, (h, s) in enumerate(st.session_state.global_scores.items()):
                cols[i].metric(h, f"{s} Points Total")
            
            if st.button("Practice Again"):
                st.session_state.submitted = False
                st.rerun()
