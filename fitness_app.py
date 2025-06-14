import streamlit as st
import requests
import datetime
import pandas as pd

# --- Nutritionix Credentials ---
APP_ID = "948fc117"
API_KEY = "17c71ea80b533910f2a7a5cbd524aa8d	—"

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

