import streamlit as st
import requests
import datetime
import pandas as pd

# --- Nutritionix API ---
APP_ID = "YOUR_APP_ID"
API_KEY = "YOUR_API_KEY"

def get_calories(food_query):
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        "x-app-id": APP_ID,
        "x-app-key": API_KEY,
        "Content-Type": "application/json"
    }
    data = {"query": food_query}
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    try:
        food = result["foods"][0]
        return food["food_name"], food["nf_calories"]
    except:
        return None, None

# --- Setup ---
if "log" not in st.session_state:
    st.session_state.log = []

if "goal" not in st.session_state:
    st.session_state.goal = 2000

# --- Page Config ---
st.set_page_config(page_title="Fitness Tracker", layout="centered")

# --- Custom Styling ---
st.markdown("""
    <style>
    body {
        background-color: #121212;
        color: #F1F1F1;
    }
    .main {
        background-color: #1e1e1e;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 0 10px rgba(255,255,255,0.05);
    }
    h1, h2, h3 {
        color: #F5A623;
        font-family: 'Trebuchet MS', sans-serif;
    }
    .stButton > button {
        background-color: #F5A623;
        color: black;
        border-radius: 8px;
        padding: 0.5em 1em;
        font-weight: bold;
    }
    .stSelectbox, .stTextInput, .stNumberInput {
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# --- TITLE ---
st.markdown("<div class='main'>", unsafe_allow_html=True)
st.title("🍽️ Aesthetic Calorie Tracker")
st.caption("Dark. Simple. Gen Z Approved.")

# --- Goal Setter ---
st.subheader("🎯 Daily Calorie Goal")
goal_input = st.number_input("Set your daily goal (kcal):", min_value=1000, max_value=5000, step=100, value=st.session_state.goal)
if st.button("Update Goal"):
    st.session_state.goal = goal_input
    st.success(f"Goal updated to {goal_input} kcal")

# --- Reset Button ---
if st.button("🧹 Reset Today's Log"):
    st.session_state.log = []
    st.warning("Log has been reset.")

# --- Food Entry ---
st.subheader("🍕 Add Food")
food_query = st.text_input("Enter food name + quantity (e.g., 2 eggs, chicken sandwich):")
if st.button("➕ Add"):
    name, kcal = get_calories(food_query)
    if name:
        st.session_state.log.append({
            "food": name.title(),
            "calories": round(kcal),
            "time": datetime.datetime.now().strftime("%H:%M")
        })
        st.success(f"Added {name.title()} - {round(kcal)} kcal")
    else:
        st.error("Food not found. Try again.")

# --- Calorie Log ---
st.subheader("📋 Meal Log")
if st.session_state.log:
    df = pd.DataFrame(st.session_state.log)
    st.table(df)
    total = sum(item["calories"] for item in st.session_state.log)
    st.metric("🔥 Total Today", f"{total} kcal", delta=f"{st.session_state.goal - total} kcal left")
else:
    st.info("Start adding meals to see your log.")

st.markdown("</div>", unsafe_allow_html=True)

# --- Workout Video Section ---
st.markdown("<div class='main'>", unsafe_allow_html=True)
st.header("🎥 Workout Demos")

exercise_library = {
    "Chest": {
        "Push Ups": "https://www.youtube.com/embed/IODxDxX7oi4",
        "Incline Push Ups": "https://www.youtube.com/embed/jWxvtyvPjbE"
    },
    "Legs": {
        "Squats": "https://www.youtube.com/embed/aclHkVaku9U",
        "Lunges": "https://www.youtube.com/embed/QOVaHwm-Q6U",
        "Calf Raises": "https://www.youtube.com/embed/-M4-G8p8fmc"
    },
    "Core": {
        "Plank": "https://www.youtube.com/embed/pSHjTRCQxIw",
        "Crunches": "https://www.youtube.com/embed/Xyd_fa5zoEU",
        "Russian Twists": "https://www.youtube.com/embed/wkD8rjkodUI"
    },
    "Full Body / Cardio": {
        "Burpees": "https://www.youtube.com/embed/dZgVxmf6jkA",
        "Mountain Climbers": "https://www.youtube.com/embed/cnyTQDSE884",
        "Jumping Jacks": "https://www.youtube.com/embed/UpH7rm0cYbM"
    }
}

selected_category = st.selectbox("Select a Body Part:", list(exercise_library.keys()))
selected_exercise = st.selectbox("Select an Exercise:", list(exercise_library[selected_category].keys()))

if selected_exercise:
    st.markdown(f"### ▶️ {selected_exercise}")
    st.components.v1.iframe(exercise_library[selected_category][selected_exercise], height=315)
st.markdown("</div>", unsafe_allow_html=True)
