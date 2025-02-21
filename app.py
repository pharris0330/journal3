import streamlit as st
from datetime import datetime
from supabase import create_client, Client
import os

# Supabase configuration - use Streamlit secrets or environment variables
SUPABASE_URL = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_entries():
    """Fetch all entries from Supabase"""
    response = supabase.table("time_logs").select("*").order("timestamp", desc=True).execute()
    return response.data

def add_entry(task, minutes):
    """Add a new entry to Supabase"""
    timestamp = datetime.now().isoformat()
    data = {
        "task": task,
        "minutes": minutes,
        "timestamp": timestamp
    }
    supabase.table("time_logs").insert(data).execute()

def main():
    # Page title
    st.title("Time Logger")
    
    # Fetch existing entries
    entries = fetch_entries()
    
    # Container for total minutes
    with st.container():
        col1, col2 = st.columns([3, 1])
        with col2:
            total_minutes = sum(entry['minutes'] for entry in entries)
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
            add_entry(task, minutes)
            st.rerun()  # Refresh the page to show new entry

    # Display all entries
    if entries:
        st.write("Logged Entries:")
        for entry in entries:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.text(f"{entry['task']}")
            with col2:
                st.text(f"{entry['minutes']} minutes")
            with col3:
                # Convert timestamp to readable format
                timestamp = datetime.fromisoformat(entry['timestamp']).strftime("%Y-%m-%d %H:%M:%S")
                st.text(f"{timestamp}")

if __name__ == "__main__":
    main()