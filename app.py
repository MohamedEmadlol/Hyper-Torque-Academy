import streamlit as st
import random
import time
import pandas as pd
import os
from datetime import datetime

# --- 1. إعدادات التصميم والبراندنج ---
st.set_page_config(page_title="Hyper Torque Pro LMS", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { border-radius: 15px; background-color: #ff4b4b; color: white; font-weight: bold; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #333; }
    h1, h2, h3 { color: #ff4b4b; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. نظام حفظ واستعادة البيانات (Persistent Database) ---
def save_log_to_csv(entry):
    file_path = 'student_logs.csv'
    df = pd.DataFrame([entry])
    if not os.path.isfile(file_path):
        df.to_csv(file_path, index=False)
    else:
        df.to_csv(file_path, mode='a', header=False, index=False)

def load_logs():
    if os.path.isfile('student_logs.csv'):
        return pd.read_csv('student_logs.csv').to_dict('records')
    return []

# --- 3. مخزن الأسئلة (زود هنا براحتك) ---
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
            {"q": "What is the unit of electric current?", "options": ["Volt", "Ampere", "Ohm"], "a": "Ampere"},
            # أضف بقية أسئلة الكهرباء هنا بنفس التنسيق
        ]
    return []

# --- 4. تهيئة الجلسة (Session Initialization) ---
if 'student_db' not in st.session_state:
    st.session_state.student_db = {"Mohamed Emad": "12-A", "Ahmed Ali": "12-B", "Sara Hassan": "12-A"}
if 'student_records' not in st.session_state:
    st.session_state.student_records = load_logs() # تحميل البيانات من الملف
if 'global_scores' not in st.session_state:
    # حساب النقاط بناءً على السجلات المحملة
    scores = {"Gryffindor 🦁": 0, "Slytherin 🐍": 0, "Hufflepuff 🦡": 0}
    for rec in st.session_state.student_records:
        scores[rec['House']] += int(rec['Score'].split('/')[0])
    st.session_state.global_scores = scores

if 'view' not in st.session_state: st.session_state.view = "login"
if 'finished_students' not in st.session_state:
    st.session_state.finished_students = {rec['Student'] for rec in st.session_state.student_records}

# --- 5. Sidebar (Admin & Live Clock) ---
with st.sidebar:
    st.markdown("### ⚡ HYPER TORQUE PRO")
    st.markdown(f"**🕒 Clock:** `{datetime.now().strftime('%I:%M:%S %p')}`")
    st.markdown("---")
    if st.button("🏠 Global Dashboard"):
        st.session_state.view = "dashboard"
        st.rerun()
    st.markdown("---")
    admin_pwd = st.text_input("Admin Access:", type="password")
    is_admin = (admin_pwd == "Admin2026")

# --- 6. الصفحات ---
if is_admin:
    st.title("🛠️ COMMAND CENTER")
    t1, t2, t3, t4 = st.tabs(["Scores Log", "House Points", "Schedule", "Manual Adjust"])
    with t1:
        if st.session_state.student_records:
            st.table(pd.DataFrame(st.session_state.student_records))
        else: st.info("No logs.")
    with t4:
        h_sel = st.selectbox("House:", list(st.session_state.global_scores.keys()))
        adj = st.number_input("Adjust (+/-):", value=0)
        if st.button("Apply"):
            st.session_state.global_scores[h_sel] += adj; st.success("Updated!")

elif st.session_state.view == "dashboard":
    st.header("🏆 Live House Rankings")
    cols = st.columns(3)
    for i, (h, s) in enumerate(st.session_state.global_scores.items()):
        cols[i].metric(h, f"{s} Pts")
    if st.button("Back to Login"): st.session_state.view = "login"; st.rerun()

else:
    # [نظام الطالب: لوجن -> اختيار درس -> واجب أو كويز]
    if 'logged_in_student' not in st.session_state:
        st.markdown("<h1>⚡ STUDENT LOGIN</h1>", unsafe_allow_html=True)
        login_name = st.text_input("Full Name:")
        if st.button("Login"):
            if login_name in st.session_state.student_db:
                if login_name in st.session_state.finished_students:
                    st.error("Attempt already recorded!")
                else:
                    st.session_state.logged_in_student = login_name
                    st.session_state.user_house = random.choice(["Gryffindor 🦁", "Slytherin 🐍", "Hufflepuff 🦡"])
                    st.rerun()
            else: st.error("Access Denied.")
    else:
        st.markdown(f"### 🎊 Welcome, {st.session_state.logged_in_student}")
        choice = st.radio("Activity:", ["Live Quiz 📝", "Assignment 📚"])
        lesson_choice = st.selectbox("Lesson:", ["Fluid Mechanics 🌊", "Electricity ⚡"])

        if choice == "Live Quiz 📝":
            if 'quiz_active' not in st.session_state: st.session_state.quiz_active = False
            if not st.session_state.quiz_active:
                if st.text_input("Quiz Key:", type="password") == "Hyper2026":
                    if st.button("Start"):
                        st.session_state.quiz_active = True
                        st.session_state.start_time = time.time()
                        st.session_state.q_list = random.sample(get_quiz_questions(lesson_choice), 10)
                        st.rerun()
            else:
                rem = (15*60) - (time.time() - st.session_state.start_time)
                if rem <= 0: st.session_state.quiz_active = False; st.rerun()
                st.sidebar.metric("⏳ Timer", f"{int(rem//60)}:{int(rem%60):02d}")
                with st.form("q_form"):
                    ans = {i: st.radio(f"Q{i+1}: {q['q']}", q['options']) for i, q in enumerate(st.session_state.q_list)}
                    if st.form_submit_button("Submit"):
                        score = sum(1 for i, q in enumerate(st.session_state.q_list) if ans[i] == q['a'])
                        entry = {"Student": st.session_state.logged_in_student, "House": st.session_state.user_house, "Score": f"{score}/10", "Date": datetime.now().strftime("%Y-%m-%d %H:%M")}
                        save_log_to_csv(entry) # الحفظ في الملف
                        st.session_state.student_records.append(entry)
                        st.session_state.global_scores[st.session_state.user_house] += score
                        st.session_state.finished_students.add(st.session_state.logged_in_student)
                        st.session_state.quiz_active = False; st.session_state.view = "dashboard"; st.rerun()
        
        elif choice == "Assignment 📚":
            for q in get_quiz_questions(lesson_choice):
                st.write(f"**{q['q']}**")
                st.radio("Options:", q['options'], key="as_"+q['q'])

        if st.button("Logout"): del st.session_state.logged_in_student; st.rerun()
