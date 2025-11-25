import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# API_BASE = os.getenv('api-base')
API_BASE = st.secrets["API_BASE"]

def start_monitoring():

    st.title(f"Let's Start Monitoring, {st.session_state['username']}")

    # ----------- STATE INITIALIZATION ----------
    if "thresholds" not in st.session_state:
        st.session_state.thresholds = [{"profit_threshold": 0, "loss_value": 0}]  # default 1 item

    # ----------- INPUTS ----------
    initial_loss_threshold = st.number_input(
        "Initial Loss Threshold",
        min_value=1,
        value=3000,
        step=100
    )

    st.subheader("Profit–Loss Threshold Levels")

    # Show each threshold entry
    for i, row in enumerate(st.session_state.thresholds):

        col1, col2, col3 = st.columns([4, 4, 1])

        with col1:
            st.session_state.thresholds[i]["profit_threshold"] = st.number_input(
                f"Profit Threshold #{i+1}",
                min_value=0,
                value=row["profit_threshold"],
                step=100,
                key=f"pt_{i}"
            )

        with col2:
            st.session_state.thresholds[i]["loss_value"] = st.number_input(
                f"Loss Value #{i+1}",
                min_value=0,
                value=row["loss_value"],
                step=100,
                key=f"lv_{i}"
            )

        with col3:
            if st.button("🗑️", key=f"del_{i}"):
                if len(st.session_state.thresholds) > 1:
                    st.session_state.thresholds.pop(i)
                    st.rerun()
                else:
                    st.warning("Minimum 1 threshold required.")

    # ---------- Add Threshold Button ----------
    if len(st.session_state.thresholds) < 10:
        if st.button("➕ Add Threshold"):
            st.session_state.thresholds.append({"profit_threshold": 0, "loss_value": 0})
            st.rerun()
    else:
        st.info("Maximum 10 thresholds allowed!")

    st.write("---")

    # -------- Send API CALL --------
    if st.button("🚀 Start Monitoring"):
        payload = {
            "token":st.session_state.token,
            "client_id":st.session_state.client_id,
            "initial_loss_threshold": initial_loss_threshold,
            "thresholds": st.session_state.thresholds
        }

        response = requests.post(f"{API_BASE}/start_manual", json=payload)

        st.write("API Response:")
        st.json(response.json())
