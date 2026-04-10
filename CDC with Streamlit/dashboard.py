import streamlit as st
import pandas as pd
import json
import os

# --- 1. SETTINGS & THEME ---
st.set_page_config(
    page_title="CDC Stream Monitor",
    page_icon="📟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for high-contrast visibility
st.markdown("""
    <style>
    /* Main background and base text */
    .stApp {
        background-color: #0E1117;
        color: #E0E0E0;
    }
    
    /* Force Metric Labels to be bright white/grey */
    [data-testid="stMetricLabel"] {
        color: #9CA3AF !important;
        font-size: 1rem !important;
    }
    
    /* Force Metric Values to be Neon Green for visibility */
    [data-testid="stMetricValue"] {
        color: #00FF41 !important;
    }

    /* Professional styling for the Table area */
    .stDataFrame {
        border: 1px solid #30363d;
        border-radius: 8px;
    }

    /* Custom scrollbar for dark mode */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #0E1117; }
    ::-webkit-scrollbar-thumb { background: #30363d; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #484f58; }
    </style>
    """, unsafe_allow_html=True)

st.title("📟 MySQL CDC Real-Time Monitor")
st.markdown("---")

# --- 2. DATA PROCESSING ---
def get_new_data():
    file_path = "data/events.jsonl"
    if not os.path.exists(file_path):
        return pd.DataFrame()
    
    events = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    
    df = pd.DataFrame(events)
    if not df.empty:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values(by='timestamp', ascending=False)
    return df

# --- 3. SIDEBAR ---
with st.sidebar:
    st.header("⚡ Controls")
    refresh_btn = st.button("Refresh Stream", type="primary", use_container_width=True)
    st.divider()
    st.info("Reading from `data/events.jsonl`.")

# --- 4. MAIN DISPLAY ---
if refresh_btn or 'initialized' not in st.session_state:
    st.session_state.initialized = True
    data = get_new_data()
    
    if not data.empty:
        # Metrics with custom labels
        m1, m2, m3 = st.columns(3)
        m1.metric("TOTAL RECORDS", f"{len(data):,}")
        m2.metric("LAST ACTION", data['event_type'].iloc[0])
        m3.metric("TARGET TABLE", data['table'].iloc[0].upper())

        st.subheader("Latest Database Changes")
        
        # Professional Table Configuration
        st.dataframe(
            data,
            column_config={
                "timestamp": st.column_config.DatetimeColumn("Time (UTC)", format="HH:mm:ss"),
                "event_type": "Action",
                "schema": "Database",
                "table": "Table",
                "data": st.column_config.JsonColumn("Payload")
            },
            hide_index=True,
            use_container_width=True # Ensure it takes full width
        )
    else:
        st.warning("Awaiting stream data... Check your MySQL CDC script.")