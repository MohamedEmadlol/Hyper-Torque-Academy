import streamlit as st
import random
import time
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(page_title="Hyper Torque Admin System", page_icon="⚡", layout="wide")

# --- 1. قاعدة بيانات النظام (تخزين مؤقت للديمو) ---
if 'global_scores' not in st.session_state:
    st.session_state.global_scores = {"Gryffindor 🦁": 0, "Slytherin 🐍": 0, "Hufflepuff 🦡": 0}
if 'student_logs' not in st.session_state:
    st.session_state.student_logs = [] # سجل درجات الطلاب

# --- 2. بنك الأسئلة ---
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

# --- 3. القائمة الجانبية (Admin Panel) ---
st.sidebar.title("🛠️ Teacher Control")
admin_pass = st.sidebar.text_input("Admin Password:", type="password")

if admin_pass == "Admin2026": # باسوورد المدرس
    st.sidebar.success("Logged in as Admin")
    mode = st.sidebar.radio("Navigate to:", ["Student View", "Teacher Dashboard", "Manual Score Adjust"])
else:
    mode = "Student View"

# --- 4. وضع المدرس (Teacher Dashboard) ---
if mode == "Teacher Dashboard":
    st.header("📊 Detailed Student Results")
    if st.session_state.student_logs:
        import pandas as pd
        df = pd.DataFrame(st.session_state.student_logs)
        
        # فلترة حسب الفصل
        selected_class = st.selectbox("Filter by Class:", ["All", "Grade 12 A", "Grade 12 B", "Grade 12 C"])
        if selected_class != "All":
            df = df[df['Class'] == selected_class]
        
        st.table(df)
    else:
        st.info("No records found yet.")

elif mode == "Manual Score Adjust":
    st.header("⚖️ Manual Points Adjustment")
    target_house = st.selectbox("Select House to Adjust:", list(st.session_state.global_scores.keys()))
    points_to_add = st.number_input("Points (+/-):", value=0)
    if st.button("Update Points"):
        st.session_state.global_scores[target_house] += points_to_add
        st.success(f"Updated {target_house} by {points_to_add} points.")

# --- 5. وضع الطالب (Student View) ---
else:
    if 'registered' not in st.session_state:
        st.session_state.registered = False
    
    if not st.session_state.registered:
        st.info("📅 Today is: " + datetime.now().strftime("%A, %d %B %Y"))
        name = st.text_input("Full Name (Official):")
        s_class = st.selectbox("Select Your Class:", ["Grade 12 A", "Grade 12 B", "Grade 12 C"])
        house = st.selectbox("House:", ["Gryffindor 🦁", "Slytherin 🐍", "Hufflepuff 🦡"])
        if st.button("Enter Quiz"):
            if name:
                st.session_state.user_name, st.session_state.user_class, st.session_state.user_house, st.session_state.registered = name, s_class, house, True
                st.rerun()
    else:
        # الكويز (نفس المنطق السابق مع إضافة الوقت)
        if 'quiz_started' not in st.session_state:
            st.session_state.quiz_started = False
        
        if not st.session_state.quiz_started:
            pwd = st.text_input("Enter Session Password:", type="password")
            if pwd == "Hyper2026":
                st.session_state.quiz_started = True
                st.session_state.start_time = time.time()
                st.rerun()
        else:
            # تايمر وأسئلة
            remaining = (15 * 60) - (time.time() - st.session_state.start_time)
            if remaining <= 0:
                st.error("Time Up!")
                st.stop()
            
            st.sidebar.metric("⏳ Time Left", f"{int(remaining//60)}m {int(remaining%60)}s")
            
            if 'random_q' not in st.session_state:
                st.session_state.random_q = random.sample(quiz_bank, 10)
            
            with st.form("quiz"):
                answers = {}
                for i, q in enumerate(st.session_state.random_q):
                    answers[i] = st.radio(f"Q{i+1}: {q['q']}", q['options'], key=f"q{i}")
                
                if st.form_submit_button("Submit"):
                    score = sum(1 for i, q in enumerate(st.session_state.random_q) if answers[i] == q['a'])
                    
                    # تسجيل البيانات مع الوقت والتاريخ
                    log_entry = {
                        "Student": st.session_state.user_name,
                        "Class": st.session_state.user_class,
                        "House": st.session_state.user_house,
                        "Score": f"{score}/10",
                        "Date": datetime.now().strftime("%Y-%m-%d"),
                        "Time": datetime.now().strftime("%H:%M:%S")
                    }
                    st.session_state.student_logs.append(log_entry)
                    st.session_state.global_scores[st.session_state.user_house] += score
                    
                    st.success(f"Score: {score}/10. Points added to {st.session_state.user_house}!")
                    st.balloons()
