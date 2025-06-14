import streamlit as st
import requests
import datetime
import pandas as pd

# --- Nutritionix Credentials ---
APP_ID = "948fc117"
API_KEY = "17c71ea80b533910f2a7a5cbd524aa8d"

# --- Helper: Get calories from Nutritionix ---
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

# --- Session State Setup ---
if "log" not in st.session_state:
    st.session_state.log = []

if "goal" not in st.session_state:
    st.session_state.goal = 2000  # default goal

# --- UI: Title + Layout ---
st.title("🍎 Daily Calorie Tracker")
st.caption("Track your calories and log your meals in real-time.")

col1, col2 = st.columns(2)
with col1:
    st.number_input("🎯 Set Daily Calorie Goal", min_value=1000, max_value=5000, step=100, value=st.session_state.goal, key="goal_input")
    if st.button("Update Goal"):
        st.session_state.goal = st.session_state.goal_input
        st.success(f"Goal set to {st.session_state.goal} kcal")

with col2:
    if st.button("🧹 Reset Today's Log"):
        st.session_state.log = []
        st.warning("Log reset for today.")

# --- Input Food Entry ---
st.subheader("🍽️ Add Food Entry")
food_query = st.text_input("Enter food (e.g. 2 boiled eggs, chicken sandwich):")

if st.button("➕ Add to Log"):
    name, kcal = get_calories(food_query)
    if name:
        st.session_state.log.append({
            "food": name.title(),
            "calories": round(kcal),
            "time": datetime.datetime.now().strftime("%H:%M")
        })
        st.success(f"Added {name.title()} - {round(kcal)} kcal")
    else:
        st.error("Couldn't recognize that food. Try something else.")

# --- Log Display ---
if st.session_state.log:
    st.subheader("📋 Today's Meals")
    df = pd.DataFrame(st.session_state.log)
    st.table(df)

    total = sum(item["calories"] for item in st.session_state.log)
    st.metric("🔥 Total Calories Today", f"{total} kcal", delta=f"{st.session_state.goal - total} kcal left")
else:
    st.info("No food logged yet. Start by adding something above.")

# --- Workout Demo Section ---

st.markdown("---")
st.header("💪 Workout Video Demos by Body Part")

# --- Exercise Video Dictionary by Category ---
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

# --- UI: Select Category First ---
selected_category = st.selectbox("Select a Body Part:", list(exercise_library.keys()))

# --- UI: Then Select Exercise ---
selected_exercise = st.selectbox(
    "Select an Exercise:", 
    list(exercise_library[selected_category].keys())
)

# --- Show the Video ---
if selected_exercise:
    st.markdown(f"### ▶️ {selected_exercise}")
    st.components.v1.iframe(exercise_library[selected_category][selected_exercise], height=315)
