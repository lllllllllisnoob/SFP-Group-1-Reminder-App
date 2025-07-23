import streamlit as st
import pandas as pd
from datetime import date, datetime

# --- PAGE SETUP ---
st.set_page_config(page_title="Reminder App", layout="wide")

# --- INITIALIZE SESSION STATE ---
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# --- SIDEBAR MENU ---
menu = st.sidebar.radio("📂 Select Page", ["🏠 Home (Add Task)", "📝 To-Do List & Calendar"])

# ------------------- HOME PAGE ------------------- #
if menu == "🏠 Home (Add Task)":
    st.markdown("## 🏠 My Reminder App")
    st.markdown("### ➕ Add a New Task")
    st.divider()

    with st.form("task_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            task_name = st.text_input("📝 Task Name")
            reminder_time = st.time_input("⏰ Reminder Time", value=datetime.now().time())
            category = st.text_input("📁 Category")
        with col2:
            due_date = st.date_input("📅 Due Date", value=date.today())
            priority = st.selectbox("🏷️ Priority", ["Critical💀", "High 🔴", "Medium 🟠", "Low 🟢"])

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
                st.success("✅ Task added successfully!")

# ------------------- TO-DO LIST & CALENDAR PAGE ------------------- #
elif menu == "📝 To-Do List & Calendar":
    st.markdown("## 📝 To-Do List")
    st.markdown("### 🗂️ Your Tasks and Calendar")
    st.divider()

    if not st.session_state.tasks:
        st.info("📭 No tasks yet. Go to the Home page to add some!")
    else:
        # --- TASK LIST ---
        st.subheader("📋 Task List")
        done_indices = []

        for i, task in enumerate(st.session_state.tasks):
            col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 2, 2, 2, 1])
            with col1:
                st.markdown(f"**📝 {task['task']}**")
            with col2:
                st.markdown(f"📅 {task['due_date']}")
            with col3:
                st.markdown(f"⏰ {task['reminder_time']}")
            with col4:
                st.markdown(f"📁 {task['category']}")
            with col5:
                st.markdown(f"🏷️ {task['priority']}")
            with col6:
                marked_done = st.checkbox("Done", key=f"done_{i}", value=False)
                if marked_done:
                    done_indices.append(i)

        st.markdown("---")
        if st.button("✅ Remove Completed Tasks"):
            st.session_state.tasks = [t for i, t in enumerate(st.session_state.tasks) if i not in done_indices]
            st.success("✅ Completed tasks removed!")

        # --- CALENDAR VIEW ---
        st.subheader("📆 Calendar View")
        if st.session_state.tasks:
            df = pd.DataFrame(st.session_state.tasks)
            df["Date"] = pd.to_datetime(df["due_date"])
            st.dataframe(df[["task", "Date", "reminder_time", "category", "priority"]].rename(columns={
                "task": "Task",
                "Date": "Due Date",
                "reminder_time": "Reminder Time",
                "category": "Category",
                "priority": "Priority"
            }), use_container_width=True)
        else:
            st.info("✅ No tasks to display.")
