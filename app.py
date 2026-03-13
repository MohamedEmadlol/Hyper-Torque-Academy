import streamlit as st
import random
import time
import pandas as pd
import os
from datetime import datetime
import pytz

# --- 1. الإعدادات والبراندنج ---
st.set_page_config(page_title="Hyper Torque Academy", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { border-radius: 15px; background-color: #ff4b4b; color: white; font-weight: bold; height: 3em; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 2px solid #ff4b4b; }
    h1, h2, h3 { color: #ff4b4b; text-align: center; font-family: 'Trebuchet MS'; }
    .timer-box { background-color: #1e2130; padding: 10px; border-radius: 10px; border: 2px solid #ff4b4b; text-align: center; margin-bottom: 20px; }
    .result-box { background-color: #1e2130; padding: 20px; border-radius: 15px; border: 3px solid #00ff88; margin: 20px 0; text-align: center; }
    .correct { color: #00ff88; font-weight: bold; }
    .wrong { color: #ff4b4b; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

egy_tz = pytz.timezone('Africa/Cairo')

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
        try: return pd.read_csv(file_path).to_dict('records')
        except: return []
    return []

# --- 3. قاعدة البيانات ---
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

# --- 4. مخزن الأسئلة الشامل (Master Bank) ---
def get_questions_by_lesson():
    return {
        "Fluid Mechanics 🌊": [
            # مسائل حسابية (Calculations) من الصور
            {"q": "A hydraulic lift has a small piston area (A1) of 0.20 m² and a large piston area (A2) of 0.90 m². If a force (F2) of 1.20 x 10⁴ N is supported, calculate F1.", "options": ["2.7 x 10³ N", "5.4 x 10³ N", "1.5 x 10³ N", "2.7 x 10² N"], "a": "2.7 x 10³ N"},
            {"q": "If the radius of the large piston in a hydraulic press is 4 times the radius of the small piston, what is the force multiplication factor?", "options": ["16 times", "4 times", "8 times", "2 times"], "a": "16 times"},
            {"q": "A crown weighs 7.84 N in air and 6.86 N in water. Calculate the density of the crown (ρ_water = 1000 kg/m³).", "options": ["8.0 x 10³ kg/m³", "19.3 x 10³ kg/m³", "10.0 x 10³ kg/m³", "7.8 x 10³ kg/m³"], "a": "8.0 x 10³ kg/m³"},
            {"q": "Water flows through a pipe at 2 m/s. If the pipe narrows to 1/4 of its original area, what is the new velocity?", "options": ["8 m/s", "4 m/s", "0.5 m/s", "16 m/s"], "a": "8 m/s"},
            {"q": "Calculate the absolute pressure at a depth of 10m in water. (P_atm = 1.01 x 10⁵ Pa, ρ=1000, g=9.8)", "options": ["1.99 x 10⁵ Pa", "0.98 x 10⁵ Pa", "1.01 x 10⁵ Pa", "2.50 x 10⁵ Pa"], "a": "1.99 x 10⁵ Pa"},
            {"q": "A block of wood (ρ = 700 kg/m³) floats in water. What percentage of the block is submerged?", "options": ["70%", "30%", "100%", "50%"], "a": "70%"},
            {"q": "If a fluid's speed increases from 2 m/s to 6 m/s in a horizontal pipe, the pressure in the fast-moving region will:", "options": ["Decrease", "Increase", "Remain same", "Double"], "a": "Decrease"},
            # أسئلة التريكات (Tricky)
            {"q": "An iron ball and an aluminum ball of the same VOLUME are submerged in water. Which experiences a greater buoyant force?", "options": ["Both the same", "Iron ball", "Aluminum ball", "Depends on mass"], "a": "Both the same"},
            {"q": "If the diameter of a pipe is doubled, the cross-sectional area increases by:", "options": ["4 times", "2 times", "8 times", "16 times"], "a": "4 times"},
            {"q": "According to Pascal's Principle, pressure applied to a fluid in a closed container is transmitted equally to:", "options": ["Every point in the fluid", "The bottom only", "The walls only", "The pistons only"], "a": "Every point in the fluid"},
            {"q": "A boat moves from fresh water (ρ=1000) to salt water (ρ=1025). The buoyant force on the boat will:", "options": ["Stay the same (it still floats)", "Increase", "Decrease", "Become zero"], "a": "Stay the same (it still floats)"},
            {"q": "The continuity equation (A1v1 = A2v2) is a statement of the conservation of:", "options": ["Mass", "Energy", "Momentum", "Pressure"], "a": "Mass"},
            {"q": "As an object sinks deeper into a fluid (fully submerged), the buoyant force on it:", "options": ["Remains constant", "Increases", "Decreases", "Becomes zero"], "a": "Remains constant"},
            {"q": "Gauge pressure is defined as:", "options": ["P_total - P_atm", "P_total + P_atm", "P_atm - P_total", "P_total / P_atm"], "a": "P_total - P_atm"},
            {"q": "Which of these is NOT a fluid?", "options": ["Steel sphere", "Water vapor", "Olive oil", "Atmospheric air"], "a": "Steel sphere"}
        ],
        "Electricity ⚡": [
            {"q": "What is the SI unit of electric current?", "options": ["Volt", "Ampere", "Ohm"], "a": "Ampere"},
            {"q": "Ohm's law states V = ?", "options": ["IR", "I/R", "R/I"], "a": "IR"},
            {"q": "Resistance depends on?", "options": ["Length", "Area", "Both"], "a": "Both"},
        ]
    }

# --- 5. تهيئة البيانات وحساب النقاط ---
if 'records' not in st.session_state:
    st.session_state.records = load_logs()

global_scores = {}
finished_ids = set()
for houses in CLASS_HOUSES.values():
    for h in houses: global_scores[h] = 0

for r in st.session_state.records:
    try:
        h_name = r.get('House', '')
        if r.get('Student') == "ADMIN_ADJUST":
            global_scores[h_name] += int(r.get('Score', 0))
        else:
            score_val = int(str(r.get('Score', '0')).split('/')[0])
            global_scores[h_name] += score_val
            finished_ids.add(f"{r.get('Student', '')}_{r.get('Class', '')}")
    except: pass
st.session_state.global_scores = global_scores

# --- 6. Sidebar ---
with st.sidebar:
    st.markdown("## ⚡ HYPER TORQUE ACADEMY")
    st.markdown(f"**🕒 Clock:** `{datetime.now(egy_tz).strftime('%I:%M:%S %p')}`")
    st.markdown("---")
    if st.button("🏠 Global Dashboard"): st.session_state.page = "dashboard"; st.rerun()
    admin_input = st.text_input("Admin Access:", type="password")
    is_admin = (admin_input == "Admin2026")

# --- 7. منطق الصفحات ---
if 'page' not in st.session_state: st.session_state.page = "login"

if is_admin:
    st.title("🛠️ COMMAND CENTER")
    st.dataframe(pd.DataFrame(st.session_state.records))
    h_sel = st.selectbox("House:", list(st.session_state.global_scores.keys()))
    adj = st.number_input("Adjust:", value=0)
    if st.button("Apply"):
        now_egy = datetime.now(egy_tz)
        entry = {"Student": "ADMIN_ADJUST", "Class": "SYSTEM", "House": h_sel, "Score": adj, "Date": now_egy.strftime("%Y-%m-%d"), "Time": now_egy.strftime("%I:%M:%S %p")}
        save_log_to_csv(entry); st.session_state.records.append(entry); st.rerun()

elif st.session_state.page == "dashboard":
    st.header("🏆 Live Global Leaderboard")
    sorted_h = sorted(st.session_state.global_scores.items(), key=lambda x: x[1], reverse=True)
    cols = st.columns(3)
    for i, (h, s) in enumerate(sorted_h):
        with cols[i % 3]: st.markdown(f"<div class='stMetric'><h4>{h}</h4><h2>{s} Pts</h2></div>", unsafe_allow_html=True)
    if st.button("🚪 Logout"):
        if 'user' in st.session_state: del st.session_state.user
        st.session_state.page = "login"; st.rerun()

else:
    if 'user' not in st.session_state:
        st.markdown("<h1>⚡ STUDENT LOGIN</h1>", unsafe_allow_html=True)
        u_class = st.selectbox("Class:", list(STUDENT_DB.keys()))
        u_name = st.selectbox("Name:", STUDENT_DB[u_class])
        u_house = st.selectbox("House:", CLASS_HOUSES[u_class])
        if st.button("Login"):
            st.session_state.user, st.session_state.u_class, st.session_state.u_house = u_name, u_class, u_house
            st.rerun()
    else:
        st.markdown(f"### 🎊 Welcome, {st.session_state.user} | {st.session_state.u_house}")
        mode = st.radio("Activity:", ["Live Quiz 📝", "Assignment 📚"])
        
        if mode == "Live Quiz 📝":
            user_id = f"{st.session_state.user}_{st.session_state.u_class}"
            if user_id in finished_ids:
                st.error("🛑 Quiz already submitted!")
            else:
                if 'quiz_active' not in st.session_state: st.session_state.quiz_active = False
                if not st.session_state.quiz_active:
                    lessons = list(get_questions_by_lesson().keys())
                    selected_lesson = st.selectbox("Select Lesson:", lessons)
                    if st.text_input("Quiz Key:", type="password") == "Hyper2026" and st.button("Start Mission"):
                        st.session_state.quiz_active = True
                        st.session_state.quiz_start_time = time.time()
                        # اختيار 10 عشوائي فقط للكويز
                        st.session_state.quiz_questions = random.sample(get_questions_by_lesson()[selected_lesson], 10)
                        st.rerun()
                else:
                    rem = (15*60) - (time.time() - st.session_state.quiz_start_time)
                    if rem <= 0: st.session_state.quiz_active = False; st.rerun()
                    st.markdown(f"<div class='timer-box'><h3>⏳ Time: {int(rem//60)}:{int(rem%60):02d}</h3></div>", unsafe_allow_html=True)
                    with st.form("quiz"):
                        ans = {i: st.radio(f"Q{i+1}: {q['q']}", q['options']) for i, q in enumerate(st.session_state.quiz_questions)}
                        if st.form_submit_button("Submit"):
                            score = sum(1 for i, q in enumerate(st.session_state.quiz_questions) if ans[i] == q['a'])
                            save_log_to_csv({"Student": st.session_state.user, "Class": st.session_state.u_class, "House": st.session_state.u_house, "Score": f"{score}/10", "Date": datetime.now(egy_tz).strftime("%Y-%m-%d"), "Time": datetime.now(egy_tz).strftime("%I:%M:%S %p")})
                            st.session_state.quiz_active = False; st.session_state.page = "dashboard"; st.rerun()
        
        else: # Assignment Mode 📚
            st.info("🎯 Practice Mode - Answer all questions in the bank!")
            lessons = list(get_questions_by_lesson().keys())
            selected_lesson = st.selectbox("Select Lesson to Practice:", lessons)
            
            # في الأسايمنت بنجيب كل الأسئلة مش عينة عشوائية
            all_practice_questions = get_questions_by_lesson()[selected_lesson]

            with st.form("assignment_form"):
                user_answers = {}
                for i, q in enumerate(all_practice_questions):
                    st.write(f"**Q{i+1}: {q['q']}**")
                    user_answers[i] = st.radio(f"Select Q{i}", q['options'], key=f"as_q_{i}", label_visibility="collapsed")
                
                check = st.form_submit_button("✅ Check Results")
            
            if check:
                st.markdown("---")
                score = 0
                for i, q in enumerate(all_practice_questions):
                    is_correct = user_answers[i] == q['a']
                    if is_correct: score += 1
                    
                    color = "correct" if is_correct else "wrong"
                    icon = "✅" if is_correct else "❌"
                    st.markdown(f"""
                        <div style='padding: 10px; border-left: 5px solid {"#00ff88" if is_correct else "#ff4b4b"}; margin-bottom: 10px; background: #1e2130;'>
                            {icon} <b>Q{i+1}:</b> {q['q']}<br>
                            Your answer: <span class='{color}'>{user_answers[i]}</span><br>
                            Correct answer: <span class='correct'>{q['a']}</span>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown(f"<div class='result-box'><h2>Total Score: {score}/{len(all_practice_questions)}</h2></div>", unsafe_allow_html=True)

        if st.button("Logout"): del st.session_state.user; st.rerun()
