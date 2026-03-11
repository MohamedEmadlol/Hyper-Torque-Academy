import streamlit as st
import random
import time
from datetime import datetime

# --- 1. الإعدادات والتصميم ---
st.set_page_config(page_title="Hyper Torque Pro LMS", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { border-radius: 15px; background-color: #ff4b4b; color: white; font-weight: bold; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #333; }
    h1, h2, h3 { color: #ff4b4b; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. مخزن الأسئلة (المكان اللي هتزود فيه براحتك) ---
def get_quiz_questions(lesson):
    if lesson == "Fluid Mechanics 🌊":
        return [
            {"q": "What is the SI unit of density?", "options": ["kg/m2", "kg/m3", "N/m2"], "a": "kg/m3"},
            {"q": "The continuity equation results from ____ conservation.", "options": ["Energy", "Mass", "Volume"], "a": "Mass"},
            {"q": "Pascal's Principle applies to?", "options": ["Solids", "Gases", "Confined Fluids"], "a": "Confined Fluids"},
            {"q": "Buoyant force direction?", "options": ["Down", "Up", "Side"], "a": "Up"},
            {"q": "If Area decreases, Velocity?", "options": ["Up", "Down", "Same"], "a": "Up"},
            {"q": "Archimedes' measures?", "options": ["Gravity", "Buoyant", "Friction"], "a": "Buoyant"},
            {"q": "Why is blood a fluid?", "options": ["Red", "Flows", "Iron"], "a": "Flows"},
            {"q": "If Area doubles, Velocity?", "options": ["Double", "Half", "Same"], "a": "Half"},
            {"q": "100 cm2 to m2?", "options": ["0.1", "0.01", "1.0"], "a": "0.01"},
            {"q": "Pressure = Force / ?", "options": ["Mass", "Volume", "Area"], "a": "Area"}
        ]
    elif lesson == "Electricity ⚡":
        return [
            {"q": "Question 1 for Electricity...", "options": ["A", "B", "C"], "a": "A"},
            # زود هنا باقي الـ 10 أسئلة لما تجهز الماتريال
        ]
    return []

# --- 3. تهيئة قواعد البيانات المؤقتة ---
if 'student_db' not in st.session_state:
    st.session_state.student_db = {"Mohamed Emad": "12-A", "Ahmed Ali": "12-B", "Sara Hassan": "12-A"}
if 'global_scores' not in st.session_state:
    st.session_state.global_scores = {"Gryffindor 🦁": 0, "Slytherin 🐍": 0, "Hufflepuff 🦡": 0}
if 'student_records' not in st.session_state:
    st.session_state.student_records = []
if 'finished_students' not in st.session_state:
    st.session_state.finished_students = set()
if 'view' not in st.session_state:
    st.session_state.view = "login"

# --- 4. Sidebar (Live Clock & Admin) ---
with st.sidebar:
    st.markdown("### ⚡ HYPER TORQUE PRO")
    st.markdown(f"**🕒 Server Time:** `{datetime.now().strftime('%I:%M:%S %p')}`")
    st.markdown("---")
    if st.button("🏠 Global Dashboard"):
        st.session_state.view = "dashboard"
        st.rerun()
    st.markdown("---")
    admin_pwd = st.text_input("Admin Access:", type="password")
    is_admin = (admin_pwd == "Admin2026")

# --- 5. منطق الصفحات ---
# [A] وضع المدرس
if is_admin:
    st.title("🛠️ COMMAND CENTER")
    tabs = st.tabs(["Scores Log", "House Points", "Schedules"])
    with tabs[0]:
        import pandas as pd
        if st.session_state.student_records: st.table(pd.DataFrame(st.session_state.student_records))
        else: st.info("No records yet.")
    with tabs[1]:
        h_sel = st.selectbox("House:", list(st.session_state.global_scores.keys()))
        adj = st.number_input("Adjust (+/-):", value=0)
        if st.button("Apply Changes"):
            st.session_state.global_scores[h_sel] += adj
            st.success("Updated!")

# [B] الـ Dashboard العام
elif st.session_state.view == "dashboard":
    st.header("🏆 Live House Rankings")
    cols = st.columns(3)
    for i, (h, s) in enumerate(st.session_state.global_scores.items()):
        cols[i].metric(h, f"{s} Pts")
    if st.button("Return to Login"):
        st.session_state.view = "login"
        st.rerun()

# [C] وضع الطالب
else:
    if 'logged_in_student' not in st.session_state:
        st.markdown("<h1>⚡ STUDENT LOGIN</h1>", unsafe_allow_html=True)
        login_name = st.text_input("Full Name:")
        if st.button("Access System"):
            if login_name in st.session_state.student_db:
                if login_name in st.session_state.finished_students:
                    st.error("Already completed!")
                else:
                    st.session_state.logged_in_student = login_name
                    st.session_state.user_house = random.choice(["Gryffindor 🦁", "Slytherin 🐍", "Hufflepuff 🦡"])
                    st.rerun()
            else: st.error("Name not in Database.")
    
    else:
        st.markdown(f"### 🎊 Welcome, {st.session_state.logged_in_student} ({st.session_state.user_house})")
        choice = st.radio("Activity:", ["Live Quiz 📝", "Assignment 📚"])
        lesson_choice = st.selectbox("Lesson:", ["Fluid Mechanics 🌊", "Electricity ⚡"])
        
        # --- بوابة الكويز ---
        if choice == "Live Quiz 📝":
            if 'quiz_active' not in st.session_state: st.session_state.quiz_active = False
            
            if not st.session_state.quiz_active:
                quiz_key = st.text_input("Enter Quiz Key:", type="password")
                if st.button("Start Quiz"):
                    if quiz_key == "Hyper2026":
                        st.session_state.quiz_active = True
                        st.session_state.start_time = time.time()
                        st.session_state.current_questions = random.sample(get_quiz_questions(lesson_choice), 10)
                        st.rerun()
            else:
                rem = (15 * 60) - (time.time() - st.session_state.start_time)
                if rem <= 0:
                    st.error("Time Up!"); st.session_state.finished_students.add(st.session_state.logged_in_student)
                    st.session_state.quiz_active = False; st.rerun()
                
                st.sidebar.metric("⏳ Timer", f"{int(rem//60)}:{int(rem%60):02d}")
                with st.form("quiz_form"):
                    user_ans = {}
                    for i, q in enumerate(st.session_state.current_questions):
                        user_ans[i] = st.radio(f"Q{i+1}: {q['q']}", q['options'], key=f"q{i}")
                    if st.form_submit_button("Submit Answers"):
                        score = sum(1 for i, q in enumerate(st.session_state.current_questions) if user_ans[i] == q['a'])
                        st.session_state.student_records.append({
                            "Student": st.session_state.logged_in_student, "Lesson": lesson_choice,
                            "Score": f"{score}/10", "Date": datetime.now().strftime("%Y-%m-%d %H:%M")
                        })
                        st.session_state.global_scores[st.session_state.user_house] += score
                        st.session_state.finished_students.add(st.session_state.logged_in_student)
                        st.session_state.quiz_active = False
                        st.session_state.view = "dashboard"
                        st.rerun()
        
        # --- بوابة الواجب ---
        elif choice == "Assignment 📚":
            st.info(f"Viewing Assignment for {lesson_choice}. (Points for practice, not house totals)")
            questions = get_quiz_questions(lesson_choice)
            for q in questions:
                st.write(f"**{q['q']}**")
                st.radio("Select:", q['options'], key="assign_"+q['q'])

        if st.button("Logout"):
            del st.session_state.logged_in_student
            st.rerun()
