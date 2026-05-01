import streamlit as st
from api_service import *
from datetime import datetime

#CONFIG
st.set_page_config(page_title="Task Management Pro", layout="wide")

#INIIALIZATION
if "add_title" not in st.session_state:
    st.session_state.add_title=""

if "add_desc" not in st.session_state:
    st.session_state.add_desc=""

if "add_priority" not in st.session_state:
    st.session_state.add_priority="low"

if "add_due_date" not in st.session_state:
    st.session_state.add_due_date=datetime.today()

if "reset_form" not in st.session_state:
    st.session_state.reset_form=False

#RESET fields after adding task

if st.session_state.reset_form:
    st.session_state.add_title=""

    st.session_state.add_desc=""

    st.session_state.add_priority="low"

    st.session_state.add_due_date=datetime.today()

    st.session_state.reset_form=False

#HEADER

st.title("My Task Manager")

#ADD TASK 

st.subheader("Add Task")

with st.form("add_task_form"):

    col1, col2=st.columns(2)

    with col1:
        title=st.text_input("Title", key="add_title")

    with col2:
        description=st.text_input("Description", key="add_desc")

    priority=st.selectbox("Priority",
                          ["low", "medium", "high"],
                          key="add_priority")
    
    due_date=st.date_input("Due Date", key="add_due_date")

    submitted=st.form_submit_button("Add Task")

    if submitted:
        if title.strip():
            add_task(title, description, priority, str(due_date))

            st.session_state.reset_form=True
            st.success("Task added")
            st.rerun()
        else:
            st.error("Title is required")
            st.divider()

#SEARCH BOX
search_query=st.text_input("Search Tasks", 
                           placeholder="Type to search any task with this title...", 
                           key ="search_input")

#FETCH ALL TASKS

if search_query:
    tasks=search_tasks(search_query)
else:
    tasks=get_tasks()

st.divider()

#SHOW TASK LIST
st.subheader("Your Tasks")

if not tasks:
    st.info("No tasks found.")

PRIORITY_LABLES = {
    "high":"High",
    "medium":"Medium",
    "low":"Low"
}

for task in tasks:
    with st.container():
        col1, col2, col3, col4=st.columns([5,2,2,1])

        with col1:
            st.markdown(f"**{task['title']}**")
            st.caption(task["description"])

        with col2:
            st.write(task["due_date"])

        with col3:
            st.markdown(f"**{PRIORITY_LABLES.get(task['priority'],task['priority'])}**")

        with col4:
            if st.button("Edit", key=f"edit_{task['id']}"):
                st.session_state.edit_task=task

            if st.button("Delete",key=f"del_{task['id']}"):
                delete_task(task["id"])
                st.success("Task deleted")
                st.rerun()
                #st.divider()

#EDIT TASK SECTION

if "edit_task" in st.session_state:
    task=st.session_state.edit_task

    st.subheader("Edit Task")

    with st.form("edit_task_form"):
        new_title=st.text_input("Title",value=task["title"], key="edit_title")

        new_desc=st.text_input("Description", value=task["description"], key="edit_desc")

        new_priority=st.selectbox("Priority",
                                    ["low", "medium", "high"],
                                    index=["low", "medium", "high"].index(task["priority"]),
                                    key ="edit_priority")
        
        try:
            default_date = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
        except:
            default_date = datetime.today().date()

        new_date=st.date_input("Due Date", value=default_date, key="edit_due_date")

        col1, col2=st.columns(2)

        with col1:
            save=st.form_submit_button("Save Changes")

        with col2:
            cancel=st.form_submit_button("Cancel")

        if save:
            update_task(task["id"],
                         new_title, 
                         new_desc, 
                         new_priority,
                         str(new_date), 
                         task["completed"]
                         )
            
            del st.session_state.edit_task
            st.success("Task updated")
            st.rerun()

        if cancel:
            del st.session_state.edit_task
            st.rerun()

        
       