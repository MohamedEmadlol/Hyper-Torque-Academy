import streamlit as st
import random
import time
import pandas as pd
import os
from datetime import datetime

# --- 1. الإعدادات والبراندنج ---
st.set_page_config(page_title="Hyper Torque Pro LMS", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { border-radius: 15px; background-color: #ff4b4b; color: white; font-weight: bold; height: 3em; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #333; }
    h1, h2, h3 { color: #ff4b4b; text-align: center; font-family: 'Trebuchet MS'; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك حفظ البيانات ---
def save_log_to_csv(entry):
    file_path = 'hyper_torque_logs.csv'
    df = pd.DataFrame([entry])
    if not os.path.isfile(file_path):
        df.to_csv(file_path, index=False)
    else:
        df.to_csv(file_path, mode='a', header=False, index=False)

def load_logs():
    if os.path.isfile('hyper_torque_logs.csv'):
        # تحويل التاريخ والوقت لنصوص عشان ميبقاش فيه مشاكل في العرض
        df = pd.read_csv('hyper_torque_logs.csv')
        return df.to_dict('records')
    return []

# --- 3. مخزن الأسئلة ---
def get_questions(lesson):
    data = {
        "Fluid Mechanics 🌊": [
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
        ],
        "Electricity ⚡": [
            {"q": "What is the unit of electric current?", "options": ["Volt", "Ampere", "Ohm"], "a": "Ampere"},
        ]
    }
    return data.get(lesson, [])

# --- 4. تهيئة البيانات وتحميل الـ Logs ---
if 'records' not in st.session_state:
    st.session_state.records = load_logs()

# حساب النقط التراكمية
scores = {"Gryffindor 🦁": 0, "Slytherin 🐍": 0, "Hufflepuff 🦡": 0}
finished_students = set()
for r in st.session_state.records:
    # التأكد إن السكور رقم عشان ميعملش Error
    try:
        score_val = int(str(r['Score']).split('/')[0])
        scores[r['House']] += score_val
        finished_students.add(r['Student'])
    except: pass

st.session_state.global_scores = scores

# داتا بيز الطلاب
student_db = {"Mohamed Emad": "12-A", "Ahmed Ali": "12-B", "Sara Hassan": "12-A"}

# --- 5. Sidebar (الساعة + Recent Activity + Admin) ---
with st.sidebar:
    st.markdown("## ⚡ HYPER TORQUE PRO")
    st.markdown(f"**🕒 Server Clock:** `{datetime.now().strftime('%I:%M:%S %p')}`")
    
    st.markdown("---")
    st.markdown("### 🟢 Recent Activity")
    if st.session_state.records:
        # عرض آخر 5 عمليات دخول/تسليم
        recent = st.session_state.records[-5:]
        for log in reversed(recent):
            st.caption(f"✅ {log['Student']} finished with {log['Score']}")
    else:
        st.write("No activity yet.")
        
    st.markdown("---")
    if st.button("🏠 Global Dashboard"):
        st.session_state.page = "dashboard"; st.rerun()
    
    st.markdown("---")
    admin_input = st.text_input("Admin Access:", type="password")
    is_admin = (admin_input == "Admin2026")

# --- 6. التنقل بين الصفحات ---
if 'page' not in st.session_state: st.session_state.page = "login"

if is_admin:
    st.title("🛠️ COMMAND CENTER")
    t1, t2 = st.tabs(["Student Logs", "House Control"])
    with t1:
        if st.session_state.records: st.table(pd.DataFrame(st.session_state.records))
        else: st.info("No records.")
    with t2:
        h_sel = st.selectbox("House:", list(st.session_state.global_scores.keys()))
        adj = st.number_input("Adjust (+/-):", value=0)
        if st.button("Apply"):
            st.session_state.global_scores[h_sel] += adj; st.success("Updated!")

elif st.session_state.page == "dashboard":
    st.header("🏆 Live House Rankings")
    c1, c2, c3 = st.columns(3)
    for i, (h, s) in enumerate(st.session_state.global_scores.items()):
        with [c1, c2, c3][i]:
            st.markdown(f"<div class='stMetric'><h3>{h}</h3><h2>{s} Pts</h2></div>", unsafe_allow_html=True)
    if st.button("Back to Login"): st.session_state.page = "login"; st.rerun()

else:
    if 'user' not in st.session_state:
        st.markdown("<h1>⚡ STUDENT LOGIN</h1>", unsafe_allow_html=True)
        u_name = st.text_input("Full Official Name:")
        if st.button("Login"):
            if u_name in student_db:
                if u_name in finished_students: st.error("Attempt already recorded!")
                else:
                    st.session_state.user = u_name
                    # اختيار عشوائي للبيت لو مش متسجل
                    st.session_state.u_house = random.choice(["Gryffindor 🦁", "Slytherin 🐍", "Hufflepuff 🦡"])
                    st.rerun()
            else: st.error("Access Denied: Name not in Database.")
    else:
        st.markdown(f"### 🎊 Welcome, {st.session_state.user}")
        mode = st.radio("Activity:", ["Live Quiz 📝", "Assignment 📚"])
        lesson = st.selectbox("Lesson:", ["Fluid Mechanics 🌊", "Electricity ⚡"])
        
        if mode == "Live Quiz 📝":
            if 'active' not in st.session_state: st.session_state.active = False
            if not st.session_state.active:
                if st.text_input("Quiz Key:", type="password") == "Hyper2026":
                    if st.button("Start Mission"):
                        st.session_state.active = True
                        st.session_state.start = time.time()
                        st.session_state.qs = random.sample(get_questions(lesson), 10)
                        st.rerun()
            else:
                rem = (15*60) - (time.time() - st.session_state.start)
                if rem <= 0: st.session_state.active = False; st.rerun()
                st.sidebar.metric("⏳ Timer", f"{int(rem//60)}:{int(rem%60):02d}")
                with st.form("quiz"):
                    ans = {i: st.radio(f"Q{i+1}: {q['q']}", q['options']) for i, q in enumerate(st.session_state.qs)}
                    if st.form_submit_button("Submit"):
                        score = sum(1 for i, q in enumerate(st.session_state.qs) if ans[i] == q['a'])
                        log = {
                            "Student": st.session_state.user, 
                            "House": st.session_state.u_house, 
                            "Score": f"{score}/10", 
                            "Time": datetime.now().strftime("%I:%M %p")
                        }
                        save_log_to_csv(log)
                        st.session_state.records.append(log)
                        st.session_state.page = "dashboard"; st.rerun()
        else:
            for q in get_questions(lesson):
                st.write(f"**{q['q']}**")
                st.radio("Practice:", q['options'], key="as_"+q['q'])

        if st.button("Logout"): del st.session_state.user; st.rerun()
