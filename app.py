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

# --- 4. مخزن الأسئلة (25 سؤال موسع) ---
def get_questions_by_lesson():
    return {
        "Fluid Mechanics 🌊": [
            {"q": "A hydraulic lift has A1 = 0.20 m² and A2 = 0.90 m². If F2 = 1.20 x 10⁴ N, calculate F1.", "options": ["1.5 x 10³ N", "2.7 x 10³ N", "5.4 x 10³ N", "2.7 x 10² N"], "a": "2.7 x 10³ N"},
            {"q": "If the radius of the large piston is 4 times the small piston radius, the force multiplication is:", "options": ["4 times", "8 times", "16 times", "2 times"], "a": "16 times"},
            {"q": "A crown weighs 7.84 N in air and 6.86 N in water. Its density is:", "options": ["19.3 x 10³ kg/m³", "8.0 x 10³ kg/m³", "10.0 x 10³ kg/m³", "2.7 x 10³ kg/m³"], "a": "8.0 x 10³ kg/m³"},
            {"q": "Water flows through a pipe at 2 m/s. If the pipe narrows to 1/4 of its area, the new velocity is:", "options": ["0.5 m/s", "4 m/s", "16 m/s", "8 m/s"], "a": "8 m/s"},
            {"q": "Iron and aluminum balls of the same VOLUME are submerged in water. Which experiences a greater buoyant force?", "options": ["Iron ball", "Aluminum ball", "Both the same", "Depends on mass"], "a": "Both the same"},
            {"q": "If pipe diameter is doubled, the area increases by:", "options": ["2 times", "8 times", "16 times", "4 times"], "a": "4 times"},
            {"q": "Calculate absolute pressure at 10m depth (P_atm=1.01x10⁵ Pa, ρ=1000, g=9.8):", "options": ["1.01 x 10⁵ Pa", "1.99 x 10⁵ Pa", "0.98 x 10⁵ Pa", "2.50 x 10⁵ Pa"], "a": "1.99 x 10⁵ Pa"},
            {"q": "Continuity equation (A1v1 = A2v2) results from conservation of:", "options": ["Energy", "Momentum", "Mass", "Pressure"], "a": "Mass"},
            {"q": "A boat moves from fresh water to salt water. The buoyant force:", "options": ["Increases", "Decreases", "Stays the same", "Disappears"], "a": "Stays the same"},
            {"q": "Gauge pressure is defined as:", "options": ["P_total + P_atm", "P_atm - P_total", "P_total - P_atm", "P_total / P_atm"], "a": "P_total - P_atm"},
            {"q": "What is the SI unit of mass
