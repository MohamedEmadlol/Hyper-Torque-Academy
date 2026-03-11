import streamlit as st
import random
import time
from datetime import datetime

# 1. إعدادات التصميم والبراندنج (Hyper Torque Theme)
st.set_page_config(page_title="Hyper Torque Pro System", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { border-radius: 15px; background-color: #ff4b4b; color: white; font-weight: bold; }
    .css-1n76uvr { background-color: #1e2130; } /* Sidebar background */
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #333; }
    h1, h2 { color: #ff4b4b; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. تهيئة قواعد البيانات (Database Initialization) ---
# أسماء الطلاب المعتمدين (Sample)
if 'student_db' not in st.session_state:
    st.session_state.student_db = {
        "Mohamed Emad": "12-A",
        "Ahmed Ali": "12-B",
        "Sara Hassan": "12-A",
        "Laila Omar": "12-C"
    }

if 'global_scores' not in st.session_state:
    st.session_state.global_scores = {"Gryffindor 🦁": 0, "Slytherin 🐍": 0, "Hufflepuff 🦡": 0}
if 'student_records' not in st.session_state:
    st.session_state.student_records = [] # سجلات دقيقة
if 'finished_students' not in st.session_state:
    st.session_state.finished_students = set() # لمنع الدخول المتكرر

# --- 3. الساعة الحية في الـ Sidebar (Live Clock) ---
with st.sidebar:
    st.markdown("### ⚡ HYPER TORQUE PRO")
    curr_time = datetime.now().strftime("%I:%M:%S %p")
    st.markdown(f"**📅 Date:** {datetime.now().strftime('%Y-%m-%d')}")
    st.markdown(f"**🕒 Server Time:** `{curr_time}`")
    
    st.markdown("---")
    # زرار العودة للـ Dashboard (مستقل)
    if st.button("🏠 Global Dashboard"):
        st.session_state.view = "dashboard"
        st.rerun()

    st.markdown("---")
    # لوحة تحكم المدرس
    admin_pwd = st.text_input("Admin Access:", type="password")
    is_admin = (admin_pwd == "Admin2026")

# --- 4. منطق الـ Navigation (التبديل بين الصفحات) ---
if 'view' not in st.session_state:
    st.session_state.view = "login"

# --- [وضع المدرس - Teacher Panels] ---
if is_admin:
    st.title("🛠️ COMMAND CENTER")
    adm_tab1, adm_tab2, adm_tab3, adm_tab4, adm_tab5 = st.tabs([
        "Live Quizzes", "Assignments", "Student Scores", "House Points", "Teacher Schedule"
    ])
    
    with adm_tab3: # سجل درجات الطلاب بالتفصيل
        import pandas as pd
        if st.session_state.student_records:
            st.table(pd.DataFrame(st.session_state.student_records))
        else: st.info("No records yet.")
        
    with adm_tab4: # تعديل النقط يدوياً (الخانة الرابعة)
        st.subheader("Manual Points Override")
        h_sel = st.selectbox("House:", list(st.session_state.global_scores.keys()))
        adj = st.number_input("Adjust (+/-):", value=0)
        if st.button("Apply Changes"):
            st.session_state.global_scores[h_sel] += adj
            st.success("Points updated in real-time!")
            
    with adm_tab5: # مواعيد الحصص
        st.write("📅 **Schedule:**")
        st.write("- Sun/Tue: Grade 12-A")
        st.write("- Mon/Wed: Grade 12-B")

# --- [الـ Dashboard العام] ---
elif st.session_state.view == "dashboard":
    st.header("🏆 Live House Rankings")
    c1, c2, c3 = st.columns(3)
    houses = list(st.session_state.global_scores.keys())
    c1.metric(houses[0], f"{st.session_state.global_scores[houses[0]]} Pts")
    c2.metric(houses[1], f"{st.session_state.global_scores[houses[1]]} Pts")
    c3.metric(houses[2], f"{st.session_state.global_scores[houses[2]]} Pts")
    if st.button("Return to Login"):
        st.session_state.view = "login"
        st.rerun()

# --- [وضع الطالب - Student Experience] ---
else:
    if 'logged_in_student' not in st.session_state:
        st.markdown("<h1>⚡ STUDENT LOGIN</h1>", unsafe_allow_html=True)
        login_name = st.text_input("Enter Full Name (Official):")
        if st.button("Access System"):
            if login_name in st.session_state.student_db:
                if login_name in st.session_state.finished_students:
                    st.error("Access Denied: You have already completed your attempt!")
                else:
                    st.session_state.logged_in_student = login_name
                    st.session_state.student_house = random.choice(["Gryffindor 🦁", "Slytherin 🐍", "Hufflepuff 🦡"]) # سيتم ربطه بالداتا بيز لاحقاً
                    st.rerun()
            else:
                st.error("❌ Access Denied: Name not in Database.")
    
    else:
        # شاشة اختيار (Quiz vs Assignment)
        st.markdown(f"### 🎊 Welcome, {st.session_state.logged_in_student}")
        choice = st.radio("Choose Activity:", ["Live Quiz 📝", "Assignments 📚"])
        
        lesson = st.selectbox("Select Lesson:", ["Fluid Mechanics 🌊", "Electricity ⚡ (Coming Soon)"])
        
        if choice == "Live Quiz 📝" and lesson == "Fluid Mechanics 🌊":
            quiz_pwd = st.text_input("Enter Quiz Key:", type="password")
            if st.button("Start Mission"):
                if quiz_pwd == "Hyper2026":
                    # منطق الكويز (الأسئلة والتايمر)
                    st.session_state.start_time = time.time()
                    st.success("Quiz Started! 15:00 on the clock.")
                    # (هنا نضع الأسئلة التي برمجناها سابقاً)
                    # عند الانتهاء:
                    # st.session_state.finished_students.add(st.session_state.logged_in_student)
                    # st.session_state.view = "dashboard"
        
        if st.button("Logout"):
            del st.session_state.logged_in_student
            st.rerun()
