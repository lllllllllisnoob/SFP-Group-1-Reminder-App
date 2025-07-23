import streamlit as st
import pandas as pd
from datetime import date, datetime

# --- PAGE SETUP ---
st.set_page_config(page_title="Reminder App", layout="centered")
st.title("📝 My Reminder App")
st.header("Welcome to your daily dashboard")

# --- INITIALIZE SESSION STATE ---
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# --- TO-DO FORM ---
with st.form("task_form", clear_on_submit=True):
    task_name = st.text_input("Task")
    due_date = st.date_input("Due Date", value=date.today())
    reminder_time = st.time_input("Reminder Time (optional)", value=datetime.now().time())

    # NEW: Select category and priority
    category = st.selectbox("Category", ["Work", "Study", "Personal", "Other"])
    priority = st.selectbox("Priority", ["High 🔴", "Medium 🟠", "Low 🟢"])

    submitted = st.form_submit_button("Add Task")

    if submitted and task_name:
        st.session_state.tasks.append({
            "task": task_name,
            "due_date": due_date,
            "reminder_time": reminder_time,
            "category": category,
            "priority": priority,
            "done": False
        })
        st.success("Task added!")

# --- TASK LIST ---
st.subheader("🗂️ To-Do List")

if not st.session_state.tasks:
    st.info("No tasks yet. Add something above!")
else:
    for i, task in enumerate(st.session_state.tasks):
        col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 2, 2, 2, 1])
        with col1:
            st.markdown(f"**{task['task']}**")
        with col2:
            st.write(f"📅 {task['due_date']}")
        with col3:
            st.write(f"⏰ {task['reminder_time']}")
        with col4:
            st.write(f"📁 {task['category']}")
        with col5:
            st.write(f"🏷️ {task['priority']}")
        with col6:
            if st.checkbox("Done", key=f"done_{i}", value=task["done"]):
                task["done"] = True

    # Remove completed tasks button
    if st.button("✅ Remove Completed Tasks"):
        st.session_state.tasks = [t for t in st.session_state.tasks if not t["done"]]
        st.success("Completed tasks removed!")

# --- CALENDAR VIEW ---
st.subheader("📆 Calendar View")
if st.session_state.tasks:
    df = pd.DataFrame(st.session_state.tasks)
    df = df[df["done"] == False]  # Show only incomplete tasks
    df["Date"] = pd.to_datetime(df["due_date"])
    st.dataframe(df[["task", "Date", "reminder_time", "category", "priority"]].rename(columns={
        "task": "Task",
        "Date": "Due Date",
        "reminder_time": "Reminder Time",
        "category": "Category",
        "priority": "Priority"
    }))
