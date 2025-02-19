import streamlit as st
#import psycopg2
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine

# Load database credentials from Streamlit secrets
DB_PARAMS = st.secrets

# Create a connection engine
def get_engine():
    return create_engine(f"postgresql://{DB_PARAMS['user']}:{DB_PARAMS['password']}@{DB_PARAMS['host']}:{DB_PARAMS['port']}/{DB_PARAMS['dbname']}")


def create_table():
    engine = get_engine()
    with engine.connect() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS journal (
                        id SERIAL PRIMARY KEY,
                        entry TEXT,
                        minutes INT,
                        created_at TIMESTAMP DEFAULT NOW()
                      )''')

def insert_entry(entry, minutes):
    engine = get_engine()
    with engine.connect() as conn:
        conn.execute("INSERT INTO journal (entry, minutes) VALUES (%s, %s)", (entry, minutes))

def get_entries():
    engine = get_engine()
    with engine.connect() as conn:
        df = pd.read_sql("SELECT * FROM journal ORDER BY created_at DESC", conn)
    return df

# UI Elements
st.title("📝 Journal Tracker")

st.sidebar.header("📊 Total Minutes Logged")

# Create table if it doesn't exist
create_table()

# Input fields
with st.form("entry_form"):
    entry = st.text_area("New Journal Entry:", height=100)
    minutes = st.number_input("Time Spent (minutes):", min_value=1, step=1)
    submit = st.form_submit_button("Add Entry")

if submit and entry:
    insert_entry(entry, minutes)
    st.success("Entry Added!")
    st.experimental_rerun()

# Fetch and display entries
df = get_entries()
total_minutes = df["minutes"].sum() if not df.empty else 0

# Display total time logged
st.sidebar.write(f"**Total Time:** {total_minutes} minutes")

if not df.empty:
    for _, row in df.iterrows():
        with st.container():
            st.write(f"📝 {row['entry']}")
            st.write(f"⏳ {row['minutes']} minutes")
            st.write("---")
else:
    st.write("No entries yet. Start journaling!")
