import streamlit as st
import pandas as pd
from scheduler import Doctor, Patient

# --- CONFIG ---
st.set_page_config(page_title="MedSync Direct", page_icon="⚡", layout="wide")

# --- 🎨 THEME (Keeping your Dark/Apple Look) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    div[data-testid="stMetric"] {
        background-color: #1A1A1A;
        border: 1px solid #333333;
        border-radius: 12px;
        padding: 15px;
    }
    div[data-testid="stMetric"] label { color: #888888; font-size: 0.8rem; }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] { color: #FFFFFF; font-size: 1.8rem; }
    
    /* TABLE STYLING */
    div[data-testid="stDataFrame"] {
        background-color: #1A1A1A;
        border: 1px solid #333333;
        border-radius: 12px;
        padding: 10px;
    }
    h2 { color: white !important; }
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- BACKEND ---
@st.cache_resource
def get_doctor_system():
    return Doctor("Gregory House", "Diagnostician")

doctor = get_doctor_system()

# --- HEADER & METRICS ---
st.markdown("## ⚡ MedSync Manager")

total = doctor.MAX_PATIENTS
booked = sum(1 for p in doctor.schedule.values() if p is not None)
free = total - booked
progress = booked / total

c1, c2, c3, c4 = st.columns(4)
c1.metric("Status", "Online 🟢") 
c2.metric("Total Slots", f"{total}")
c3.metric("Patients", f"{booked}")
c4.metric("Available", f"{free}")
st.progress(progress)
st.write("") 

# --- THE INTERACTIVE SCHEDULE ---

# 1. BUILD THE DATAFRAME FROM LIVE DATA
# We rebuild this from scratch every time the script runs
schedule_data = []
for time_slot, patient in doctor.schedule.items():
    schedule_data.append({
        "Time": time_slot,
        "Status": "🔴 Booked" if patient else "🔹 Open",
        "Patient Name": patient.name if patient else None,
        "Notes": patient.ailment if patient else None,
        "Clear": False # Always start unchecked
    })

df = pd.DataFrame(schedule_data)

# 2. RENDER THE EDITOR
edited_df = st.data_editor(
    df,
    use_container_width=True,
    hide_index=True,
    height=600,
    column_config={
        "Time": st.column_config.TextColumn("Time", disabled=True, width="small"),
        "Status": st.column_config.TextColumn("Status", disabled=True, width="small"),
        "Patient Name": st.column_config.TextColumn("Patient Name", width="medium"),
        "Notes": st.column_config.TextColumn("Notes", width="large"),
        "Clear": st.column_config.CheckboxColumn("Clear Slot?", help="Check to remove patient", width="small")
    },
    key="schedule_editor",
    num_rows="fixed"
)

# 3. CHANGE DETECTION LOGIC
# We compare the 'edited' version to the original 'df'
if not df.equals(edited_df):
    
    for index, row in edited_df.iterrows():
        time_slot = row["Time"]
        
        # User Actions from the Table
        is_cleared = row["Clear"]
        new_name = row["Patient Name"]
        new_note = row["Notes"]
        
        # Current Backend State
        current_patient = doctor.schedule[time_slot]
        current_name = current_patient.name if current_patient else None
        
        # ACTION 1: "CLEAR" CHECKBOX CLICKED
        # This takes priority. If checked, we nuke the slot.
        if is_cleared:
            doctor.cancel_appointment(time_slot)
            st.toast(f"🗑️ Cleared slot {time_slot}", icon="🗑️")
            # We don't need to manually uncheck it here; 
            # the st.rerun() below will reload the table with "Clear: False" by default.
            
        # ACTION 2: NAME ADDED (BOOKING)
        elif new_name and new_name != current_name:
            # If no note provided, give a default one so it's not empty
            if not new_note: new_note = "Routine Visit"
            doctor.book_appointment(Patient(new_name, new_note), time_slot)
            st.toast(f"✅ Booked {new_name}", icon="💾")
            
        # ACTION 3: NAME DELETED MANUALLY
        elif not new_name and current_name and not is_cleared:
            doctor.cancel_appointment(time_slot)
            st.toast(f"🗑️ Cancelled {current_name}", icon="🗑️")
            
        # ACTION 4: UPDATED NOTES
        elif new_name == current_name and new_note != (current_patient.ailment if current_patient else None):
             if current_patient: # Only update if patient exists
                doctor.book_appointment(Patient(new_name, new_note), time_slot)
                st.toast("📝 Note updated", icon="✏️")

    # CRITICAL: Force the app to reload immediately.
    # This ensures the "Status" column updates from "Open" to "Booked" (or vice versa)
    st.rerun()