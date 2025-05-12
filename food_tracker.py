
import streamlit as st
import pandas as pd
import datetime

@st.cache_data
def load_food_data():
    try:
        df = pd.read_csv("food_log.csv")
        df["Date"] = pd.to_datetime(df["Date"])
    except:
        today = datetime.date.today()
        df = pd.DataFrame(columns=["Date", "Meal Time", "Food Item", "Calories", "Protein (g)", "Carbs (g)", "Fat (g)", "Notes"])
    return df

def save_food_data(df):
    df.to_csv("food_log.csv", index=False)

def food_log_ui():
    st.header("Food Intake Tracker")
    df = load_food_data()
    today = datetime.date.today()
    with st.form("food_form"):
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("Date", today)
        with col2:
            meal_time = st.selectbox("Meal Time", ["Breakfast", "Lunch", "Dinner", "Snack"])
        food_item = st.text_input("Food Item")
        calories = st.number_input("Calories", min_value=0, max_value=2000, value=0)
        protein = st.number_input("Protein (g)", min_value=0, max_value=200, value=0)
        carbs = st.number_input("Carbs (g)", min_value=0, max_value=200, value=0)
        fat = st.number_input("Fat (g)", min_value=0, max_value=100, value=0)
        notes = st.text_input("Notes")
        submitted = st.form_submit_button("Add Entry")
        if submitted:
            new_entry = pd.DataFrame([{
                "Date": date,
                "Meal Time": meal_time,
                "Food Item": food_item,
                "Calories": calories,
                "Protein (g)": protein,
                "Carbs (g)": carbs,
                "Fat (g)": fat,
                "Notes": notes
            }])
            df = pd.concat([df, new_entry], ignore_index=True)
            save_food_data(df)
            st.success("Entry added successfully!")

    st.subheader("Today's Summary")
    today_data = df[df["Date"] == pd.to_datetime(today)]
    if not today_data.empty:
        st.dataframe(today_data[["Meal Time", "Food Item", "Calories", "Protein (g)", "Carbs (g)", "Fat (g)"]])
        st.write("**Total Calories:**", today_data["Calories"].sum())
        st.write("**Total Protein:**", today_data["Protein (g)"].sum(), "g")
        st.write("**Total Carbs:**", today_data["Carbs (g)"].sum(), "g")
        st.write("**Total Fat:**", today_data["Fat (g)"].sum(), "g")
    else:
        st.write("No entries for today.")
