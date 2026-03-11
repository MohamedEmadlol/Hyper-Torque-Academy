import streamlit as st
import random
import time
from datetime import datetime

# 1. إعدادات الصفحة والبراندنج
st.set_page_config(page_title="Hyper Torque Academy", page_icon="⚡", layout="wide")

# تصميم CSS احترافي (Dark Theme)
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #ff4b4b; color: white; font-weight: bold; }
    .house-stat { padding: 15px; border-radius: 10px; background: #1e2130; border-left: 5px solid #ff4b4b; margin-bottom: 10px; }
    h1, h2 { color: #ff4b4b; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة البيانات (Persistent Session Data) ---
if 'global_scores' not in st.session_state:
    st.session_state.global_scores = {"Gryffindor 🦁": 0, "Slytherin 🐍": 0, "Hufflepuff 🦡": 0}
if 'student_logs' not in st.session_state:
    st.session_state.student_logs = []
if 'recent_activity' not in st.session_state:
    st.session_state.recent_activity = []

# --- 3. القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.markdown("## ⚡ Hyper Torque Panel")
    
    # قسم النشاط المباشر (Recent Activity)
    st.markdown("### 🟢 Recent Activity")
    if st.session_state.recent_activity:
        for activity in reversed(st.session_state.recent_activity[-5:]):
            st.caption(activity)
    else:
        st.write("Waiting for first hero...")
    
    st.markdown("---")
    # دخول المدرس
    admin_pass = st.text_input("Teacher Access:", type="password")
    is_admin = (admin_pass == "Admin2026")

# --- 4. منطق عرض الصفحات ---
if is_admin:
    st.title("🛠️ Teacher Intelligence Dashboard")
    tab1, tab2, tab3 = st.tabs(["Student Results", "Points Control", "Class Schedules"])
    
    with tab1:
        import pandas as pd
        if st.session_state.student_logs:
            df = pd.DataFrame(st.session_state.student_logs)
            st.dataframe(df, use_container_width=True)
        else: st.info("No data yet.")
        
    with tab2:
        house_to_fix = st.selectbox("Select House:", list(st.session_state.global_scores.keys()))
        mod_points = st.number_input("Adjust Points:", value=0)
        if st.button("Update Scores"):
            st.session_state.global_scores[house_to_fix] += mod_points
            st.success("Points Updated!")

    with tab3:
        st.write("📅 Class Rotation: Grade 12A (Sun), 12B (Mon), 12C (Tue)")

# وضع الطالب (الرئيسي)
else:
    st.markdown("<h1>⚡ HYPER TORQUE ACADEMY</h1>", unsafe_allow_html=True)
    
    if 'registered' not in st.session_state: st.session_state.registered = False
    if 'submitted' not in st.session_state: st.session_state.submitted = False

    # المرحلة 1: التسجيل
    if not st.session_state.registered:
        st.markdown("### 📝 Student Identification")
        name = st.text_input("Full Official Name (No Nicknames):")
        s_class = st.selectbox("Class:", ["Grade 12 A", "Grade 12 B", "Grade 12 C"])
        house = st.selectbox("House:", ["Gryffindor 🦁", "Slytherin 🐍", "Hufflepuff 🦡"])
        if st.button("Initialize System"):
            if name:
                st.session_state.user_name, st.session_state.user_class, st.session_state.user_house, st.session_state.registered = name, s_class, house, True
                st.rerun()

    # المرحلة 2: الكويز أو النتيجة
    elif st.session_state.registered:
        # لو لسه مخلصش الكويز
        if not st.session_state.submitted:
            st.markdown(f"### 🎊 Welcome, **{st.session_state.user_name}**")
            st.write(f"🛡️ House: {st.session_state.user_house} | 📍 Class: {st.session_state.user_class}")
            
            if 'quiz_ready' not in st.session_state: st.session_state.quiz_ready = False
            
            if not st.session_state.quiz_ready:
                pwd = st.text_input("Authorization Code:", type="password")
                if st.button("Start 15-Min Timer"):
                    if pwd == "Hyper2026":
                        st.session_state.quiz_ready = True
                        st.session_state.start_time = time.time()
                        st.rerun()
            else:
                # التايمر والأسئلة
                rem = (15 * 60) - (time.time() - st.session_state.start_time)
                if rem <= 0: st.error("Time Up!"); st.stop()
                st.sidebar.metric("⏳ Timer", f"{int(rem//60)}:{int(rem%60):02d}")
                
                # الأسئلة
                with st.form("quiz"):
                    # (هنا بنك الأسئلة اللي اتفقنا عليه)
                    q1 = st.radio("Q1: SI unit of density?", ["kg/m2", "kg/m3", "N/m2"])
                    q2 = st.radio("Q2: Continuity equation conservation?", ["Energy", "Mass", "Volume"])
                    # ... بكمل بقية الـ 10 بنفس الطريقة
                    if st.form_submit_button("Submit Deployment"):
                        score = 0
                        if q1 == "kg/m3": score += 1
                        if q2 == "Mass": score += 1
                        # (حساب بقية الدرجات)
                        
                        # تسجيل في اللوج والنشاط
                        timestamp = datetime.now().strftime("%H:%M")
                        st.session_state.student_logs.append({
                            "Student": st.session_state.user_name, "Class": st.session_state.user_class, 
                            "House": st.session_state.user_house, "Score": score, "Time": timestamp
                        })
                        st.session_state.recent_activity.append(f"{timestamp} - {st.session_state.user_name} (Class {st.session_state.user_class}) finished!")
                        st.session_state.global_scores[st.session_state.user_house] += score
                        st.session_state.submitted = True
                        st.rerun()

        # المرحلة 3: بعد التسليم (Live Dashboard)
        else:
            st.markdown(f"## 🎯 Done! Your Score: {st.session_state.get('final_score', 'Saved')}")
            st.balloons()
            st.markdown("---")
            st.markdown("## 🏆 Live House Leaderboard")
            c1, c2, c3 = st.columns(3)
            houses = list(st.session_state.global_scores.keys())
            c1.metric(houses[0], f"{st.session_state.global_scores[houses[0]]} pts")
            c2.metric(houses[1], f"{st.session_state.global_scores[houses[1]]} pts")
            c3.metric(houses[2], f"{st.session_state.global_scores[houses[2]]} pts")
            
            if st.button("Back to Practice Mode"):
                st.session_state.submitted = False
                st.rerun()
