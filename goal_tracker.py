import streamlit as st
import pandas as pd
import datetime

# Set page config
st.set_page_config(page_title="🎯 Goal Tracker", layout="wide")

# Title
st.title("🎯 Goal Tracker")

# Sidebar for adding goals
st.sidebar.header("➕ Set Your Goals")

goal_name = st.sidebar.text_input("Goal Name")
goal_category = st.sidebar.selectbox("Goal Category", ["Personal", "Academic", "Career", "Health"])
goal_description = st.sidebar.text_area("Goal Description")
goal_due_date = st.sidebar.date_input("Due Date", datetime.date.today())

add_goal = st.sidebar.button("➕ Add Goal")

# Initialize session state
if "goals" not in st.session_state:
    st.session_state.goals = []
if "notification" not in st.session_state:
    st.session_state.notification = ""

# Add goal functionality
if add_goal and goal_name:
    goal = {
        "Goal": goal_name,
        "Category": goal_category,
        "Description": goal_description,
        "Due Date": goal_due_date,
        "Status": "In Progress"
    }
    st.session_state.goals.append(goal)
    st.session_state.notification = "✅ Goal Added Successfully!"
    st.rerun()

# Display Goals
st.header("🏆 Your Goals")

if st.session_state.goals:
    goal_df = pd.DataFrame(st.session_state.goals)
    goal_df['Due Date'] = pd.to_datetime(goal_df['Due Date']).dt.strftime('%b %d, %Y')
    st.dataframe(goal_df, use_container_width=True)

    # Goal selection dropdown
    selected_goal = st.selectbox("🔄 Select a goal to update", [goal["Goal"] for goal in st.session_state.goals], index=None, placeholder="Choose a goal")

    if selected_goal:
        selected_idx = next((i for i, goal in enumerate(st.session_state.goals) if goal["Goal"] == selected_goal), None)
        
        if selected_idx is not None:
            st.write(f"### ✏️ Updating: {selected_goal}")
            status_options = ["Not Started", "In Progress", "Completed"]
            new_status = st.selectbox("📝 Update Status", status_options, index=status_options.index(st.session_state.goals[selected_idx]["Status"]))

            if st.button("✅ Update Status"):
                st.session_state.goals[selected_idx]["Status"] = new_status
                st.session_state.notification = f"✅ Status for '{selected_goal}' updated to {new_status}."
                st.rerun()

# Show notification
if st.session_state.notification:
    st.success(st.session_state.notification)
    st.session_state.notification = ""

# Track Progress
st.subheader("📊 Track Your Progress")
completed_goals = len([goal for goal in st.session_state.goals if goal["Status"] == "Completed"])
total_goals = len(st.session_state.goals)
completion_percentage = (completed_goals / total_goals) * 100 if total_goals > 0 else 0

st.progress(completion_percentage / 100)
st.write(f"🎯 Total Goals: {total_goals} | ✅ Completed: {completed_goals}")


      