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

# --- 4. مخزن الأسئلة (مقسم حسب الدروس) ---
def get_questions_by_lesson():
    return {
        # ============================================
        # 📚 Fluid Mechanics (دروس الفيزياء الحالية)
        # ============================================
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
        
        # ============================================
        # ⚡ Electricity (دروس الكهرباء الجديدة)
        # ============================================
        "Electricity ⚡": [
            {"q": "What is the SI unit of electric current?", "options": ["Volt", "Ampere", "Ohm"], "a": "Ampere"},
            {"q": "Ohm's law states V = ?", "options": ["IR", "I/R", "R/I"], "a": "IR"},
            {"q": "Resistance depends on?", "options": ["Length", "Area", "Both"], "a": "Both"},
            {"q": "If length doubles, resistance?", "options": ["Doubles", "Halves", "Same"], "a": "Doubles"},
            {"q": "If area doubles, resistance?", "options": ["Doubles", "Halves", "Same"], "a": "Halves"},
            {"q": "Current flows from ____ to ____.", "options": ["Positive to Negative", "Negative to Positive", "Same potential"], "a": "Positive to Negative"},
            {"q": "Power in electric circuit is?", "options": ["VI", "V/I", "I/V"], "a": "VI"},
            {"q": "1 Ampere = ____ Coulombs per second.", "options": ["1", "10", "100"], "a": "1"},
            {"q": "Series resistors add ____.", "options": ["Directly", "Inversely", "Square"], "a": "Directly"},
            {"q": "Parallel resistors add ____.", "options": ["Directly", "Inversely", "Square"], "a": "Inversely"},
        ],
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
            st.write(f"✅ **{log.get('Student', 'Unknown')}** ({log.get('Class', 'N/A')}) - `{log.get('Score', 'N/A')}`")
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
    with t1: st.dataframe(pd.DataFrame(st.session_state.records))
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
                    st.markdown(f"**📚 Lesson:** {st.session_state.selected_lesson}")
                    
                    with st.form("quiz_form"):
                        answers = {}
                        for i, q in enumerate(st.session_state.quiz_questions):
                            st.write(f"**Q{i+1}: {q['q']}**")
                            answers[i] = st.radio("Choose:", q['options'], key=f"q{i}", label_visibility="collapsed")
                        
                        if st.form_submit_button("Submit Deployment"):
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
                            save_log_to_csv(log)
                            st.session_state.records.append(log)
                            finished_ids.add(user_id)
                            st.session_state.quiz_active = False
                            st.session_state.page = "dashboard"
                            st.rerun()
        
        else:  # Assignment Mode 📚
            st.info("🎯 Practice Mode - Check your answers!")
            
            # إعداد Assignment
            if 'assignment_lesson' not in st.session_state:
                lessons = list(get_questions_by_lesson().keys())
                st.session_state.assignment_lesson = st.selectbox("Select Lesson for Assignment:", lessons, key="assign_lesson")
                questions = get_questions_by_lesson()[st.session_state.assignment_lesson]
                num_questions = min(10, len(questions))
                st.session_state.assignment_questions = random.sample(questions, num_questions)
                st.session_state.assignment_answers = {}
                st.session_state.assignment_submitted = False
            
            selected_lesson = st.session_state.assignment_lesson
            
            # إعادة تحميل الأسئلة لو غير الدرس
            if 'assignment_lesson_changed' in st.session_state and st.session_state.assignment_lesson_changed:
                questions = get_questions_by_lesson()[selected_lesson]
                num_questions = min(10, len(questions))
                st.session_state.assignment_questions = random.sample(questions, num_questions)
                st.session_state.assignment_answers = {}
                st.session_state.assignment_submitted = False
                del st.session_state.assignment_lesson_changed
                st.rerun()
            
            questions = st.session_state.assignment_questions
            
            # عرض الأسئلة
            with st.form("assignment_form", clear_on_submit=False):
                st.markdown("### 📝 Answer all questions:")
                for i, q in enumerate(questions):
                    st.write(f"**Q{i+1}: {q['q']}**")
                    default_index = 0
                    if i in st.session_state.assignment_answers:
                        try:
                            default_index = q['options'].index(st.session_state.assignment_answers[i])
                        except:
                            default_index = 0
                    
                    st.session_state.assignment_answers[i] = st.radio(
                        "Your Answer:", q['options'], 
                        key=f"assign_q{i}", 
                        label_visibility="collapsed",
                        index=default_index
                    )
                
                col1, col2, col3 = st.columns([2, 1, 1])
                with col2:
                    submitted = st.form_submit_button("✅ Check Answers", use_container_width=True)
                with col3:
                    if st.form_submit_button("🔄 New Questions", use_container_width=True):
                        st.session_state.assignment_lesson_changed = True
                        st.rerun()
            
            # حساب وعرض النتيجة بعد الضغط على Check Answers
            if submitted and st.session_state.assignment_questions:
                st.markdown("---")
                st.markdown("""
                <div class='result-box'>
                    <h2>🎯 YOUR RESULTS</h2>
                </div>
                """, unsafe_allow_html=True)
                
                score = 0
                total = len(st.session_state.assignment_questions)
                results = []
                
                for i, q in enumerate(st.session_state.assignment_questions):
                    user_ans = st.session_state.assignment_answers.get(i, "")
                    correct_ans = q['a']
                    is_correct = user_ans == correct_ans
                    
                    if is_correct:
                        score += 1
                    
                    results.append({
                        'question': q['q'],
                        'user_answer': user_ans,
                        'correct_answer': correct_ans,
                        'is_correct': is_correct
                    })
                
                # عرض النتيجة النهائية
                percentage = int((score / total) * 100)
                result_message = "Excellent! 👏" if percentage >= 80 else "Good! 👍" if percentage >= 60 else "Keep Practicing! 💪"
                st.markdown(f"""
                <div class='result-box'>
                    <h1 style='color: #00ff88;'>{score}/{total}</h1>
                    <h2>{percentage}% 🎯</h2>
                    <h4>{result_message}</h4>
                </div>
                """, unsafe_allow_html=True)
                
                # عرض تفاصيل كل سؤال
                st.markdown("### 📋 Detailed Results:")
                for i, result in enumerate(results):
                    color = "correct" if result['is_correct'] else "wrong"
                    icon = "✅" if result['is_correct'] else "❌"
                    st.markdown(f"""
                    <div style='padding: 15px; margin: 10px 0; 
                                background-color: #1e2130;
                                border-left: 6px solid {'#00ff88' if result['is_correct'] else '#ff4b4b'};
                                border-radius: 8px;'>
                        <h4>{icon} Q{i+1}: {result['question']}</h4>
                        <p><strong>👤 You chose:</strong> <span class='{color}'>{result['user_answer']}</span></p>
                        <p><strong>✅ Correct:</strong
