
import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import food_tracker

@st.cache_data
def load_performance_data():
    try:
        df = pd.read_csv("performance_data.csv")
        df['Week Start'] = pd.to_datetime(df['Week Start'])
    except:
        today = datetime.date.today()
        weeks = [today + datetime.timedelta(weeks=i) for i in range(10)]
        df = pd.DataFrame({
            "Week Start": weeks,
            "Push-Ups (2 min)": [None]*10,
            "Plank Time (sec)": [None]*10,
            "1.5 Mile Run Time (sec)": [None]*10,
            "Weight (lbs)": [None]*10,
            "Waist (inches)": [None]*10,
            "Notes": ["" for _ in range(10)]
        })
    return df

def save_performance_data(df):
    df.to_csv("performance_data.csv", index=False)

st.title("Navy PRT Tracker App")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Enter PRT Data", "Progress Charts", "Food Intake"])

df = load_performance_data()

if page == "Dashboard":
    st.header("Progress Overview")
    current_weight = df["Weight (lbs)"].dropna().iloc[-1] if df["Weight (lbs)"].dropna().any() else "N/A"
    total_pushups = df["Push-Ups (2 min)"].dropna().max() if df["Push-Ups (2 min)"].dropna().any() else "N/A"
    best_run = df["1.5 Mile Run Time (sec)"].dropna().min()
    best_run = f"{int(best_run//60)}:{int(best_run%60):02d}" if pd.notna(best_run) else "N/A"

    st.metric("Current Weight", current_weight)
    st.metric("Best Push-Ups", total_pushups)
    st.metric("Fastest Run Time", best_run)

elif page == "Enter PRT Data":
    st.header("Weekly PRT Data Entry")
    selected_week = st.selectbox("Select Week", df["Week Start"].dt.strftime("%Y-%m-%d"))
    idx = df[df["Week Start"].dt.strftime("%Y-%m-%d") == selected_week].index[0]

    pushups = st.number_input("Push-Ups (2 min)", min_value=0, max_value=100, value=int(df.at[idx, "Push-Ups (2 min)"] or 0))
    plank = st.number_input("Plank Time (sec)", min_value=0, max_value=300, value=int(df.at[idx, "Plank Time (sec)"] or 0))
    run = st.number_input("1.5 Mile Run Time (sec)", min_value=300, max_value=1500, value=int(df.at[idx, "1.5 Mile Run Time (sec)"] or 900))
    weight = st.number_input("Weight (lbs)", min_value=100, max_value=300, value=int(df.at[idx, "Weight (lbs)"] or 178))
    waist = st.number_input("Waist (inches)", min_value=20, max_value=60, value=int(df.at[idx, "Waist (inches)"] or 34))
    notes = st.text_input("Notes", value=df.at[idx, "Notes"])

    if st.button("Save Entry"):
        df.at[idx, "Push-Ups (2 min)"] = pushups
        df.at[idx, "Plank Time (sec)"] = plank
        df.at[idx, "1.5 Mile Run Time (sec)"] = run
        df.at[idx, "Weight (lbs)"] = weight
        df.at[idx, "Waist (inches)"] = waist
        df.at[idx, "Notes"] = notes
        save_performance_data(df)
        st.success("Data Saved!")

elif page == "Progress Charts":
    st.header("Performance Charts")
    fig, ax = plt.subplots()
    df["Week Start"] = pd.to_datetime(df["Week Start"])
    df_chart = df.set_index("Week Start")
    if df_chart["Push-Ups (2 min)"].notna().any():
        df_chart["Push-Ups (2 min)"].plot(ax=ax, marker='o', label="Push-Ups")
    if df_chart["Plank Time (sec)"].notna().any():
        df_chart["Plank Time (sec)"].plot(ax=ax, marker='o', label="Plank (sec)")
    if df_chart["1.5 Mile Run Time (sec)"].notna().any():
        df_chart["1.5 Mile Run Time (sec)"].plot(ax=ax, marker='o', label="1.5 Mile Time (sec)")
    if df_chart["Weight (lbs)"].notna().any():
        df_chart["Weight (lbs)"].plot(ax=ax, marker='o', label="Weight")
    ax.set_ylabel("Performance Metrics")
    ax.legend()
    st.pyplot(fig)

elif page == "Food Intake":
    food_tracker.food_log_ui()
