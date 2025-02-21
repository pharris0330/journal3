import streamlit as st
from datetime import datetime

def main():
    # Page title
    st.markdown("""
## Paul's Accountability Tracker
### -Read Bible 3 times per day
### -Walk 2 times per day
### -Read Book 2 times per day
""")
    
    # Initialize session state for entries if not exists
    if 'entries' not in st.session_state:
        st.session_state.entries = []
    
    # Container for total minutes
    with st.container():
        col1, col2 = st.columns([3, 1])
        with col2:
            total_minutes = sum(entry['minutes'] for entry in st.session_state.entries)
            st.metric("Total Minutes", total_minutes)

    # Input form for new entries
    with st.form(key='entry_form', clear_on_submit=True):
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            task = st.text_input("Task Description")
        with col2:
            minutes = st.number_input("Minutes", min_value=0, step=1)
        with col3:
            submit = st.form_submit_button("Add Entry")
        
        if submit and task:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.entries.append({
                "task": task,
                "minutes": minutes,
                "timestamp": current_time
            })

    # Display all entries
    if st.session_state.entries:
        st.write("Logged Entries:")
        for i, entry in enumerate(st.session_state.entries):
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.text(f"{entry['task']}")
            with col2:
                st.text(f"{entry['minutes']} minutes")
            with col3:
                st.text(f"{entry['timestamp']}")

if __name__ == "__main__":
    main()