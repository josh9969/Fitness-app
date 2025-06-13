import streamlit as st

# ------------------------
# 🍱 Sample Food Calorie Data
# ------------------------
food_db = {
    "Banana": 89,
    "Egg (boiled)": 78,
    "Rice (1 cup)": 206,
    "Chicken Breast (100g)": 165,
    "Apple": 95,
    "Oats (1 cup)": 150
}

# ------------------------
# 🏋️ Exercise Database
# ------------------------
exercise_db = {
    "Chest": [
        {"name": "Push-Up", "img": "https://media.giphy.com/media/L05HgB2h6qICDs5Sms/giphy.gif", "desc": "Bodyweight chest exercise"},
        {"name": "Bench Press", "img": "https://media.giphy.com/media/xUNd9HZq1itMkiK652/giphy.gif", "desc": "Classic barbell chest builder"}
    ],
    "Back": [
        {"name": "Pull-Up", "img": "https://media.giphy.com/media/iFmw13LNwz9k6/giphy.gif", "desc": "Bodyweight back & biceps"},
        {"name": "Deadlift", "img": "https://media.giphy.com/media/3o7abAhvUQjTWeN4CW/giphy.gif", "desc": "Mass builder for back and legs"}
    ]
}

# ------------------------
# 🚀 App Layout
# ------------------------
st.set_page_config(page_title="Fitness Tracker", layout="centered")

st.sidebar.title("🏋️ Fitness App")
page = st.sidebar.radio("Go to", ["Calorie Counter", "Exercise Guide"])

# ------------------------
# 🍽️ Calorie Counter Page
# ------------------------
if page == "Calorie Counter":
    st.title("🍽️ Calorie Tracker")

    if "meals" not in st.session_state:
        st.session_state["meals"] = []

    with st.form("meal_form"):
        food = st.selectbox("Select Food", list(food_db.keys()))
        quantity = st.number_input("Quantity (servings)", min_value=0.5, step=0.5, value=1.0)
        submit = st.form_submit_button("Add Meal")

        if submit:
            calories = food_db[food] * quantity
            st.session_state["meals"].append((food, quantity, calories))
            st.success(f"Added {food} ({calories} kcal)")

    if st.session_state["meals"]:
        st.subheader("Today's Meals")
        total = 0
        for item in st.session_state["meals"]:
            st.write(f"{item[0]} × {item[1]} → **{item[2]} kcal**")
            total += item[2]
        st.markdown(f"### 🔥 Total Calories: **{total:.2f} kcal**")

# ------------------------
# 🏋️ Exercise Page
# ------------------------
elif page == "Exercise Guide":
    st.title("🏋️ Exercise Tutorials")

    category = st.selectbox("Select Muscle Group", list(exercise_db.keys()))
    exercises = exercise_db[category]

    for ex in exercises:
        st.markdown(f"### {ex['name']}")
        st.image(ex['img'], width=300)
        st.caption(ex['desc'])
        st.markdown("---")
