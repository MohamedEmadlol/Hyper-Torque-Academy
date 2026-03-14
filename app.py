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
    .correct { color: #00ff88; font-weight: bold; }
    .wrong { color: #ff4b4b; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# توقيت القاهرة الثابت
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
        try:
            return pd.read_csv(file_path).to_dict('records')
        except:
            return []
    return []

# --- 3. قاعدة بيانات الطلاب والبيوت ---
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

# --- 4. مخزن الأسئلة الشامل (25 سؤال + توزيع عشوائي للإجابات) ---
def get_questions_by_lesson():
    return {
        "Fluid Mechanics 🌊": [
            {"q": "A hydraulic lift has A1 = 0.20 m² and A2 = 0.90 m². If F2 = 1.20 x 10⁴ N, calculate F1.", "options": ["1.5 x 10³ N", "2.7 x 10³ N", "5.4 x 10³ N", "2.7 x 10² N"], "a": "2.7 x 10³ N"},
            {"q": "If the radius of the large piston is 4 times the small piston radius, the force multiplication is:", "options": ["4 times", "8 times", "16 times", "2 times"], "a": "16 times"},
            {"q": "A crown weighs 7.84 N in air and 6.86 N in water. Its density is:", "options": ["19.3 x 10³ kg/m³", "8.0 x 10³ kg/m³", "10.0 x 10³ kg/m³", "2.7 x 10³ kg/m³"], "a": "8.0 x 10³ kg/m³"},
            {"q": "Water flows through a pipe at 2 m/s. If the pipe narrows to 1/4 of its area, the new velocity is:", "options": ["0.5 m/s", "4 m/s", "16 m/s", "8 m/s"], "a": "8 m/s"},
            {"q": "Iron and aluminum balls of the same VOLUME are submerged in water. Which experiences a greater buoyant force?", "options": ["More force on Iron", "More force on Aluminum", "Both the same", "Depends on mass"], "a": "Both the same"},
            {"q": "If pipe diameter is doubled, the cross-sectional area increases by:", "options": ["2 times", "8 times", "16 times", "4 times"], "a": "4 times"},
            {"q": "Calculate absolute pressure at 10m depth (P_atm = 1.01x10⁵ Pa, ρ=1000, g=9.8):", "options": ["1.01 x 10⁵ Pa", "1.99 x 10⁵ Pa", "0.98 x 10⁵ Pa", "2.50 x 10⁵ Pa"], "a": "1.99 x 10⁵ Pa"},
            {"q": "A boat moves from fresh water to salt water. The buoyant force:", "options": ["Increases", "Decreases", "Stays the same", "Disappears"], "a": "Stays the same"},
            {"q": "The continuity equation (A1v1 = A2v2) is a statement of the conservation of:", "options": ["Energy", "Momentum", "Mass", "Pressure"], "a": "Mass"},
            {"q": "Gauge pressure is defined as:", "options": ["P_total + P_atm", "P_atm - P_total", "P_total - P_atm", "P_total / P_atm"], "a": "P_total - P_atm"},
            {"q": "What is the SI unit of mass density?", "options": ["kg/m³", "kg/m²", "Newton/m³", "Pascal"], "a": "kg/m³"},
            {"q": "Pascal's principle states pressure in a closed container is transmitted equally to:", "options": ["The bottom only", "The walls only", "Every point in the fluid", "The pistons only"], "a": "Every point in the fluid"},
            {"q": "If an object is floating, the buoyant force (Fb) is:", "options": ["Equal to weight", "Greater than weight", "Less than weight", "Zero"], "a": "Equal to weight"},
            {"q": "Fluid flows through a pipe that narrows to half its original DIAMETER. The speed will:", "options": ["Increase by 2 times", "Increase by 4 times", "Decrease by 4 times", "Decrease by 2 times"], "a": "Increase by 4 times"},
            {"q": "Which of these are considered fluids?", "options": ["Liquid and Gas", "Solid and Liquid", "Solid only", "Gas only"], "a": "Liquid and Gas"},
            {"q": "In a hydraulic system, if you triple the area of the output piston, the output force will:", "options": ["Triple", "Divide by 3", "Increase 9x", "Same"], "a": "Triple"},
            {"q": "As an object sinks deeper (fully submerged), the buoyant force:", "options": ["Increases", "Remains constant", "Decreases", "Becomes zero"], "a": "Remains constant"},
            {"q": "Viscosity measures:", "options": ["Flow resistance", "Density", "Pressure", "Mass"], "a": "Flow resistance"},
            {"q": "100 cm2 to m2 conversion factor is:", "options": ["0.1", "0.01", "1.0", "10"], "a": "0.01"},
            {"q": "Pressure is calculated as:", "options": ["Mass / Volume", "Force / Area", "Force * Area", "Mass * Gravity"], "a": "Force / Area"},
            {"q": "As a submarine dives deeper, the water pressure against the hull:", "options": ["Decreases", "Increases", "Stays constant", "Becomes zero"], "a": "Increases"},
            {"q": "A 10 kg mass has a density of 2000 kg/m³. Its volume is:", "options": ["0.005 m³", "20,000 m³", "0.05 m³", "2 m³"], "a": "0.005 m³"},
            {"q": "Bernoulli's equation relates to conservation of:", "options": ["Mass", "Momentum", "Energy", "Force"], "a": "Energy"},
            {"q": "If a gas is compressed to half its volume (constant T), its density:", "options": ["Doubles", "Halves", "Stays same", "Triples"], "a": "Doubles"}
        ],
        "Electricity ⚡": [
            {"q": "What is the SI unit of electric current?", "options": ["Volt", "Ampere", "Ohm", "Watt"], "a": "Ampere"},
            {"q": "Ohm's law states V = ?", "options": ["I/R", "IR", "R/I", "I+R"], "a": "IR"},
            {"q": "Resistance depends on:", "options": ["Length", "Area", "Both", "Color"], "a": "Both"}
        ]
    }

# --- 5. تهيئة البيانات ---
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

# --- 6. Sidebar (النشاط الأخير + ساعة القاهرة) ---
with st.sidebar:
    st.markdown("## ⚡ HYPER TORQUE ACADEMY")
    st.markdown(f"**🕒 Clock:** `{datetime.now(egy_tz).strftime('%I:%M:%S %p')}`")
    st.markdown("---")
    st.markdown("### 🟢 Recent Activity")
    if st.session_state.records:
        student_only = [r for r in st.session_state.records if r.get('Student') != "ADMIN_ADJUST"]
        for log in reversed(student_only[-5:]):
            day = log.get('Day', 'N/A')
            st.caption(f"📅 {log.get('Date', 'N/A')} ({day}) | {log.get('Time', 'N/A')}")
            st.write(f"📚 **Lesson:** `{log.get('Lesson', 'N/A')}`")
            st.write(f"✅ **{log.get('Student', 'Unknown')}** - `{log.get('Score', 'N/A')}`")
            st.markdown("---")
    else:
        st.write("No activity yet.")
    
    if st.button("🏠 Global Dashboard"): st.session_state.page = "dashboard"; st.rerun()
    admin_input = st.text_input("Admin Access:", type="password")
    is_admin = (admin_input == "Admin2026")

# --- 7. منطق الصفحات ---
if 'page' not in st.session_state: st.session_state.page = "login"

if is_admin:
    st.title("🛠️ COMMAND CENTER")
    t1, t2 = st.tabs(["Records", "House Control"])
    with t1: 
        # ⚠️ هنا التعديل: عرض الجدول بالكامل شامل عمود الدرس (Lesson)
        st.dataframe(pd.DataFrame(st.session_state.records))
    with t2:
        h_sel = st.selectbox("House:", list(st.session_state.global_scores.keys()))
        adj = st.number_input("Adjust:", value=0)
        if st.button("Apply"):
            now_egy = datetime.now(egy_tz)
            entry = {
                "Student": "ADMIN_ADJUST", 
                "Class": "SYSTEM", 
                "House": h_sel, 
                "Score": adj, 
                "Lesson": "ADMIN_ADJUST", # وسم التعديل الإداري في عمود الدرس
                "Day": now_egy.strftime("%A"),
                "Date": now_egy.strftime("%Y-%m-%d"), 
                "Time": now_egy.strftime("%I:%M:%S %p")
            }
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
        st.title("⚡ STUDENT LOGIN")
        u_class = st.selectbox("Class:", list(STUDENT_DB.keys()))
        u_name = st.selectbox("Name:", STUDENT_DB[u_class])
        u_house = st.selectbox("House:", CLASS_HOUSES[u_class])
        if st.button("Login"):
            st.session_state.user, st.session_state.u_class, st.session_state.u_house = u_name, u_class, u_house
            st.rerun()
    else:
        st.write(f"### Welcome, {st.session_state.user} | {st.session_state.u_house}")
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
                    pwd = st.text_input("Quiz Key:", type="password")
                    if st.button("Start Mission") and pwd == "Hyper2026":
                        st.session_state.quiz_active = True
                        st.session_state.quiz_start_time = time.time()
                        st.session_state.selected_lesson = selected_lesson
                        questions = get_questions_by_lesson()[selected_lesson]
                        num_questions = min(10, len(questions))
                        st.session_state.quiz_questions = random.sample(questions, num_questions)
                        st.rerun()
                else:
                    remaining = (15*60) - (time.time() - st.session_state.quiz_start_time)
                    if remaining <= 0: 
                        st.session_state.quiz_active = False
                        st.rerun()
                    
                    st.markdown(f"<div class='timer-box'><h3>⏳ Time: {int(remaining//60)}:{int(remaining%60):02d}</h3></div>", unsafe_allow_html=True)
                    st.write(f"📚 **Testing on:** {st.session_state.selected_lesson}")
                    
                    with st.form("quiz_form"):
                        answers = {}
                        for i, q in enumerate(st.session_state.quiz_questions):
                            st.write(f"**Q{i+1}: {q['q']}**")
                            answers[i] = st.radio("Select:", q['options'], key=f"q{i}", index=None, label_visibility="collapsed")
                        
                        if st.form_submit_button("Submit Deployment"):
                            if None in answers.values():
                                st.warning("⚠️ جاوب على كل الأسئلة الأول يا بطل!")
                            else:
                                score = sum(1 for i, q in enumerate(st.session_state.quiz_questions) if answers[i] == q['a'])
                                now_egy = datetime.now(egy_tz)
                                log = {
                                    "Student": st.session_state.user, 
                                    "Class": st.session_state.u_class, 
                                    "House": st.session_state.u_house, 
                                    "Score": f"{score}/{len(st.session_state.quiz_questions)}", 
                                    "Lesson": st.session_state.selected_lesson, 
                                    "Day": now_egy.strftime("%A"),
                                    "Date": now_egy.strftime("%Y-%m-%d"), 
                                    "Time": now_egy.strftime("%I:%M:%S %p")
                                }
                                save_log_to_csv(log); st.session_state.records.append(log)
                                finished_ids.add(user_id)
                                st.session_state.quiz_active = False; st.session_state.page = "dashboard"; st.rerun()
        else:
            st.info("🎯 Practice Mode")
            lessons = list(get_questions_by_lesson().keys())
            selected_lesson = st.selectbox("Select Lesson for Practice:", lessons)
            all_qs = get_questions_by_lesson()[selected_lesson]
            with st.form("assignment_form"):
                user_ans = {}
                for i, q in enumerate(all_qs):
                    st.write(f"**Q{i+1}: {q['q']}**")
                    user_ans[i] = st.radio(f"As {i}", q['options'], key=f"as_{i}", index=None, label_visibility="collapsed")
                check = st.form_submit_button("✅ Check Results")
            
            if check:
                if None in user_ans.values():
                    st.error("❌ لازم تختار إجابة لكل سؤال!")
                else:
                    st.markdown("---")
                    score = 0
                    for i, q in enumerate(all_qs):
                        is_correct = user_ans[i] == q['a']
                        if is_correct: score += 1
                        color = "correct" if is_correct else "wrong"
                        icon = "✅" if is_correct else "❌"
                        st.markdown(f"""
                            <div style='padding: 10px; border-left: 5px solid {"#00ff88" if is_correct else "#ff4b4b"}; margin-bottom: 10px; background: #1e2130;'>
                                {icon} <b>Q{i+1}:</b> {q['q']}<br>
                                Your answer: <span class='{color}'>{user_ans[i]}</span><br>
                                Correct answer: <span class='correct'>{q['a']}</span>
                            </div>
                        """, unsafe_allow_html=True)
                    st.write(f"### Total Score: {score}/{len(all_qs)}")

        if st.button("Logout"):
            st.session_state.quiz_active = False
            del st.session_state.user
            st.rerun()
