import streamlit as st
import random
import time
import pandas as pd
import os
from datetime import datetime
import pytz

# --- 1. الإعدادات والبراندنج مع JavaScript للتحديث المباشر ---
st.set_page_config(page_title="Hyper Torque Academy", page_icon="⚡", layout="wide")

# JavaScript لتحديث الساعة والتايمر مباشرة في المتصفح دون الحاجة لريفريش السيرفر
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { border-radius: 15px; background-color: #ff4b4b; color: white; font-weight: bold; height: 3em; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 2px solid #ff4b4b; }
    h1, h2, h3 { color: #ff4b4b; text-align: center; font-family: 'Trebuchet MS'; }
    .timer-box { background-color: #1e2130; padding: 10px; border-radius: 10px; border: 2px solid #ff4b4b; text-align: center; margin-bottom: 20px; }
    </style>
    
    <script>
    function updateClock() {
        const options = { 
            timeZone: 'Africa/Cairo',
            hour: '2-digit', 
            minute: '2-digit', 
            second: '2-digit',
            hour12: true 
        };
        const now = new Date();
        const timeString = now.toLocaleTimeString('en-US', options);
        
        // البحث عن عنصر الساعة وتحديثه
        const clockElements = window.parent.document.querySelectorAll('p, span, div');
        clockElements.forEach(el => {
            if (el.textContent.includes('🕒 Clock:')) {
                el.innerHTML = `🕒 Clock: <strong>${timeString}</strong>`;
            }
        });
    }
    setInterval(updateClock, 1000);
    </script>
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
            {"q": "What is the SI unit of density?", "options": ["kg/m2", "kg/m3", "N/m2"], "a": "kg/m3"},
            {"q": "The continuity equation results from ____ conservation.", "options": ["Energy", "Mass", "Volume"], "a": "Mass"},
            {"q": "Pascal's Principle applies to?", "options": ["Solids", "Gases", "Confined Fluids"], "a": "Confined Fluids"},
            {"q": "Buoyant force direction?", "options": ["Down", "Up", "Side"], "a": "Up"},
            {"q": "If Area decreases, Velocity?", "options": ["Up", "Down", "Same"], "a": "Up"},
            {"q": "Archimedes' principle measures ____ force?", "options": ["Gravity", "Buoyant", "Friction"], "a": "Buoyant"},
            {"q": "Viscosity measures?", "options": ["Flow resistance", "Density", "Pressure"], "a": "Flow resistance"},
            {"q": "100 cm2 to m2?", "options": ["0.1", "0.01", "1.0"], "a": "0.01"},
            {"q": "Pressure = Force / ?", "options": ["Mass", "Volume", "Area"], "a": "Area"},
            {"q": "Bernoulli's equation relates to?", "options": ["Energy", "Momentum", "Force"], "a": "Energy"},
        ],
        "Electricity ⚡": [
            {"q": "What is the SI unit of electric current?", "options": ["Volt", "Ampere", "Ohm"], "a": "Ampere"},
            {"q": "Ohm's law states V = ?", "options": ["IR", "I/R", "R/I"], "a": "IR"}
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
    st.markdown("### 🟢 Recent Activity")
    if st.session_state.records:
        student_only = [r for r in st.session_state.records if r.get('Student') != "ADMIN_ADJUST"]
        for log in reversed(student_only[-5:]):
            st.caption(f"📅 {log.get('Date', 'N/A')} | {log.get('Time', 'N/A')}")
            st.write(f"✅ **{log.get('Student', 'Unknown')}** - `{log.get('Score', 'N/A')}`")
            st.markdown("---")
    
    if st.button("🏠 Global Dashboard"): st.session_state.page = "dashboard"; st.rerun()
    admin_input = st.text_input("Admin Access:", type="password")
    is_admin = (admin_input == "Admin2026")

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
            now_egy = datetime.now(egy_tz)
            entry = {"Student": "ADMIN_ADJUST", "Class": "SYSTEM", "House": h_sel, "Score": adj, "Day": now_egy.strftime("%A"), "Date": now_egy.strftime("%Y-%m-%d"), "Time": now_egy.strftime("%I:%M:%S %p")}
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
                    pwd = st.text_input("Quiz Key:", type="password")
                    if st.button("Start Mission") and pwd == "Hyper2026":
                        st.session_state.quiz_active = True
                        st.session_state.quiz_end_time = time.time() + (15 * 60)
                        st.session_state.selected_lesson = selected_lesson
                        qs = get_questions_by_lesson()[selected_lesson]
                        st.session_state.quiz_questions = random.sample(qs, min(10, len(qs)))
                        st.rerun()
                else:
                    remaining = st.session_state.quiz_end_time - time.time()
                    if remaining <= 0:
                        st.session_state.quiz_active = False; st.rerun()
                    
                    # الـ HTML والـ JS الخاص بالتايمر الحي
                    timer_html = f"""
                    <div class='timer-box'>
                        <h3 id="live-timer">⏳ Time: {int(remaining//60)}:{int(remaining%60):02d}</h3>
                    </div>
                    <script>
                    (function() {{
                        const endTime = {st.session_state.quiz_end_time};
                        function updateTimer() {{
                            const now = Date.now() / 1000;
                            const remaining = Math.max(0, endTime - now);
                            if (remaining <= 0) {{
                                document.getElementById('live-timer').innerHTML = '⏳ Time: 0:00';
                                return;
                            }}
                            const minutes = Math.floor(remaining / 60);
                            const seconds = Math.floor(remaining % 60);
                            document.getElementById('live-timer').innerHTML = `⏳ Time: ${{minutes}}:${{seconds < 10 ? '0' : ''}}${{seconds}}`;
                        }}
                        setInterval(updateTimer, 1000);
                    }})();
                    </script>
                    """
                    st.markdown(timer_html, unsafe_allow_html=True)
                    
                    with st.form("quiz"):
                        ans = {i: st.radio(f"Q{i+1}: {q['q']}", q['options']) for i, q in enumerate(st.session_state.quiz_questions)}
                        if st.form_submit_button("Submit Deployment"):
                            score = sum(1 for i, q in enumerate(st.session_state.quiz_questions) if ans[i] == q['a'])
                            now_egy = datetime.now(egy_tz)
                            log = {"Student": st.session_state.user, "Class": st.session_state.u_class, "House": st.session_state.u_house, "Score": f"{score}/{len(st.session_state.quiz_questions)}", "Date": now_egy.strftime("%Y-%m-%d"), "Time": now_egy.strftime("%I:%M:%S %p")}
                            save_log_to_csv(log); st.session_state.records.append(log)
                            st.session_state.quiz_active = False; st.session_state.page = "dashboard"; st.rerun()
        else:
            st.info("Practice Mode.")
            for q in get_questions_by_lesson()["Fluid Mechanics 🌊"]:
                st.write(f"**{q['q']}**")
                st.radio("Practice:", q['options'], key="as_"+q['q'])
        
        if st.button("Logout"): del st.session_state.user; st.rerun()
