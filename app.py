import streamlit as st
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import pytz  # Add this for timezone support

# Load environment variables from .env file (local only)
load_dotenv()

# Try Streamlit secrets first (Cloud), then fall back to env vars (local)
SUPABASE_URL = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")

# Debug and validation
if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("Supabase configuration missing!")
    st.write("SUPABASE_URL:", SUPABASE_URL)
    st.write("SUPABASE_KEY:", SUPABASE_KEY)
    st.stop()

# Initialize Supabase client
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error(f"Failed to initialize Supabase: {str(e)}")
    st.stop()

# Define EST timezone
EST = pytz.timezone('America/New_York')

def fetch_entries():
    response = supabase.table("time_logs").select("*").order("timestamp", desc=True).execute()
    return response.data

def add_entry(task, minutes):
    # Store in UTC (Supabase standard), conversion to EST happens on display
    timestamp = datetime.now(pytz.UTC).isoformat()
    data = {"task": task, "minutes": minutes, "timestamp": timestamp}
    supabase.table("time_logs").insert(data).execute()

def main():
    st.markdown("""
## Paul's Accountability Journal (2025 GOAL = 4k min)
### -Read Bible 3 times per day
### -Read a Book 2 times per day
### -Walk 2 times per day                
""")

    entries = fetch_entries()
    
    with st.container():
        col1, col2 = st.columns([3, 1])
        with col2:
            total_minutes = sum(entry['minutes'] for entry in entries)
            st.metric("Total Minutes", total_minutes)

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
            st.rerun()

    if entries:
        st.write("Logged Entries (EST):")
        for entry in entries:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.text(entry['task'])
            with col2:
                st.text(f"{entry['minutes']} minutes")
            with col3:
                # Convert UTC to EST
                utc_time = datetime.fromisoformat(entry['timestamp'])
                est_time = utc_time.astimezone(EST)
                timestamp = est_time.strftime("%Y-%m-%d %H:%M:%S %Z")
                st.text(timestamp)

if __name__ == "__main__":
    main()