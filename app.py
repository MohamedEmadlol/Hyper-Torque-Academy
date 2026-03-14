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
    .fame-card { text-align: center; background-color: #1e2130; padding: 20px; border-radius: 15px; border: 2px solid #ff4b4b; margin-bottom: 10px; }
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
        try: return pd.read_csv(file_path).to_dict('records')
        except: return []
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

# --- 4. مخزن الأسئلة ---
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
            {"q": "The continuity equation (A1v1 = A2v2) is a statement of the conservation of:", "options": ["Energy", "Momentum", "Mass", "Pressure"], "a": "Mass"}
        ],
        "Electricity ⚡": [
            {"q": "What is the SI unit of electric current?", "options": ["Volt", "Ampere", "Ohm", "Watt"], "a": "Ampere"},
            {"q": "Ohm's law states V = ?", "options": ["I/R", "IR", "R/I", "I+R"], "a": "IR"}
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

# --- 6. Sidebar ---
with st.sidebar:
    st.markdown("## ⚡ HYPER TORQUE ACADEMY")
    st.markdown(f"**🕒 Clock:** `{datetime.now(egy_tz).strftime('%I:%M:%S %p')}`")
    st.markdown("---")
    st.markdown("### 🟢 Recent Activity")
    if st.session_state.records:
        student_only = [r for r in st.session_state.records if r.get('Student') != "ADMIN_ADJUST"]
        for log in reversed(student_only[-3:]):
            st.caption(f"📅 {log.get('Date', 'N/A')} | {log.get('Time', 'N/A')}")
            st.write(f"📚 **{log.get('Lesson', 'N/A')}**")
            st.write(f"✅ **{log.get('Student', 'Unknown')}** - `{log.get('Score', 'N/A')}`")
            st.markdown("---")
    
    if st.button("🏠 Global Dashboard"): st.session_state.page = "dashboard"; st.rerun()
    is_admin = (st.text_input("Admin Access:", type="password") == "Admin2026")

# --- 7. منطق الصفحات ---
if 'page' not in st.session_state: st.session_state.page = "login"

if is_admin:
    st.title("🛠️ COMMAND CENTER")
    t1, t2 = st.tabs(["Records", "House Control"])
    with t1: st.dataframe(pd.DataFrame(st.session_state.records))
    with t2:
        h_sel = st.selectbox("House:", list(st.session_state.global_scores.keys()))
        adj = st.number_input("Adjust:", value=0)
        if st.button("Apply"):
            now = datetime.now(egy_tz)
            entry = {"Student": "ADMIN_ADJUST", "Class": "SYSTEM", "House": h_sel, "Score": adj, "Lesson": "ADJUSTMENT", "Day": now.strftime("%A"), "Date": now.strftime("%Y-%m-%d"), "Time": now.strftime("%I:%M:%S %p")}
            save_log_to_csv(entry); st.session_state.records.append(entry); st.rerun()

elif st.session_state.page == "dashboard":
    st.title("🏆 HALL OF FAME")
    st.subheader("⚡ The Fastest Heroes (Score >= 8)")
    fame_list = []
    for r in st.session_state.records:
        if r.get('Student') != "ADMIN_ADJUST" and 'Duration' in r:
            try:
                score_val = int(str(r.get('Score')).split('/')[0])
                if score_val >= 8:
                    dur = int(str(r['Duration']).replace('s',''))
                    fame_list.append({'Name': r['Student'], 'Lesson': r['Lesson'], 'Score': r['Score'], 'Time': dur})
            except: pass
    if fame_list:
        fame_list = sorted(fame_list, key=lambda x: (int(x['Score'].split('/')[0]), -x['Time']), reverse=True)
        cols = st.columns(3); medals = ["🥇", "🥈", "🥉"]
        for i, s in enumerate(fame_list[:3]):
            with cols[i]:
                st.markdown(f"<div class='fame-card'><h1>{medals[i]}</h1><h3>{s['Name']}</h3><p>{s['Lesson']}</p><p class='correct'>{s['Score']}</p><p>⏱️ {s['Time']}s</p></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.header("🏠 Standings")
    sorted_h = sorted(st.session_state.global_scores.items(), key=lambda x: x[1], reverse=True)
    cols_h = st.columns(3)
    for i, (h, s) in enumerate(sorted_h):
        with cols_h[i % 3]: st.metric(h, f"{s} Pts")
    if st.button("🚪 Logout"):
        if 'user' in st.session_state: del st.session_state.user
        st.session_state.page = "login"; st.rerun()

else:
    if 'user' not in st.session_state:
        st.title("⚡ STUDENT LOGIN")
        u_class = st.selectbox("Class:", list(STUDENT_DB.keys())); u_name = st.selectbox("Name:", STUDENT_DB[u_class]); u_house = st.selectbox("House:", CLASS_HOUSES[u_class])
        if st.button("Login"): st.session_state.user, st.session_state.u_class, st.session_state.u_house = u_name, u_class, u_house; st.rerun()
    else:
        st.write(f"### Welcome, {st.session_state.user} | {st.session_state.u_house}")
        mode = st.radio("Activity:", ["Live Quiz 📝", "Assignment 📚"])
        if mode == "Live Quiz 📝":
            u_id = f"{st.session_state.user}_{st.session_state.u_class}"
            if u_id in finished_ids: st.error("🛑 Quiz already submitted!")
            else:
                if 'quiz_active' not in st.session_state: st.session_state.quiz_active = False
                if not st.session_state.quiz_active:
                    lessons = list(get_questions_by_lesson().keys()); sel_lesson = st.selectbox("Select Lesson:", lessons)
                    if st.text_input("Quiz Key:", type="password") == "Hyper2026" and st.button("Start"):
                        st.session_state.quiz_active = True; st.session_state.quiz_start_time = time.time()
                        st.session_state.selected_lesson = sel_lesson
                        st.session_state.quiz_questions = random.sample(get_questions_by_lesson()[sel_lesson], 10)
                        st.rerun()
                else:
                    rem = (15*60) - (time.time() - st.session_state.quiz_start_time)
                    if rem <= 0: st.session_state.quiz_active = False; st.rerun()
                    st.markdown(f"<div class='timer-box'><h3>⏳ Time: {int(rem//60)}:{int(rem%60):02d}</h3></div>", unsafe_allow_html=True)
                    st.write(f"📚 **Testing on:** {st.session_state.selected_lesson}")
                    with st.form("quiz_form"):
                        answers = {i: st.radio(f"Q{i+1}: {q['q']}", q['options'], index=None) for i, q in enumerate(st.session_state.quiz_questions)}
                        if st.form_submit_button("Submit"):
                            if None in answers.values(): st.warning("⚠️ Answer all questions!")
                            else:
                                score = sum(1 for i, q in enumerate(st.session_state.quiz_questions) if answers[i] == q['a'])
                                duration = int(time.time() - st.session_state.quiz_start_time)
                                now = datetime.now(egy_tz)
                                log = {"Student": st.session_state.user, "Class": st.session_state.u_class, "House": st.session_state.u_house, "Score": f"{score}/10", "Duration": f"{duration}s", "Lesson": st.session_state.selected_lesson, "Day": now.strftime("%A"), "Date": now.strftime("%Y-%m-%d"), "Time": now.strftime("%I:%M:%S %p")}
                                save_log_to_csv(log); st.session_state.records.append(log); st.session_state.quiz_active = False; st.session_state.page = "dashboard"; st.rerun()
        else:
            st.info("🎯 Practice Mode")
            sel_lesson = st.selectbox("Select Lesson:", list(get_questions_by_lesson().keys()))
            all_qs = get_questions_by_lesson()[sel_lesson]
            with st.form("as_form"):
                u_ans = {i: st.radio(f"Q{i+1}: {q['q']}", q['options'], index=None) for i, q in enumerate(all_qs)}
                if st.form_submit_button("Check"):
                    if None in u_ans.values(): st.error("❌ Fill all questions!")
                    else:
                        score = sum(1 for i, q in enumerate(all_qs) if u_ans[i] == q['a'])
                        for i, q in enumerate(all_qs):
                            is_c = u_ans[i] == q['a']
                            st.markdown(f"<p class='{'correct' if is_c else 'wrong'}'>{'✅' if is_c else '❌'} Q{i+1}: {q['a']}</p>", unsafe_allow_html=True)
                        st.write(f"### Score: {score}/{len(all_qs)}")
        if st.button("Logout"): del st.session_state.user; st.rerun()
