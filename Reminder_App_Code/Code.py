import streamlit as st
import pandas as pd
from datetime import date, datetime

# --- PAGE SETUP ---
st.set_page_config(page_title="Reminder App", layout="wide")
st.markdown("""
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            padding-left: 1.5rem;
            padding-right: 1.5rem;
        }
        @media only screen and (max-width: 600px) {
            .stButton>button {
                width: 100%;
            }
            .stTextInput>div>div>input {
                font-size: 16px;
            }
        }
    </style>
""", unsafe_allow_html=True)

st.title("📝 My Reminder App")
st.header("Welcome to your daily dashboard")

# --- INITIALIZE SESSION STATE ---
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# --- TO-DO FORM ---
with st.form("task_form", clear_on_submit=True):
    task_name = st.text_input("Task")
    due_date = st.date_input("Due Date", value=date.today())
    reminder_time = st.time_input("Reminder Time", value=datetime.now().time())
    category = st.text_input("Category")
    priority = st.selectbox("Priority", ["Critical💀", "High 🔴", "Medium 🟠", "Low 🟢"])
    submitted = st.form_submit_button("Add Task")

    if submitted:
        if not task_name.strip():
            st.warning("⚠️ Please enter a task name.")
        elif not category.strip():
            st.warning("⚠️ Please enter a category.")
        else:
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
        cols = st.columns([3, 2, 2, 2, 2, 1])
        with cols[0]:
            st.markdown(f"**{task['task']}**")
        with cols[1]:
            st.write(f"{task['due_date']}")
        with cols[2]:
            st.write(f"{task['reminder_time']}")
        with cols[3]:
            st.write(f"{task['category']}")
        with cols[4]:
            st.write(f"{task['priority']}")
        with cols[5]:
            if st.checkbox("Done", key=f"done_{i}", value=task["done"]):
                task["done"] = True

    if st.button("✅ Remove Completed Tasks"):
        st.session_state.tasks = [t for t in st.session_state.tasks if not t["done"]]
        st.success("Completed tasks removed!")

# --- CALENDAR VIEW ---
st.subheader("📆 Calendar View")
if st.session_state.tasks:
    df = pd.DataFrame(st.session_state.tasks)
    df = df[df["done"] == False]  # Only show incomplete tasks
    df["Date"] = pd.to_datetime(df["due_date"])
    st.dataframe(df[["task", "Date", "reminder_time", "category", "priority"]]
        .rename(columns={
            "task": "Task",
            "Date": "Due Date",
            "reminder_time": "Reminder Time",
            "category": "Category",
            "priority": "Priority"
        }),
        use_container_width=True
    )
