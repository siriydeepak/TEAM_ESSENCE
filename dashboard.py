import sys
import datetime
import time
from pathlib import Path

import streamlit as st
import yaml
import plotly.graph_objects as go

# Absolute path handling to safely import from root and prevent FileNotFound errors
ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

# Import required tools without breaking OpenClaw SDK or existing logic
from network_check import get_local_ip, check_ngrok_status
from flux_engine import parse_expiry, get_decay_days, TODAY

LEDGER_PATH = ROOT_DIR / "pantry_ledger.yaml"

st.set_page_config(page_title="Pantry Decay Dashboard", layout="wide")

def load_ledger():
    if not LEDGER_PATH.exists():
        return []
    try:
        with open(LEDGER_PATH, "r") as f:
            return yaml.safe_load(f) or []
    except Exception:
        return []

def render_dashboard():
    st.title("AetherShelf: Dynamic Flux Dashboard")
    st.caption("Powered by OpenClaw 2026.4.27 | Offline-Resilient Node")
    
    # ---------------------------------------------------------
    # Task 2: The "Offline" Hybrid Failsafe (Network Resilience)
    # ---------------------------------------------------------
    col1, col2 = st.columns(2)
    local_ip = get_local_ip()
    local_url = f"http://{local_ip}:8501"
    
    with col1:
        st.info(f"🌐 Local Network IP: `{local_url}`")
        
    with col2:
        if check_ngrok_status():
            st.success("🟢 Ngrok Tunnel: ACTIVE (Global Sync)")
        else:
            st.error("⚠️ Running in Local-Only Mode. Connect to the same Wi-Fi to view.")
            
    st.markdown("---")
    
    items = load_ledger()
    if not items:
        st.warning("Pantry ledger is empty. Waiting for OpenClaw triggers...")
        return

    # ---------------------------------------------------------
    # Task 1: Dynamic Flux Visualization (The Entropy Curve)
    # ---------------------------------------------------------
    
    # Generate the X-axis for the next 7 days
    dates = [TODAY + datetime.timedelta(days=i) for i in range(8)]
    date_strings = [d.strftime("%Y-%m-%d") for d in dates]
    
    fig = go.Figure()

    critical_threshold = 2.0  # Less than 3 days means we cross the 2.0 marker

    for item in items:
        name = item.get("name", "Unknown")
        qty = int(item.get("quantity", 0))
        if qty <= 0:
            continue
            
        expiry = parse_expiry(item.get("estimated_expiry"))
        if not expiry:
            decay = get_decay_days(name)
            expiry = TODAY + datetime.timedelta(days=decay)
            
        # Calculate base days remaining
        initial_days = (expiry - TODAY).days
        
        y_values = []
        for i in range(8):
            # The curve slopes downwards as time increases
            rem = initial_days - i
            y_values.append(max(0, rem))
            
        fig.add_trace(go.Scatter(
            x=date_strings, 
            y=y_values, 
            mode='lines+markers', 
            name=name,
            line=dict(width=4),
            marker=dict(size=8)
        ))

    # Add the "Utility Gap" Marker (Horizontal Critical Threshold)
    fig.add_hline(
        y=critical_threshold, 
        line_dash="dash", 
        line_color="rgba(255, 60, 60, 1)", 
        annotation_text="Critical Threshold (Utility Gap Marker)"
    )

    # Visually shade the critical zone in red
    fig.add_hrect(
        y0=0, y1=critical_threshold, 
        fillcolor="red", opacity=0.15, 
        layer="below", line_width=0,
    )

    fig.update_layout(
        title="7-Day Flux Entropy Forecast",
        xaxis_title="Time (Next 7 Days)",
        yaxis_title="Freshness Remaining (Days)",
        hovermode="x unified",
        template="plotly_dark",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    # Plotly is resilient local-first out of the box when used inside Streamlit 
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

def main():
    # ---------------------------------------------------------
    # Task 3: Real-Time Syncing (Background Refresh)
    # ---------------------------------------------------------
    placeholder = st.empty()
    
    with placeholder.container():
        render_dashboard()
        
    # Polls pantry_ledger.yaml every 3 seconds to instantly reflect changes
    # triggered by EmailParser or the OpenClaw Gateway.
    time.sleep(3)
    st.rerun()

if __name__ == "__main__":
    main()
