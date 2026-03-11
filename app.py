import streamlit as st
import random
import time
import pandas as pd
import os
from datetime import datetime

# --- 1. الإعدادات والبراندنج (Hyper Torque Style) ---
st.set_page_config(page_title="Hyper Torque Pro LMS", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { border-radius: 15px; background-color: #ff4b4b; color: white; font-weight: bold; height: 3em; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #333; }
    h1, h2, h3 { color: #ff4b4b; text-align: center; font-family: 'Trebuchet MS'; }
    .timer-box { background-color: #1e2130; padding: 10px; border-radius: 10px; border: 2px solid #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك حفظ البيانات ---
def save_log_to_csv(entry):
    file_path = 'hyper_torque_final_db.csv'
    df = pd.DataFrame([entry])
    if not os.path.isfile(file_path):
        df.to_csv(file_path, index=False)
    else:
        df.to_csv(file_path, mode='a', header=False, index=False)

def load_logs():
    file_path = 'hyper_torque_final_db.csv'
    if os.path.isfile(file_path):
        return pd.read_csv(file_path).to_dict('records')
    return []

# --- 3. قاعدة بيانات الطلاب والبيوت (التحكم الأساسي) ---
STUDENT_DB = {
    "12-A": ["Mohamed Emad", "Ahmed Ali", "Sara Hassan"],
    "12-B": ["Eren Yeager", "Mikasa Ackerman", "Armin Arlert"],
    "12-C": ["Levi Ackerman", "Erwin Smith", "Hange Zoe"]
}

CLASS_HOUSES = {
    "12-A": ["Gryffindor 🦁", "Slytherin 🐍", "Hufflepuff 🦡"],
    "12-B": ["Scout Regiment ⚔️", "Military Police 🦄", "Garrison 🌹"],
    "12-C": ["Survey Corps 🕊️", "Wall Rose 🏰", "Wall Maria 🧱"]
}

# --- 4. مخزن الأسئلة (أكبر عشان التوزيع العشوائي) ---
def get_all_questions():
    """مخزن شامل للأسئلة - 20 سؤال عشان نختار 10 عشوائية"""
    all_questions = [
        {"q": "What is the SI unit of density?", "options": ["kg/m2", "kg/m3", "N/m2"], "a": "kg/m3"},
        {"q": "The continuity equation results from ____ conservation.", "options": ["Energy", "Mass", "Volume"], "a": "Mass"},
        {"q": "Pascal's Principle applies to?", "options": ["Solids", "Gases", "Confined Fluids"], "a": "Confined Fluids"},
        {"q": "Buoyant force direction?", "options": ["Down", "Up", "Side"], "a": "Up"},
        {"q": "If Area decreases, Velocity?", "options": ["Up", "Down", "Same"], "a": "Up"},
        {"q": "Archimedes' measures?", "options": ["Gravity", "Buoyant", "Friction"], "a": "Buoyant"},
        {"q": "Why is blood a fluid?", "options": ["Red", "Flows", "Iron"], "a": "Flows"},
        {"q": "If Area doubles, Velocity?", "options": ["Double", "Half", "Same"], "a": "Half"},
        {"q": "100 cm2 to m2?", "options": ["0.1", "0.01", "1.0"], "a": "0.01"},
        {"q": "Pressure = Force / ?", "options": ["Mass", "Volume", "Area"], "a": "Area"},
        {"q": "Bernoulli's equation relates to?", "options": ["Energy", "Momentum", "Force"], "a": "Energy"},
        {"q": "Viscosity measures?", "options": ["Flow resistance", "Density", "Pressure"], "a": "Flow resistance"},
        {"q": "Laminar flow is characterized by?", "options": ["Smooth layers", "Turbulence", "High speed"], "a": "Smooth layers"},
        {"q": "Turbulent flow has?", "options": ["High Reynolds number", "Low Reynolds number", "No friction"], "a": "High Reynolds number"},
        {"q": "Streamline flow means?", "options": ["Particles follow same path", "Random motion", "High speed"], "a": "Particles follow same path"},
        {"q": "The equation of continuity is based on?", "options": ["Mass conservation", "Energy conservation", "Momentum conservation"], "a": "Mass conservation"},
        {"q": "Dynamic pressure is given by?", "options": ["1/2 ρv²", "ρgh", "P + ρgh"], "a": "1/2 ρv²"},
        {"q": "Stokes' law applies to?", "options": ["Small spheres in fluid", "Large objects", "Gases only"], "a": "Small spheres in fluid"},
        {"q": "Terminal velocity occurs when?", "options": ["Drag = Weight", "Drag = 0", "Weight = 0"], "a": "Drag = Weight"},
        {"q": "Reynolds number determines?", "options": ["Flow type", "Temperature", "Pressure"], "a": "Flow type"}
    ]
    return all_questions

def get_random_questions(lesson, count=10):
    """اختيار 10 أسئلة عشوائية من المخزن"""
    all_q = get_all_questions()
    return random.sample(all_q, count)

# --- 5. تهيئة البيانات وحساب النقاط ---
if 'records' not in st.session_state:
    st.session_state.records = load_logs()

global_scores = {}
finished_ids = set()
for houses in CLASS_HOUSES.values():
    for h in houses: global_scores[h] = 0

for r in st.session_state.records:
    try:
        h_name = r['House']
        if r['Student'] == "ADMIN_ADJUST":
            global_scores[h_name] += int(r['Score'])
        else:
            score_val = int(str(r['Score']).split('/')[0])
            global_scores[h_name] += score_val
            finished_ids.add(f"{r['Student']}_{r['Class']}")
    except: pass

st.session_state.global_scores = global_scores

# --- 6. Sidebar (الساعة + Recent Activity + Admin) ---
with st.sidebar:
    st.markdown("## ⚡ HYPER TORQUE PRO")
    st.markdown(f"**🕒 Clock:** `{datetime.now().strftime('%I:%M:%S %p')}`")
    
    st.markdown("---")
    st.markdown("### 🟢 Recent Activity")
    if st.session_state.records:
        student_only = [r for r in st.session_state.records if r['Student'] != "ADMIN_ADJUST"]
        recent = student_only[-5:]
        for log in reversed(recent):
            st.caption(f"📅 {log['Date']} | {log['Time']}")
            st.write(f"✅ **{log['Student']}** ({log['Class']})")
            st.markdown(f"🎯 Score: `{log['Score']}`")
            st.markdown("---")
    else:
        st.write("No activity yet.")
        
    st.markdown("---")
    if st.button("🏠 Dashboard"): st.session_state.page = "dashboard"; st.rerun()
    admin_input = st.text_input("Admin Access:", type="password")
    is_admin = (admin_input == "Admin2026")

# --- 7. الصفحات ---
if 'page' not in st.session_state: st.session_state.page = "login"

if is_admin:
    st.title("🛠️ COMMAND CENTER")
    t1, t2 = st.tabs(["Student Records", "House Control"])
    with t1: st.dataframe(pd.DataFrame(st.session_state.records))
    with t2:
        h_sel = st.selectbox("Select House:", list(st.session_state.global_scores.keys()))
        adj = st.number_input("Adjust Points:", value=0)
        if st.button("Apply & Save"):
            entry = {"Student": "ADMIN_ADJUST", "Class": "SYSTEM", "House": h_sel, "Score": adj, "Date": datetime.now().strftime("%Y-%m-%d"), "Time": datetime.now().strftime("%I:%M:%S %p")}
            save_log_to_csv(entry); st.session_state.records.append(entry); st.rerun()

elif st.session_state.page == "dashboard":
    st.header("🏆 Live Global Leaderboard")
    sorted_houses = sorted(st.session_state.global_scores.items(), key=lambda x: x[1], reverse=True)
    cols = st.columns(3)
    for i, (h, s) in enumerate(sorted_houses):
        with cols[i % 3]:
            st.markdown(f"<div class='stMetric'><h4>{h}</h4><h2>{s} Pts</h2></div>", unsafe_allow_html=True)
    if st.button("🚪 Logout"):
        if 'user' in st.session_state: del st.session_state.user
        st.session_state.page = "login"; st.rerun()

else:
    if 'user' not in st.session_state:
        st.markdown("<h1>⚡ STUDENT LOGIN</h1>", unsafe_allow_html=True)
        u_class = st.selectbox("Select Your Class:", list(STUDENT_DB.keys()))
        u_name = st.selectbox("Select Your Name:", STUDENT_DB[u_class])
        u_house = st.selectbox("Choose Your House:", CLASS_HOUSES[u_class])
        if st.button("Login"):
            st.session_state.user, st.session_state.u_class, st.session_state.u_house = u_name, u_class, u_house
            st.rerun()
    else:
        st.markdown(f"### 🎊 Welcome, {st.session_state.user} | {st.session_state.u_house}")
        mode = st.radio("Activity:", ["Live Quiz 📝", "Assignment 📚"])
        lesson = "Fluid Mechanics 🌊"
        
        if mode == "Live Quiz 📝":
            user_id = f"{st.session_state.user}_{st.session_state.u_class}"
            if user_id in finished_ids:
                st.error("🛑 Quiz already submitted! Check your score in the Dashboard.")
            else:
                # --- تهيئة حالة الاختبار ---
                if 'quiz_active' not in st.session_state: st.session_state.quiz_active = False
                if 'quiz_questions' not in st.session_state: st.session_state.quiz_questions = []
                if 'quiz_answers' not in st.session_state: st.session_state.quiz_answers = {}
                if 'quiz_start_time' not in st.session_state: st.session_state.quiz_start_time = None
                
                if not st.session_state.quiz_active:
                    if st.text_input("Quiz Key:", type="password") == "Hyper2026" and st.button("Start Mission"):
                        st.session_state.quiz_active = True
                        st.session_state.quiz_start_time = time.time()
                        st.session_state.quiz_questions = get_random_questions(lesson, 10)
                        st.session_state.quiz_answers = {}
                        st.rerun()
                else:
                    # --- عرض الأسئلة مع التايمر الدقيق ---
                    elapsed = time.time() - st.session_state.quiz_start_time
                    total_time = 15 * 60  # 15 دقيقة
                    remaining = max(0, total_time - elapsed)
                    minutes = int(remaining // 60)
                    seconds = int(remaining % 60)
                    
                    # عرض التايمر بشكل بارز
                    st.markdown(f"""
                        <div class='timer-box'>
                            <h3>⏳ Time Remaining: {minutes}:{seconds:02d}</h3>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # عرض الأسئلة
                    with st.form("quiz"):
                        for i, q in enumerate(st.session_state.quiz_questions):
                            if i not in st.session_state.quiz_answers:
                                st.session_state.quiz_answers[i] = None
                            ans = st.radio(
                                f"Q{i+1}: {q['q']}", 
                                q['options'], 
                                key=f"q_{i}",
                                label_visibility="collapsed"
                            )
                            st.session_state.quiz_answers[i] = ans
                        
                        if st.form_submit_button("Submit Deployment"):
                            # حساب النتيجة
                            score = sum(1 for i, q in enumerate(st.session_state.quiz_questions) 
                                       if st.session_state.quiz_answers.get(i) == q['a'])
                            
                            # حفظ النتيجة
                            log = {
                                "Student": st.session_state.user, 
                                "Class": st.session_state.u_class, 
                                "House": st.session_state.u_house, 
                                "Score": f"{score}/10", 
                                "Date": datetime.now().strftime("%Y-%m-%d"), 
                                "Time": datetime.now().strftime("%I:%M:%S %p")
                            }
                            save_log_to_csv(log)
                            st.session_state.records.append(log)
                            finished_ids.add(user_id)
                            st.session_state.quiz_active = False
                            st.success(f"✅ Submission Complete! Your Score: {score}/10")
                            st.rerun()
                            
        else:
            # وضع التدريب (Practice Mode)
            st.info("📚 Practice Mode: No score will be recorded.")
            for q in get_random_questions(lesson, 10):
                st.write(f"**{q['q']}**")
                st.radio("Practice:", q['options'], key="as_"+q['q'])
        
        if st.button("Logout"): 
            # تنظيف حالة الاختبار
            st.session_state.quiz_active = False
            st.session_state.quiz_questions = []
            st.session_state.quiz_answers = {}
            st.session_state.quiz_start_time = None
            del st.session_state.user
            st.rerun()
